## Installation  

### Prerequisites  
1. **Python Version**: Ensure Python 3.8 or higher is installed.  
2. **Dependencies**: Install the required libraries:  
   ```bash
   pip install streamlit llama-index chromadb pymongo
   ```  
   **Note**: `pymongo` is added for MongoDB support.  
3. **External Tools**:  
   - **Ollama LLM server** (macOS only):  
     ```bash
     brew install ollama
     ```  
   - **MongoDB**: Ensure MongoDB is installed and running on your system. [Download MongoDB](https://www.mongodb.com/try/download/community) if not installed.  

### Clone the Repository  
```bash
git clone <repository-url>
cd <repository-name>
```  

---

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
3. The assistant responds to your query and stores the conversation in MongoDB.  

### Attaching Files and Question Answering  
1. Upload `.txt` files one by one or multiple at once.  
2. Ask questions related to the uploaded documents.  
3. The assistant provides answers within the context of the uploaded documents.  

### Multi-Query and RAG Fusion  
- Multi-query functionality ensures multiple queries are generated for each input, improving response relevance.  
- Retrieval-Augmented Generation (RAG) fusion combines retrieved documents with your query to provide more accurate responses.  

### Inspecting MongoDB  
1. Use the **Check MongoDB** button to view stored documents and metadata.  
2. View query history and assistant responses stored in MongoDB.  

---

## Examples  

### Example 1: Chat and Store in MongoDB  
1. Select `llama3.2` from the sidebar.  
2. Enter the query: "What is the constitution of the Republic of Kazakhstan?"  
3. The assistant responds with an explanation based on the constitution document. (Hopefully)

### Example 2: Inspect MongoDB  
1. After several interactions, click the **Check MongoDB** button.  
2. View stored queries, assistant responses, and metadata in the Streamlit interface.  
