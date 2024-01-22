import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import Replicate
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import TextLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from gtts import gTTS
import pygame
import os
from dotenv import load_dotenv
import tempfile
import uuid
import pandas as pd
load_dotenv()

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

def conversation_chat(query, chain, history):
    result = chain({"question": query, "chat_history": history})
    history.append((query, result["answer"]))
    return result["answer"]

def display_chat_history(chain, user_input):
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            with st.spinner('Generating response...'):
                output = conversation_chat(user_input, chain, st.session_state['history'])

            st.session_state['past'].append(user_input)

            if isinstance(output, dict):
                answer = output.get("answer", "")
            else:
                answer = output

            st.session_state['generated'].append(answer)

            # Call text_to_speech function here
            text_to_speech(answer)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['past'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="fun-emoji")
                message(st.session_state["generated"][i], key=str(i), avatar_style="fun-emoji")

                # Call text_to_speech function here
                # text_to_speech(st.session_state["generated"][i])

def create_conversational_chain(vector_store):
    load_dotenv()
    llm = Replicate(
        streaming=True,
        model="replicate/llama-2-70b-chat:58d078176e02c219e11eb4da5a02a7830a283b14cf8f94537af893ccff5ee781",
        callbacks=[StreamingStdOutCallbackHandler()],
        input={"temperature": 0.01, "max_length": 500, "top_p": 1})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff',
                                                 retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
                                                 memory=memory)
    return chain

def text_to_speech(text):
    # Generate a unique file name
    unique_filename = str(uuid.uuid4()) + ".mp3"
    file_path = os.path.join(tempfile.gettempdir(), unique_filename)

    tts = gTTS(text=text, lang='en')
    tts.save(file_path)

    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
def main():
    load_dotenv()

    initialize_session_state()

    st.title("CHaNAKiA")

    st.sidebar.title("Document Processing")
    uploaded_files = st.sidebar.file_uploader("Upload files", accept_multiple_files=True)

    if uploaded_files:
        text = []
        for file in uploaded_files:
            file_extension = os.path.splitext(file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file.read())
                temp_file_path = temp_file.name

            loader = None
            if file_extension == ".pdf":
                loader = PyPDFLoader(temp_file_path)
            elif file_extension == ".docx" or file_extension == ".doc":
                loader = Docx2txtLoader(temp_file_path)
            elif file_extension == ".csv":
                loader = TextLoader(temp_file_path)

            if loader:
                text.extend(loader.load())

                os.remove(temp_file_path)

        text_splitter = CharacterTextSplitter(separator="\n", chunk_size=4000, chunk_overlap=100, length_function=len)
        text_chunks = text_splitter.split_documents(text)

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                           model_kwargs={'device': 'cpu'})

        vector_store = FAISS.from_documents(text_chunks, embedding=embeddings)

        chain = create_conversational_chain(vector_store)

        template = """Question: {question}
         make it precise 1 sentence long only and in english as well as hindi .
        Answer:"""
        prompt = PromptTemplate(template=template, input_variables=["question"])

        user_input = st.text_input("What's your question?")
        formatted_prompt = prompt.format(question=user_input)

        display_chat_history(chain, user_input)

if __name__ == "__main__":
    main()
