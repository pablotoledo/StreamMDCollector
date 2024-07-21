# StreamMDCollector

StreamMDCollector is a Streamlit-based web application that compiles Markdown files from Git repositories into a single document. It supports various Git hosting services and authentication methods, making it ideal for quick documentation gathering and review.

The idea is use that compiled markdown to use them as a context for a chatbot, for example.

## Features

- Clone Git repositories using HTTPS
- Support for public and private repositories
- Authentication options: No authentication, Token, Username and Password
- Branch selection
- Compile all Markdown files from the selected branch into a single document
- Preview compiled documentation in the app
- Download compiled documentation as a single Markdown file

## Quick Start with Docker

The easiest way to run StreamMDCollector is using the pre-built Docker image:

```bash
docker run -p 8501:8501 jtoledog/streammdcollector
```

Then open your web browser and go to `http://localhost:8501`.

## Installation for Local Development

If you want to run StreamMDCollector locally or contribute to its development, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/StreamMDCollector.git
   cd StreamMDCollector
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

## Usage

1. Enter the URL of the Git repository you want to compile documentation from.
2. Select the authentication method if required (No authentication, Token, or Username and Password).
3. Click "Clone Repository" to fetch the repository.
4. Select the branch you want to compile documentation from.
5. Click "Compile documentation" to generate the combined Markdown file.
6. Preview the compiled documentation in the app.
7. Use the "Download combined documentation" link to save the compiled Markdown file.

## Building the Docker Image Locally

If you want to build the Docker image yourself:

```bash
docker build -t streammdcollector .
docker run -p 8501:8501 streammdcollector
```

## Contributing

Contributions to StreamMDCollector are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

