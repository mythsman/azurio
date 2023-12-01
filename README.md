# Azurio
Azurio is a state-of-the-art, self-hosted web server that utilizes Gradio to facilitate access to Azure AI features. It seamlessly integrates powerful technologies such as GPT-4 and Text-to-Speech (TTS), offering a platform that is both professional and user-friendly for AI-driven applications.

# Setup Instructions
## Running from Source
When setting up Azurio to run from source code, an .env file is required for environment configuration.

### Environment Variables for Source Deployment
Create a .env file in the root directory and input the following details with your Azure service credentials and Gradio configurations:

```
AZURE_SPEECH_KEY=your_azure_speech_key_here
AZURE_SPEECH_ENDPOINT=your_azure_speech_endpoint_here
AZURE_GPT_KEY=your_azure_openai_key_here
AZURE_GPT_ENDPOINT=your_azure_openai_endpoint_here
GRADIO_AUTH_LIST=user1:password1;user2:password2
GRADIO_SERVER_NAME=0.0.0.0
GRADIO_SERVER_PORT=8888
```

Be sure to replace the placeholder text with your actual Azure API keys and endpoints, as well as Gradio user credentials.

### Launching the Server from Source
Once the .env file is configured, follow these steps:

1. Clone the repository.
2. Install the dependencies with the command:
```
pip install -r requirements.txt
```
3. Start the server:
```
python webui.py
```
## Docker Deployment
Deploying Azurio using Docker does not require the creation of an .env file since the environment variables are defined within the docker-compose.yml file.

### Docker Compose Configuration
Edit the docker-compose.yml file to include your specific Azure credentials and Gradio settings:

```yaml
version: "3.8"
services:
  azurio:
    image: mythsman/azurio
    container_name: azurio
    restart: always
    environment:
      AZURE_SPEECH_KEY: your_azure_speech_key_here
      AZURE_SPEECH_ENDPOINT: your_azure_speech_endpoint_here
      AZURE_GPT_KEY: your_azure_openai_key_here
      AZURE_GPT_ENDPOINT: your_azure_openai_endpoint_here
      GRADIO_AUTH_LIST: user1:password1;user2:password2
      GRADIO_SERVER_NAME: 0.0.0.0
      GRADIO_SERVER_PORT: 8888
    ports:
      - "8888:8888"
```

Replace the placeholders with your actual Azure Speech and OpenAI keys and endpoints, as well as the Gradio authentication details.

### Starting Azurio with Docker
To deploy Azurio using Docker, run:

```
docker-compose up -d
```

Azurio will now be running and accessible on the specified port, offering a secure and personalized environment for your Azure AI solutions.
