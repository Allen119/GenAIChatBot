# 📝 NoteBot – Your PDF Tutor Bot

**NoteBot** is a smart assistant that lets you:

✅ Upload a PDF  
✅ Ask questions about it  
✅ Get clear answers using **local AI** (no OpenAI keys required!)

It uses **LangChain with Ollama (LLaMA3)** to understand your questions and extract answers from the uploaded PDF.

---

## 🛠️ Tech Stack & Tools Used

| Tool/Library                        | Purpose                                      |
|------------------------------------|----------------------------------------------|
| Streamlit                          | Web-based UI                                 |
| PyPDF2                             | Extracts text from PDF                       |
| LangChain                          | Manages LLM prompting and chaining           |
| HuggingFace Embeddings             | Converts text into numerical vectors         |
| FAISS                              | Finds similar text using vector search       |
| Ollama (with LLaMA3 model)         | Local AI model for question answering        |
| RecursiveCharacterTextSplitter     | Breaks text into manageable chunks           |

---

## 🧠 How It Works – Step-by-Step

> This process is the same in both the `master` and `static` branches (except for the assistant's tone, explained below).

### 🔹 1. Upload a PDF
- Upload a `.pdf` file via Streamlit sidebar.  
- PyPDF2 reads and extracts text from each page.  
- All text is combined into a single string.

### 🔹 2. Split the PDF into Chunks
- Long text is split into smaller parts using: python
RecursiveCharacterTextSplitter(
    chunk_size=200, 
    chunk_overlap=50
)

    Overlap ensures context is preserved between chunks.

🔹 3. Embed Text (Convert to Vectors)

    Each chunk is converted into vectors using HuggingFace:

    model = "sentence-transformers/all-MiniLM-L6-v2"

    These embeddings capture the semantic meaning of the text.

🔹 4. Store in Vector Database

    Vectors are stored in FAISS for fast semantic search.

🔹 5. Ask a Question

    User asks a natural-language question (e.g., "What is the main idea of Chapter 3?").

    The app retrieves most relevant chunks using vector similarity.

🔹 6. Get Answer from Local LLM

    Instead of OpenAI, the project uses Ollama with LLaMA3:

    Ollama(model="llama3")

    LangChain sends both context and the question to the LLM using a custom prompt.

🔹 7. Answer Appears!

    AI generates a response based on PDF context.

    If unsure, behavior depends on the branch:
    
## 🌿 Branch Differences: `master` vs `static`

| Feature                | `master` Branch                        | `static` Branch                           |
|------------------------|----------------------------------------|-------------------------------------------|
| 🤖 Assistant Tone      | Acts as a **polite tutor**, honest     | Acts like a **general helpful assistant** |
| 📜 Prompt Behavior     | Says “I don’t know Jenny” if unsure    | Tries to answer using model's own knowledge |
| 💬 Prompt Template     | Encourages honesty                     | Encourages helpfulness                    |
| 🔄 Other Code Diff     | None                                   | None                                      |
