Features:

Interactive Chat Interface:

Users can ask questions and receive answers from selected LLMs.
Supports multiple models: llama3.2, llama3.1 8b, phi3, mistral.

ChromaDB Integration:

Stores all user queries and responses from the assistant in a vector database for efficient retrieval and storage.
Model Selection:

Offers the ability to choose from different LLMs for interaction.

Logging:

Detailed logging of user inputs, model responses, and errors for debugging and monitoring.

Database Inspection:

A button allows users to inspect documents stored in ChromaDB.

Installation:

Clone this repository:
git clone <repository-url>
cd <repository-name>

Install the required dependencies:
pip install streamlit llama-index chromadb
Ensure your environment is configured with any necessary API keys or access credentials.

Usage:

Run the application:
streamlit run app.py
Open the application in your web browser at the provided local URL.

Select a model from the sidebar and start chatting.

Use the "Check ChromaDB" button to view stored interactions.

Code Explanation:

Modules and Initialization:

Streamlit: Used for the web interface and managing session state.
LlamaIndex: Manages message formatting for LLM interactions.
ChromaDB: Stores user queries and responses for efficient retrieval.

Key Functions:

stream_chat: Handles streaming responses from the selected LLM.
add_to_chroma_db: Adds user inputs and model responses to the ChromaDB collection.
main: Orchestrates the chat interface, user input handling, and model responses.

ChromaDB Management:

A collection named chat_responses is used to store all chat interactions.
Each entry contains metadata, including the model name, role (user or assistant), and timestamps.

Logging:

Logs all key actions, including user queries, responses, and any errors, to assist in debugging.

Debugging:

If ChromaDB is not functioning, check the logs for errors.
Ensure the ChromaDB client is correctly configured and running.

Future Improvements:

Add support for additional models.
Enhance UI for better user experience.
Implement advanced retrieval techniques from ChromaDB.
