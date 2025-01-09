## Installation

### Prerequisites
1. **Python Version**: Ensure Python 3.8 or higher is installed.
2. **Dependencies**: Install the required libraries:
   ```bash
   pip install streamlit llama-index chromadb
   ```
3. **External Tools**:
   - Install and set up the Ollama LLM server. For macOS:
     ```bash
     brew install ollama
     ```
   - Ensure ChromaDB is running locally or accessible.

### Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

## Usage

### Run the Application
1. Start the application using Streamlit:
   ```bash
   streamlit run app.py
   ```
2. Open the local URL provided in your terminal to access the chat interface.

### Chatting with LLMs
1. Select a model from the sidebar (e.g., `llama3.2`, `phi3`).
2. Enter your query in the chat input field.
3. View the assistant's response and chat history directly in the interface.

### Inspecting ChromaDB
1. Use the **Check ChromaDB** button to view stored documents and metadata.

## Examples

### Example 1: Basic Chat
1. Select `llama3.2` from the sidebar.
2. Enter the query: "What is the capital of France?"
3. The assistant responds: "The capital of France is Paris."
4. The interaction is saved in ChromaDB with metadata.

### Example 2: Inspect ChromaDB
1. After several interactions, click the **Check ChromaDB** button.
2. View stored documents, IDs, and metadata in the Streamlit interface.
