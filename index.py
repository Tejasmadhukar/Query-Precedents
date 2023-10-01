from flask import Flask, request, jsonify
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores import FaissVectorStore
from llama_index.storage.index_store import SimpleIndexStore
from llama_index import load_index_from_storage
from llama_index.storage.storage_context import StorageContext
from llama_index.query_engine import CitationQueryEngine
import openai
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

storage_context = StorageContext.from_defaults(docstore=SimpleDocumentStore.from_persist_dir(persist_dir="persist_new"),
                                              vector_store=FaissVectorStore.from_persist_dir(persist_dir="persist_new"),
                                              index_store=SimpleIndexStore.from_persist_dir(persist_dir="persist_new"))
index = load_index_from_storage(storage_context=storage_context)
query_engine = CitationQueryEngine.from_args(index, similarity_top_k=3, citation_chunk_size=1024)

@app.route('/')
def home():
    return 'Api is Healthy'

@app.route("/query", methods=["POST"])
def run():
    query = request.json.get("query")
    database_answer = query_engine.query(query)
    
    response = {'query_result': database_answer.response, 'case_name': [], 'source_text': []}
    
    for i in range(len(database_answer.source_nodes)):
        response['case_name'].append(database_answer.source_nodes[i].node.extra_info["file_name"])
        response['source_text'].append(database_answer.source_nodes[i].node.get_text())
        
    return jsonify(response)


if __name__ == "__main__":
    p = int(os.getenv('PORT'))
    app.run(host='0.0.0.0', port=p)