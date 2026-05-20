# ============================================
# MusicBot - Chatbot RAG sur la Musique
# Réalisé avec LangChain + Groq + ChromaDB
# ============================================

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import gradio as gr

# ============================================
# ÉTAPE 1 : Chargement de la clé API
# ============================================
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ============================================
# ÉTAPE 2 : Chargement des documents
# ============================================
print("📂 Chargement des documents...")
loader = DirectoryLoader(
    "documents/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)
documents = loader.load()
print(f"✅ {len(documents)} documents chargés !")

# ============================================
# ÉTAPE 3 : Découpage en chunks
# ============================================
print("✂️ Découpage des documents en chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)
print(f"✅ {len(chunks)} chunks créés !")

# ============================================
# ÉTAPE 4 : Génération des embeddings
# ============================================
print("🧠 Génération des embeddings...")
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# ============================================
# ÉTAPE 5 : Stockage dans ChromaDB
# ============================================
print("💾 Stockage dans la base vectorielle ChromaDB...")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
print("✅ Base vectorielle créée !")

# ============================================
# ÉTAPE 6 : Configuration du LLM (Groq)
# ============================================
print("🤖 Configuration du modèle LLM...")
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192",
    temperature=0.7
)

# ============================================
# ÉTAPE 7 : Création du prompt personnalisé
# ============================================
prompt_template = """
Tu es MusicBot, un assistant intelligent spécialisé dans la musique.
Utilise uniquement le contexte fourni pour répondre à la question.
Si tu ne trouves pas la réponse dans le contexte, dis-le poliment.
Réponds toujours en français de manière claire et détaillée.

Contexte : {context}

Question : {question}

Réponse :
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)

# ============================================
# ÉTAPE 8 : Création de la chaîne RAG
# ============================================
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
)

# ============================================
# ÉTAPE 9 : Interface Gradio
# ============================================
def respond(message, history):
    response = qa_chain.invoke({"query": message})
    return response["result"]

demo = gr.ChatInterface(
    fn=respond,
    title="🎵 MusicBot - Assistant Musical Intelligent",
    description="Posez vos questions sur la musique : histoire, genres, artistes et bien plus !",
    examples=[
        "Qui est Michael Jackson ?",
        "Quelle est l'histoire du Jazz ?",
        "Parle moi d'Oum Kalthoum",
        "Quels sont les genres musicaux ?",
        "Qui sont les Beatles ?"
    ],
    theme=gr.themes.Soft()
)

if __name__ == "__main__":
    print("🚀 Lancement de MusicBot...")
    demo.launch()