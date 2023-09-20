import os
import weaviate
from langchain import HuggingFaceTextGenInference
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index import (
    LangchainEmbedding,
    PromptHelper,
    QuestionAnswerPrompt,
    RefinePrompt,
    ServiceContext,
    VectorStoreIndex,
)
from llama_index.llm_predictor import LLMPredictor
from llama_index.vector_stores import WeaviateVectorStore
from llama_index.callbacks import CallbackManager, LlamaDebugHandler

if __name__ == "__main__":
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

    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    callback_manager = CallbackManager([llama_debug])

    service_context = ServiceContext.from_defaults(
        embed_model=embed_model,
        llm_predictor=llm_predictor,
        prompt_helper=PromptHelper(context_window=1024),
        callback_manager=callback_manager,
    )

    vector_store = WeaviateVectorStore(
        weaviate_client=client, index_name="DstackExample"
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store, service_context=service_context
    )

    text_qa_template = QuestionAnswerPrompt(
        """<s>[INST] <<SYS>>
We have provided context information below. 

{context_str}

Given this information, please answer the question.
<</SYS>>

{query_str} [/INST]"""
    )

    refine_template = RefinePrompt(
        """<s>[INST] <<SYS>>
The original query is as follows: 

{query_str}

We have provided an existing answer:

{existing_answer}

We have the opportunity to refine the existing answer (only if needed) with some more context below.

{context_msg}
<</SYS>>

Given the new context, refine the original answer to better answer the query. If the context isn't useful, return the original answer. [/INST]"""
    )

    query_engine = index.as_query_engine(
        text_qa_template=text_qa_template,
        refine_template=refine_template,
        streaming=True,
    )

    response = query_engine.query(
        "Make a bullet-point timeline of the authors biography."
    )
    response.print_response_stream()
    print(f"\n\nSources:\n\n{response.get_formatted_sources()}")
