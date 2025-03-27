# Spam Detection App

A Streamlit application utilizing multiple LLM-powered agents for spam message detection.

## Features

- **Multi-agent architecture** for comprehensive spam analysis
- **Sentiment analysis** to detect manipulative language
- **Grammar analysis** to identify unnatural patterns
- **URL detection** and analysis
- **Domain reputation** checking
- **Configurable decision engine** with weighted agent contributions

## Quick Start with Docker Compose

### Prerequisites

- Docker & Docker Compose

### Steps

1. Clone the repository
2. Navigate to the project directory
3. Run: `docker-compose up -d`
4. Access the app at [http://localhost:8501](http://localhost:8501)

> **Note:** First-time setup may take longer as Ollama downloads the LLM model.

### Stopping the Application

- Run: `docker-compose down`

## Usage

1. Enter text in the sidebar input field
2. Click "Submit" to analyze
3. View results: spam classification, confidence score, and reasoning

## Architecture

- **Frontend:** Streamlit for user interaction
- **Agents:** Sentiment, grammar, URL, domain analysis
- **Decision Engine:** Combines agent outputs
- **LLM Inference:** Powered by Ollama

## Configuration

- Managed with Hydra
- Config files in `configs/`

## Development Setup

1. Install Python 3.10+
2. Install dependencies: `pip install -r requirements.txt`
3. Run Ollama locally and pull the required model
4. Launch the app: `streamlit run app.py`
