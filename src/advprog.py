import streamlit as st
from llama_index.core.llms import ChatMessage
import logging
import time
from llama_index.llms.ollama import Ollama
from chromadb import Client
from typing import List

logging.basicConfig(level=logging.INFO)

try:
    chromadb_client = Client()
    collection = chromadb_client.get_or_create_collection("chat_responses")
except Exception as e:
    logging.error(f"ChromaDB initialization error: {str(e)}")

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'uploaded_docs' not in st.session_state:
    st.session_state.uploaded_docs = []

def load_constitution():
    try:
        with open("kazakhstan_constitution.txt", "r", encoding="utf-8") as file:
            content = file.read()
            doc_id = "kazakhstan_constitution"
            collection.add(
                ids=[doc_id],
                documents=[content],
                metadatas=[{"filename": "Constitution of Kazakhstan", "timestamp": int(time.time())}]
            )
            logging.info("Constitution loaded into ChromaDB.")
    except FileNotFoundError:
        logging.error("Constitution file not found. Please ensure 'kazakhstan_constitution.txt' is available.")
        st.error("Constitution file not found. Please upload 'kazakhstan_constitution.txt'.")

def process_uploaded_files(files):
    for file in files:
        try:
            file_content = file.read().decode("utf-8")
            doc_id = str(int(time.time()))
            collection.add(
                ids=[doc_id],
                documents=[file_content],
                metadatas=[{"filename": file.name, "timestamp": int(time.time())}]
            )
            st.session_state.uploaded_docs.append({"filename": file.name, "content": file_content})
            logging.info(f"File uploaded and added to ChromaDB: {file.name}")
        except Exception as e:
            logging.error(f"Error processing file {file.name}: {str(e)}")
            st.error(f"Error processing file {file.name}: {str(e)}")

def get_relevant_context(query: str, top_k: int = 3) -> List[str]:
    try:
        results = collection.query(query_texts=[query], n_results=top_k)
        return results["documents"]
    except Exception as e:
        logging.error(f"Error querying ChromaDB: {str(e)}")
        return []

def stream_chat_with_context(model, messages, context):
    try:
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
    except Exception as e:
        logging.error(f"Error during streaming: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"

def main():
    st.title("Chat with the Constitution of Kazakhstan")
    logging.info("App started")

    load_constitution()

    model = st.sidebar.selectbox("Choose a model", ["llama3.2", "llama3.1 8b", "phi3", "mistral"])
    logging.info(f"Model selected: {model}")

    st.sidebar.subheader("Upload Additional Documents")
    uploaded_files = st.sidebar.file_uploader("Upload .txt files", type=["txt"], accept_multiple_files=True)
    if st.sidebar.button("Process Files"):
        process_uploaded_files(uploaded_files)

    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        logging.info(f"User input: {prompt}")

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                st.spinner("Generating response...")
                start_time = time.time()

                try:
                    context = get_relevant_context(prompt)
                    messages = [ChatMessage(role=msg["role"], content=msg["content"]) for msg in st.session_state.messages]
                    response_message = stream_chat_with_context(model, messages, context)
                    duration = time.time() - start_time

                    response_message_with_duration = f"{response_message}\n\nDuration: {duration:.2f} seconds"
                    st.session_state.messages.append({"role": "assistant", "content": response_message_with_duration})

                    st.write(response_message_with_duration)
                    logging.info(f"Response: {response_message}, Duration: {duration:.2f} s")

                    collection.add(
                        ids=[str(int(time.time()))],
                        documents=[response_message],
                        metadatas=[{"role": "assistant", "timestamp": int(time.time())}]
                    )
                except Exception as e:
                    error_msg = f"An error occurred: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.error(error_msg)
                    logging.error(error_msg)

if __name__ == "__main__":
    main()
