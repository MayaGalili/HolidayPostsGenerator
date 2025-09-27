---
title: HolidayPostsGenerator
app_file: app.py
sdk: gradio
sdk_version: 5.31.0
---

# Holiday Posts Generator

A LinkedIn post generator for Ag-Tech companies using holiday data. This application uses OpenAI's GPT models to generate engaging "did you know?" style posts based on holiday information.

## Preview

Here's how the application looks when deployed on Hugging Face Spaces:

![Holiday Posts Generator Interface](resources/Chat_Screenshot.png)

The chatbot interface allows users to:
- Ask for posts for specific dates
- Receive 3 different LinkedIn post ideas tailored for Ag-Tech companies
- Get posts with relevant hashtags and engaging content
- Choose their favorite post from the generated options

## Prerequisites

- **Python 3.9 or higher**
- **OpenAI API Key** - Get one from [OpenAI Platform](https://platform.openai.com/api-keys)
- **uv** (recommended) or pip for package management

## Quick Start

### Option 1: Using uv (Recommended)

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd HolidayPostsGenerator
   uv venv
   uv sync
   ```

3. **Set up your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Or create a `.env` file:
   ```bash
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

4. **Run the application**:
   ```bash
   uv run python run.py
   ```

### Option 2: Using pip

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd HolidayPostsGenerator
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Set up your OpenAI API key** (same as above)

3. **Run the application**:
   ```bash
   python run.py
   ```

## Deployment

### Deploy to Hugging Face Spaces

1. **Create a new Space** on [Hugging Face Spaces](https://huggingface.co/new-space)
2. **Choose Gradio SDK** when creating the space
3. **Upload your files** to the space:
   - `app.py`
   - `pyproject.toml` 
   - `uv.lock` (or `requirements.txt`)
   - `resources/` folder (with `HolidaysDB.tsv`)
   - `README.md`

4. **Set environment variables** in your Space settings:
   - Go to Settings → Variables and secrets
   - Add `OPENAI_API_KEY` with your API key

5. **Your app will automatically deploy!** The Gradio interface will be available at your space URL.

### Deploy to other platforms

The app can be deployed to any platform that supports Python web applications:
- **Railway**: Connect your GitHub repo
- **Render**: Deploy as a web service
- **Heroku**: Use the included `pyproject.toml`
- **Docker**: Create a Dockerfile (see example below)

#### Docker Example
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 7860
CMD ["python", "run.py"]
```

## Running the Application

Once running, the application will:
- Start a Gradio web interface (usually at `http://localhost:7860`)
- Allow you to chat with the LinkedIn post generator
- Generate holiday-themed posts for your Ag-Tech company

The `uv.lock` file ensures all dependencies are locked to specific versions for reproducible builds.

## Features

- Interactive chat interface for generating LinkedIn posts
- Holiday database integration
- OpenAI GPT-4 integration for content generation
- Professional and engaging post suggestions

## Troubleshooting

### Common Issues

**"OpenAI API key not found" error:**
- Make sure you've set the `OPENAI_API_KEY` environment variable
- Check that your API key is valid and has credits
- Restart the application after setting the environment variable

**"Module not found" errors:**
- Make sure you've installed all dependencies: `uv sync` or `pip install -r requirements.txt`
- Check that you're in the correct virtual environment

**App won't start:**
- Ensure Python 3.9+ is installed
- Check that port 7860 is available (or Gradio will find another port)
- Look at the console output for specific error messages

**Hugging Face deployment issues:**
- Make sure all required files are uploaded to your Space
- Check that the `OPENAI_API_KEY` is set in Space settings
- Verify the Space is using the correct Python version (3.9+)

## Dependencies

- **gradio**: Web interface framework
- **openai**: OpenAI API client  
- **pandas**: Data manipulation
- **pypdf**: PDF processing
- **python-dotenv**: Environment variable management

## File Structure

```
HolidayPostsGenerator/
├── app.py                 # Main application code
├── run.py                 # Simple runner script
├── pyproject.toml         # Project configuration
├── uv.lock               # Locked dependencies (uv)
├── requirements.txt      # Dependencies (pip)
├── README.md             # This file
└── resources/
    ├── HolidaysDB.tsv    # Holiday database
    └── Chat_Screenshot.png # Interface preview
```
