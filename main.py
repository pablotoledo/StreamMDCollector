import base64
import io
import logging
import os
import tempfile
import threading

import git
import streamlit as st
from git import RemoteProgress, Repo

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class ProgressPrinter(RemoteProgress):
    def __init__(self):
        super().__init__()
        self.progress = 0

    def update(self, op_code, cur_count, max_count=None, message=""):
        self.progress = float(cur_count) / float(max_count or 100)
        logging.info(f"Clone progress: {self.progress:.2%}")

    def __call__(self, op_code, cur_count, max_count=None, message=""):
        self.update(op_code, cur_count, max_count, message)


def clone_repo(repo_url, auth=None):
    logging.info(f"Attempting to clone repository: {repo_url}")
    tmp_dir = tempfile.mkdtemp()
    if auth:
        if "token" in auth:
            repo_url = f"https://{auth['token']}@{repo_url.split('://')[1]}"
        elif "username" in auth and "password" in auth:
            repo_url = f"https://{auth['username']}:{auth['password']}@{repo_url.split('://')[1]}"

    progress_printer = ProgressPrinter()
    try:
        repo = Repo.clone_from(repo_url, tmp_dir, progress=progress_printer)
        logging.info("Repository cloned successfully")
        return repo, progress_printer, tmp_dir
    except git.GitCommandError as e:
        logging.error(f"Git command error: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during cloning: {e}")
        raise


def get_branches(repo):
    try:
        branches = [ref.name for ref in repo.references if isinstance(ref, git.RemoteReference)]
        if not branches:
            branches = [branch.name for branch in repo.branches]
        logging.info(f"Found branches: {branches}")
        return branches
    except Exception as e:
        logging.error(f"Error fetching branches: {e}")
        return []


def get_md_files(repo):
    logging.info("Searching for Markdown files")
    md_files = []
    try:
        for root, _, files in os.walk(repo.working_dir):
            for file in files:
                if file.endswith(".md") or file.endswith(".mdx"):
                    relative_path = os.path.relpath(os.path.join(root, file), repo.working_dir)
                    md_files.append(relative_path)
        logging.info(f"Found {len(md_files)} Markdown files")
        return md_files
    except Exception as e:
        logging.error(f"Error while getting Markdown files: {e}")
        raise


def combine_md_files(repo, md_files):
    logging.info("Combining Markdown files")
    combined = io.StringIO()
    for file_path in md_files:
        try:
            full_path = os.path.join(repo.working_dir, file_path)
            with open(full_path, encoding="utf-8") as file:
                content = file.read()
            combined.write(f"# {file_path}\n\n")
            combined.write(content)
            combined.write("\n\n---\n\n")
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
    return combined.getvalue()


def main():
    st.title("Git Repository MD Documentation Compiler")

    repo_url = st.text_input("Git repository URL:")
    auth_method = st.radio(
        "Authentication method:", ("No authentication", "Token", "Username and Password")
    )

    auth = None
    if auth_method == "Token":
        token = st.text_input("Access token:", type="password")
        auth = {"token": token}
    elif auth_method == "Username and Password":
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        auth = {"username": username, "password": password}

    if st.button("Clone Repository"):
        if repo_url:
            try:
                with st.spinner("Cloning repository..."):
                    repo, progress_printer, tmp_dir = clone_repo(repo_url, auth)
                    st.session_state.repo = repo
                    st.session_state.tmp_dir = tmp_dir
                    st.success("Repository cloned successfully!")
            except Exception as e:
                st.error(f"Error cloning repository: {e!s}")
                return

            branches = get_branches(repo)
            if branches:
                st.session_state.selected_branch = st.selectbox("Select a branch:", branches)
            else:
                st.warning("No branches found. You can manually enter a branch name.")
                st.session_state.selected_branch = st.text_input(
                    "Enter branch name (e.g., 'main' or 'master'):"
                )

    if "repo" in st.session_state and "selected_branch" in st.session_state:
        if st.button("Compile documentation"):
            try:
                repo = st.session_state.repo
                selected_branch = st.session_state.selected_branch

                progress_bar = st.progress(0)
                status_text = st.empty()

                def compile_docs():
                    nonlocal combined_md
                    repo.git.checkout(selected_branch)
                    md_files = get_md_files(repo)
                    combined_md = combine_md_files(repo, md_files)

                combined_md = ""
                thread = threading.Thread(target=compile_docs)
                thread.start()

                while thread.is_alive():
                    thread.join(0.1)
                    progress_bar.progress(1)
                    status_text.text("Compiling MD files...")

                status_text.text("Compilation completed!")

                # Create download link
                b64 = base64.b64encode(combined_md.encode()).decode()
                href = (
                    f'<a href="data:file/md;base64,{b64}" '
                    'download="combined_docs.md">Download combined documentation</a>'
                )
                st.markdown(href, unsafe_allow_html=True)

                # Show preview
                st.text_area("Content preview:", combined_md, height=300)
            except Exception as e:
                logging.error(f"An error occurred during compilation: {e!s}")
                st.error(f"An error occurred: {e!s}")


# dummy

if __name__ == "__main__":
    main()
