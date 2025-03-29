# Spam Detection App

A Streamlit app utilizing LLM-powered agents for spam detection.


## Quick Start

1. Clone the repository
2. Navigate to the project directory
3. Run: `docker-compose up -d`
4. Access the app at [http://localhost:8501](http://localhost:8501)

> **Note:** First-time setup may take longer as Ollama downloads the model.

### Stopping the App

- Run: `docker-compose down`

## Usage

1. Enter text in the input field
2. Click "Submit" to analyze
3. View results: spam classification, confidence score, and reasoning

## Architecture

- **Frontend:** Streamlit
- **Agents:** Sentiment, grammar, URL, domain analysis
- **Decision Engine:** Combines agent outputs
- **LLM Inference:** Powered by Ollama


## Decision Engine

- Naive decision maker aggregates predictions and computes a final score.
- Optimized using Bayesian Optimization.
- Demonstrates varied models from deep-learning classifiers to heuristics.

## Chosen LLM & models

The application utilizes the Ollama LLM for two agents, which provides robust language model capabilities for spam detection. In addition, I used a DL based classifier for the URL engine.

## Agent Flow Overview

The system consists of multiple agents that analyze input text:

- **Sentiment Agent:** Evaluates the emotional tone of the text.
- **Grammar Agent:** Checks for grammatical correctness and unnatural patterns.
- **URL Agent:** Detects and analyzes URLs present in the text.
- **Domain Agent:** Assesses the reputation of domains linked in the text.

These agents work in tandem, with their outputs aggregated by the decision engine to provide a final classification.

## Design Decisions and Trade-offs

- The decision engine employs a naive approach for simplicity and ease of understanding, and mainly to emphasize the option to build a system with different model types, from a simple heurstic through a basic classifier, to LLMs.
- Bayesian Optimization was chosen to improve the decision-making process without significantly increasing complexity.
- In a production environment, the agents would typically operate in parallel, utilizing a Kubernetes architecture. However, for the purposes of this task, such an approach is excessive and beyond the project's scope.
