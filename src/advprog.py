import streamlit as st
import openai
import logging
import time
from pymongo import MongoClient

# Logging setup
logging.basicConfig(level=logging.INFO)

# MongoDB initialization
try:
    mongo_client = MongoClient("mongodb://localhost:27017/")
    db = mongo_client["chat_database"]
    collection = db["chat_responses"]
except Exception as e:
    logging.error(f"MongoDB initialization error: {str(e)}")

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to interact with OpenAI
def chat_with_openai(messages, model="gpt-4"):
    try:
        openai.api_key = "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"
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {"role": "user", "content": "Tell me what is the country of Kazakhstan?"}
    ]
)

        response_text = response.choices[0].message['content']
        logging.info(f"Response from OpenAI: {response_text}")
        return response_text
    except Exception as e:
        logging.error(f"Error during OpenAI chat: {str(e)}")
        return "An error occurred while generating the response."

# MongoDB add function
def add_to_mongo_db(model, message):
    try:
        document = {
            "model": model,
            "role": message["role"],
            "content": message["content"],
            "timestamp": int(time.time())
        }
        collection.insert_one(document)
        logging.info(f"Document added to MongoDB: {message}")
    except Exception as e:
        logging.error(f"Error adding to MongoDB: {str(e)}")

# Main Streamlit app
def main():
    st.title("Ask about Kazakhstan's constitution")
    logging.info("App started")

    # Model choice
    model = st.sidebar.selectbox("Choose a model", ["gpt-4", "gpt-3.5-turbo"])
    logging.info(f"Model selected: {model}")

    # Chat input
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        logging.info(f"User input: {prompt}")

        # Display messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Generate assistant response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                st.spinner("Generating response...")
                start_time = time.time()

                try:
                    formatted_messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
                    response_message = chat_with_openai(formatted_messages, model=model)
                    duration = time.time() - start_time

                    response_message_with_duration = f"{response_message}\n\nDuration: {duration:.2f} seconds"
                    st.session_state.messages.append({"role": "assistant", "content": response_message_with_duration})

                    st.write(response_message_with_duration)
                    logging.info(f"Response: {response_message}, Duration: {duration:.2f} s")

                    add_to_mongo_db(model, {"role": "assistant", "content": response_message_with_duration})
                except Exception as e:
                    error_msg = f"An error occurred while generating the response: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.error(error_msg)
                    logging.error(error_msg)

    # Check MongoDB contents
    if st.button("Check MongoDB"):
        try:
            documents = collection.find()
            st.write("Documents in MongoDB:")
            for doc in documents:
                st.write(f"ID: {doc['_id']}")
                st.write(f"Content: {doc['content']}")
                st.write(f"Metadata: Model: {doc['model']}, Role: {doc['role']}, Timestamp: {doc['timestamp']}")
                st.write("---")
        except Exception as e:
            st.error(f"Error checking MongoDB: {str(e)}")
            logging.error(f"Error checking MongoDB: {str(e)}")

if __name__ == "__main__":
    main()
