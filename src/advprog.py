import streamlit as st
from llama_index.core.llms import ChatMessage
from llama_index.llms.ollama import Ollama
from pymongo import MongoClient
import logging
import time
from typing import List

logging.basicConfig(level=logging.INFO)

# MongoDB connection
try:
    client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
    db = client["chat_database"]
    collection = db["chat_responses"]
except Exception as e:
    logging.error(f"MongoDB initialization error: {str(e)}")

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'uploaded_docs' not in st.session_state:
    st.session_state.uploaded_docs = []

def generate_multi_queries(prompt: str, model: str, n_queries: int = 3) -> List[str]:
    llm = Ollama(model=model, request_timeout=60.0)
    multi_queries = []
    for i in range(n_queries):
        response = llm.chat([ChatMessage(role="system", content=f"Generate query variation {i+1} for: {prompt}")])
        multi_queries.append(response.message)
    logging.info(f"Generated multi-queries: {multi_queries}")
    return multi_queries

def get_relevant_context_multi(queries: List[str], top_k: int = 3) -> List[str]:
    all_contexts = []
    for query in queries:
        results = collection.find({"$text": {"$search": query}}).limit(top_k)
        for result in results:
            all_contexts.append(result["document"])
    return list(set(all_contexts))

def stream_chat_with_context(model, messages, context):
    llm = Ollama(model=model, request_timeout=120.0)
    if context:
        context_message = "\n\n".join(context)
        messages.append(ChatMessage(role="system", content=f"Context: {context_message}"))
    resp = llm.stream_chat(messages)
    response = ""
    for r in resp:
        response += r.delta
    logging.info(f"Model: {model}, Messages: {messages}, Response: {response}")
    return response

def main():
    st.title("Chat with RAG and Multi-Query Support using MongoDB")
    logging.info("App started")

    model = st.sidebar.selectbox("Choose a model", ["llama3.2", "llama3.1 8b", "phi3", "mistral"])

    st.sidebar.subheader("Upload Additional Documents")
    uploaded_files = st.sidebar.file_uploader("Upload .txt files", type=["txt"], accept_multiple_files=True)
    if st.sidebar.button("Process Files"):
        for file in uploaded_files:
            file_content = file.read().decode("utf-8")
            doc_id = str(int(time.time()))
            collection.insert_one({
                "_id": doc_id,
                "document": file_content,
                "filename": file.name,
                "timestamp": int(time.time())
            })
            st.session_state.uploaded_docs.append({"filename": file.name, "content": file_content})
            logging.info(f"File uploaded and added to MongoDB: {file.name}")

    st.sidebar.subheader("Query History")
    if st.sidebar.button("Load History"):
        try:
            results = collection.find().sort("timestamp", -1).limit(20)
            for i, result in enumerate(results):
                query_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(result['timestamp']))
                st.sidebar.write(f"{i+1}. [{query_time}] {result.get('role', 'Query')}: {result['document']}")
        except Exception as e:
            st.sidebar.error(f"Error loading history: {str(e)}")

    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                st.spinner("Generating response...")
                start_time = time.time()

                try:
                    multi_queries = generate_multi_queries(prompt, model)
                    context = get_relevant_context_multi(multi_queries)
                    messages = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in st.session_state.messages]
                    response_message = stream_chat_with_context(model, messages, context)
                    duration = time.time() - start_time

                    response_message_with_duration = f"{response_message}\n\nDuration: {duration:.2f} seconds"
                    st.session_state.messages.append({"role": "assistant", "content": response_message_with_duration})

                    st.write(response_message_with_duration)
                    logging.info(f"Response: {response_message}, Duration: {duration:.2f} s")

                    collection.insert_one({
                        "document": response_message,
                        "role": "assistant",
                        "timestamp": int(time.time())
                    })
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.error(error_msg)
                    logging.error(error_msg)

if __name__ == "__main__":
    main()
