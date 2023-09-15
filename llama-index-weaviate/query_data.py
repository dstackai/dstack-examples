import os
import weaviate
from langchain import HuggingFaceTextGenInference
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import (
    LangchainEmbedding,
    QuestionAnswerPrompt,
    ServiceContext,
    VectorStoreIndex,
)
from llama_index.llm_predictor import LLMPredictor
from llama_index.vector_stores import WeaviateVectorStore

weaviate_api_key = os.getenv("WEAVIATE_API_TOKEN")
weaviate_url = os.getenv("WEAVIATE_URL")
tgi_endpoint_url = os.getenv("TGI_ENDPOINT_URL")

if not weaviate_api_key or not weaviate_url or not tgi_endpoint_url:
    exit(
        "Make sure you've set WEAVIATE_API_TOKEN, WEAVIATE_URL, and TGI_ENDPOINT_URL environment variables"
    )

auth_config = weaviate.AuthApiKey(api_key=weaviate_api_key)

client = weaviate.Client(
    url=weaviate_url,
    auth_client_secret=auth_config,
)

embed_model = LangchainEmbedding(HuggingFaceEmbeddings())

llm_predictor = LLMPredictor(
    llm=HuggingFaceTextGenInference(
        inference_server_url=tgi_endpoint_url,
        max_new_tokens=512,
        streaming=True,
    ),
)

service_context = ServiceContext.from_defaults(
    embed_model=embed_model,
    llm_predictor=llm_predictor,
)

vector_store = WeaviateVectorStore(
    weaviate_client=client, index_name="llama-index-weaviate"
)

index = VectorStoreIndex.from_vector_store(
    vector_store, service_context=service_context
)

prompt = QuestionAnswerPrompt(
    """<s>[INST] <<SYS>>
We have provided context information below. 

{context_str}

Given this information, please answer the question.
<</SYS>>

[/INST]</s>
<s>[INST]{query_str}[/INST]"""
)
query_engine = index.as_query_engine(
    text_qa_template=prompt,
    streaming=True,
)

response = query_engine.query("What did the author do growing up?")
response.print_response_stream()
print(f"\n\nSources:\n\n{response.get_formatted_sources()}")
