#!/bin/bash

# Start ollama in the background
ollama serve &

# Wait for the server to start
echo "Waiting for Ollama server to be ready..."
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    sleep 1
done

echo "Ollama server is ready!"
MODEL_NAME=$(awk -F'"' '/name:/{print $2}' /tmp/model.yaml)

echo "Creating/updating model $MODEL_NAME..."
ollama pull $MODEL_NAME #-f /tmp/model.yaml

echo "Waiting for ollama pull to finish..."
# Check if model is available by listing models
while ! ollama list | grep -q "$MODEL_NAME"; do
    sleep 1
done

echo "Model setup complete!"

# Keep container running
tail -f /dev/null 