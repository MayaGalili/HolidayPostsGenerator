---
title: HolidayPostsGenerator
app_file: app.py
sdk: gradio
sdk_version: 5.31.0
---

# Holiday Posts Generator

A LinkedIn post generator for Ag-Tech companies using holiday data. This application uses OpenAI's GPT models to generate engaging "did you know?" style posts based on holiday information.

## Setup with uv

This project is configured to work with `uv`, a fast Python package manager and project manager.

### Prerequisites

1. Install `uv` if you haven't already:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Installation

1. Clone or navigate to the project directory
2. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   uv sync
   ```

3. Set up environment variables:
   ```bash
   cp env.template .env
   # Edit .env and add your OpenAI API key
   ```

### Running the Application

You can run the app in two ways:

**Option 1: Using the run script (recommended)**
```bash
uv run python run.py
```

**Option 2: Direct execution**
```bash
uv run python app.py
```

The `uv.lock` file ensures all dependencies are locked to specific versions for reproducible builds.

The application will start a Gradio web interface where you can interact with the LinkedIn post generator.

## Features

- Interactive chat interface for generating LinkedIn posts
- Holiday database integration
- OpenAI GPT-4 integration for content generation
- Professional and engaging post suggestions

## Dependencies

- gradio: Web interface framework
- openai: OpenAI API client
- pandas: Data manipulation
- pypdf: PDF processing
- python-dotenv: Environment variable management
