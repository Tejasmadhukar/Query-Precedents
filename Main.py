import streamlit as st
import openai
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores import FaissVectorStore
from llama_index.storage.index_store import SimpleIndexStore

from llama_index import load_index_from_storage
from llama_index.storage.storage_context import StorageContext
from llama_index.query_engine import CitationQueryEngine

@st.cache_resource
def preprocess_prelimnary():
    storage_context = StorageContext.from_defaults(docstore = SimpleDocumentStore.from_persist_dir(persist_dir = "persist_new"),
        vector_store = FaissVectorStore.from_persist_dir(persist_dir = "persist_new"),
        index_store = SimpleIndexStore.from_persist_dir(persist_dir = "persist_new"))
    index = load_index_from_storage(storage_context = storage_context)
    query_engine = CitationQueryEngine.from_args(index, similarity_top_k = 3, citation_chunk_size = 1024)
    return query_engine

openai.api_key = st.secrets['OPENAI_API_KEY']

st.set_page_config(layout = 'wide', page_title = 'Precedents Database')

st.title('Query Precedents')

q_e = preprocess_prelimnary()

query = st.text_area(label = 'Enter your query involving Indian Legal Precedents.')
# model = st.selectbox(label = 'Select a model', options = ['gpt-3.5-turbo', 'gpt-4'])

start = st.button(label = 'Start')

base_append = ""

if start:
    st.subheader('Query Response -')
    database_answer = q_e.query(query + base_append)
    st.write(database_answer.response)
    st.subheader('Actual Sources -')
    for i in range(len(database_answer.source_nodes)):
        st.write(database_answer.source_nodes[i].node.get_text())
        st.write(f'Case Name - {database_answer.source_nodes[i].node.extra_info["file_name"]}')