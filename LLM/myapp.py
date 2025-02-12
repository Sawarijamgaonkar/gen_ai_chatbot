import streamlit as st
# from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM

from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import retrieval_qa
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
ollama = OllamaLLM(
    model="llama3.2", 
    params={'decoding_method':'sample',
            'max_new_tokens':200,
            'temprature':0.5
            }
)
st. title('Self care helper')

if'messages' not in st.session_state:
    st.session_state.messages=[]

# displaying the older messages:
for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message)

# if user hits enter then
prompt=st.chat_input('Write your question here')
if prompt:
    # message is displayed:
    st.chat_message('user').markdown(prompt)
    # store user prompts in state:
    st.session_state.messages.append({'role':'user','content':prompt})
    # get response fom llm:
    response=ollama(prompt)
    # show llm response on screen:
    st.chat_message('assistant').markdown(response)
    # store llm responses in state:
    st.session_state.messages.append({'role':'assistant','content':response})


    
