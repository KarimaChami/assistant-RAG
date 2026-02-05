# rag_utils.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnablePassthrough
from pathlib import Path
import os
import time

# ---- Charger le PDF ----
PDF_PATH = Path("src/data/support_it.pdf")
loader = PyPDFLoader(str(PDF_PATH))
pages = loader.load()

decouper = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50) 
chunks = decouper.split_documents(pages)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
vectorstore.persist()

# ---- LLM ----
os.environ["GOOGLE_API_KEY"] = "AIzaSyDvDCzHytYkueDpUln-xfy4Xib56n8o5QY"
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

prompt_template = ChatPromptTemplate.from_template("""
Tu es un assistant IT.
Réponds UNIQUEMENT à partir du contexte fourni.

Contexte :
{context}

Question :
{question}
""")

def ask_rag(question: str):
    start_time = time.time()

    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)

    messages = prompt_template.format_messages(
        context=context,
        question=question
    )

    response = llm.invoke(messages)

    latency_ms = (time.time() - start_time) * 1000
    return response.content, latency_ms
