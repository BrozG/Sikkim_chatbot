import os
import hashlib
#import Langchain dependencies
from langchain.vectorstores import FAISS
from wxai_langchain.credentials import Credentials
from langchain_community.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

#Bring in streamlit for UI dev
import streamlit as st

#Bring in watsonx interface
from wxai_langchain.llm import LangChainInterface

#Setup crendentials dictionary
creds=Credentials(
    api_key='3JQOZFLpP_zDSAvcpNZNVlEQ4LnQfuIJ3j1nrsihfx8i',
    api_endpoint='https://jp-tok.ml.cloud.ibm.com',
    project_id='2841f6ba-e49e-43b9-a7ad-f749295e28ab'
)

llm =LangChainInterface(
    credentials=creds,
    model='meta-llama/llama-3-3-70b-instruct',
    params={
    'decoding_method':'sample',
    'max_new_tokens':200,
    'temperature':0.2
    },
    
)
#Function to compute hash of the data folder
def get_data_folder_hash():
    data_folder = "data"
    hash_md5 = hashlib.md5()
    for root, _, files in os.walk(data_folder):
        for file in sorted(files):  # Sorting to ensure consistency
            if file.endswith(".pdf"):
                with open(os.path.join(root, file), "rb") as f:
                    while chunk := f.read(8192):
                        hash_md5.update(chunk)
    return hash_md5.hexdigest()

#This function loads a PDF and create vector store
@st.cache_resource
def load_pdf_vectorestore():
    vectorstore_path='vector_store'
    embeddings=HuggingFaceBgeEmbeddings(model_name='all-MiniLM-L12-v2')
    
    #To check if data folder contents have changed (by hash)
    data_folder_hash=get_data_folder_hash()
    if os.path.exists(vectorstore_path):
        saved_hash=open("data_folder_hash.txt","r").read() if os.path.exists("data_folder_hash.txt") else ""
        if saved_hash==data_folder_hash:
            return FAISS.load_local(vectorstore_path,embeddings,allow_dangerous_deserialization=True)
    
    #load pdfs from data folder
    loaders=[PyPDFLoader(os.path.join("data", file)) for file in os.listdir("data") if file.endswith(".pdf")]
    if not loaders:
        st.error("No PDFs found in data folder.")
        return FAISS.from_documents([],embeddings)
    
    #load documents
    documents=[]
    for loader in loaders:
        documents.extend(loader.load())
        
    #Spilt text into chunks
    splitter=RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=0)
    docs=splitter.split_documents(documents)
    
    #Create FAISS vectorstore
    vectorstore=FAISS.from_documents(docs,embeddings)

    #Save to local
    vectorstore.save_local(vectorstore_path)
    
    # Save the new data folder hash to detect future changes
    with open("data_folder_hash.txt", "w") as f:
        f.write(data_folder_hash)
    
    return vectorstore

#load Vectorstore
vectorstore=load_pdf_vectorestore()
    
#Create a Q&A chain
chain =RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=vectorstore.as_retriever(),
    input_key='question'
)
    
#Setup the app title
st.title('ASK KANCHA')

#Setup a session state message variable to hold all the old messages
if'messages' not in st.session_state:
    st.session_state.messages=[]

#Display all the historical messages
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

#Build a prompt input template to display the prompts
prompt =st.chat_input('Pass Your Prompt Here.')

#If the user hits enter then
if prompt:

    #Display the prompt
    st.chat_message('user').markdown(prompt)

    #Store the user prompt in state
    st.session_state.messages.append({'role':'user','content':prompt})

    #Send the prompt to the PDF and Q&A chain
    response=chain.run(prompt)

    #Show the LLM Response
    st.chat_message('assistant').markdown(response)

    #Store the LLM response in state
    st.session_state.messages.append(
        {'role':'assistant','content':response})