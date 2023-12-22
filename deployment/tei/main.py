from langchain.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.vectorstores.docarray import DocArrayInMemorySearch
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# Specify your service url
EMBEDDINGS_URL = "https://tasty-mole-1.examples.cloud.dstack.ai"

embedding=HuggingFaceInferenceAPIEmbeddings(
    api_url=EMBEDDINGS_URL,
    api_key="", # No api key required
)
texts = [
    "The earliest known name for Great Britain is Albion (Greek: Ἀλβιών) or insula Albionum",
    "Human footprints have been found from over 800,000 years ago in Norfolk.",
    # ...
]
vectorstore = DocArrayInMemorySearch.from_texts(texts, embedding)
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
setup_and_retrieval = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
)
print(setup_and_retrieval.invoke("How was Great Britain called before?"))
# {
#     'context':[Document(page_content='The earliest known name for Great Britain is Albion (Greek: Ἀλβιών) or insula Albionum')],
#     'question': 'How was Great Britain called before?'
# }

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.llms.huggingface_text_gen_inference import (
    HuggingFaceTextGenInference
)

# Specify your service url
INFERENCE_URL = "https://shy-elephant-1.examples.cloud.dstack.ai"

template = """
<s>[INST] Answer the question using the following context:
{context}

Question: {question} [/INST]
"""
prompt = PromptTemplate.from_template(template)
model = HuggingFaceTextGenInference(
    inference_server_url=INFERENCE_URL,
    max_new_tokens=500,
)
output_parser = StrOutputParser()

chain = setup_and_retrieval | prompt | model | output_parser

print(chain.invoke("How was Great Britain called before?"))
# Before its modern name, Great Britain was known as Albion.
# This name is derived from the Latin term 'insula Albionum'.