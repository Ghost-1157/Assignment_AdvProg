# Chat with OpenAI using Streamlit and MongoDB

## Installation

### Prerequisites
1. **Python Version**: Ensure Python 3.8 or higher is installed.
2. **Dependencies**: Install the required libraries:
   ```bash
   pip install streamlit openai pymongo
   ```  
3. **External Tools**:
   - **MongoDB**: Ensure MongoDB is running locally or accessible.

### Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

## Usage

### Run the Application
1. Start the application using Streamlit:
   ```bash
   streamlit run advprog.py
   ```
2. Open the local URL provided in your terminal to access the chat interface.

### Chatting with OpenAI
1. Choose a model (`gpt-4` or `gpt-3.5-turbo`) from the sidebar.
2. Enter your query in the chat input field.
3. View the assistant's response and chat history directly in the interface.

### Storing Queries and Answers
- All user inputs and assistant responses are stored in MongoDB with metadata, including the timestamp and model used.

### Inspecting MongoDB
1. Use the **Check MongoDB** button to view stored documents and metadata.
2. Each document contains the query, assistant response, model information, and a timestamp.

## Examples

### Example 1: Basic Chat
1. Select `gpt-4` from the sidebar.
2. Enter the query: "What is the capital of Kazakhstan?"
3. The assistant responds: "Astana."
4. The interaction is saved in MongoDB with metadata.

### Example 2: Inspect MongoDB
1. After several interactions, click the **Check MongoDB** button.
2. View stored documents, IDs, and metadata in the Streamlit interface.

## Additional Notes
- Ensure MongoDB is running locally before starting the application.
- Replace `"YOUR_OPENAI_API_KEY"` in the code with your actual OpenAI API key.
