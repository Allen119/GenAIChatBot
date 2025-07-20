import streamlit as st
from PyPDF2 import PdfReader
from langchain.chains.combine_documents import create_stuff_documents_chain
#from langchain.chains.question_answering import load_qa_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama

st.header("NoteBot")

with st.sidebar:
    st.title("My Notes")
    file = st.file_uploader("Upload a file and start asking questions", type="pdf")

if file is not None:
    my_pdf = PdfReader(file)
    text = ""
    for page in my_pdf.pages:
        text += page.extract_text()
        st.write(text)

    splitter = RecursiveCharacterTextSplitter(separators =["\n"], chunk_size=200, chunk_overlap=50)
    chunks = splitter.split_text(text)
    st.write(chunks)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = FAISS.from_texts(chunks,embeddings)

    user_query = st.text_input("Ask a question about the PDF:")
    if user_query is not None:
        matching_chunks = vector_store.similarity_search(user_query)

        llm = Ollama(
            model="llama3",  # or any model you downloaded via `ollama run <model>`
            temperature=0.0,
        )
        # chain = load_qa_chain(llm, chain_type="stuff")
        # output = chain.run(question=user_query, input_documents=matching_chunks)
        # st.write(output)

        customized_prompt = ChatPromptTemplate.from_template(
            """ You are my assistant tutor. Answer the question based on the following context and
            if you did not get the context simply say "I don't know Jenny" :
            {context}
            Question: {input}
            """
        )

        chain = create_stuff_documents_chain(llm, customized_prompt)
        output = chain.invoke({"input": user_query, "context": matching_chunks})
        st.write(output)


