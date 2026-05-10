from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_groq import ChatGroq

from config import GROQ_API_KEY


# --------------------------------------------------
# BUILD VECTOR DATABASE
# --------------------------------------------------

def build_vectorstore(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    docs = splitter.create_documents([text])

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        docs,
        embeddings
    )

    return vectorstore


# --------------------------------------------------
# GENERATE ANSWER
# --------------------------------------------------

def generate_answer(vectorstore, question):

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )

    answer = qa_chain.run(question)

    return answer