# 📄 Documentation Technique - MusicBot RAG

## 1. Introduction

MusicBot est un système intelligent de question-réponse basé sur la technique **RAG (Retrieval-Augmented Generation)**. Il combine une base de connaissances locale sur la musique avec un modèle de langage (LLM) pour générer des réponses précises et contextualisées.

---

## 2. Architecture Globale du Système

```
┌─────────────────────────────────────────────────────────┐
│                    INTERFACE UTILISATEUR                 │
│                      (Gradio Chat)                       │
└─────────────────────────┬───────────────────────────────┘
                          │ Question
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   PIPELINE RAG                           │
│                                                          │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────┐  │
│  │  Embedding  │───▶│  ChromaDB    │───▶│  Retriever │  │
│  │  Question   │    │  Recherche   │    │  Top-3     │  │
│  └─────────────┘    └──────────────┘    └─────┬──────┘  │
│                                               │          │
│  ┌─────────────────────────────────────────── ▼──────┐  │
│  │              Construction du Prompt               │  │
│  │         Contexte (chunks) + Question              │  │
│  └───────────────────────────┬───────────────────────┘  │
│                              │                           │
│                              ▼                           │
│                    ┌─────────────────┐                   │
│                    │   LLM (Groq)    │                   │
│                    │   LLaMA3-8B     │                   │
│                    └────────┬────────┘                   │
└─────────────────────────────┼───────────────────────────┘
                              │ Réponse
                              ▼
                    ┌─────────────────┐
                    │   Utilisateur   │
                    └─────────────────┘
```

---

## 3. Explication Technique de Chaque Étape

### 3.1 Chargement des Documents
```python
loader = DirectoryLoader(
    "documents/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}
)
documents = loader.load()
```
**Explication :** Le `DirectoryLoader` parcourt le dossier `documents/` et charge tous les fichiers `.txt`. Chaque fichier devient un objet `Document` contenant le texte et des métadonnées (nom du fichier, chemin...).

---

### 3.2 Découpage en Chunks (Chunking)
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_documents(documents)
```
**Explication :** Les documents sont découpés en morceaux de **500 caractères** avec un **chevauchement de 50 caractères**. Le chevauchement permet de ne pas perdre le contexte entre deux chunks consécutifs.

**Pourquoi 500 caractères ?** C'est un bon compromis entre :
- Trop petit → perd le contexte
- Trop grand → dépasse la fenêtre du LLM

---

### 3.3 Génération des Embeddings
```python
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
```
**Explication :** Chaque chunk de texte est transformé en un **vecteur numérique** de 384 dimensions. Ces vecteurs capturent le sens sémantique du texte. Le modèle `all-MiniLM-L6-v2` est léger, rapide et efficace.

**Principe :** Deux textes avec un sens similaire auront des vecteurs proches dans l'espace vectoriel.

---

### 3.4 Stockage dans ChromaDB
```python
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```
**Explication :** ChromaDB est une **base de données vectorielle** qui stocke les embeddings des chunks. Elle permet de faire des recherches de similarité très rapidement. Le paramètre `persist_directory` sauvegarde la base sur le disque.

---

### 3.5 Recherche Sémantique
```python
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```
**Explication :** Quand l'utilisateur pose une question, elle est transformée en vecteur, puis ChromaDB trouve les **3 chunks les plus proches** (k=3) par similarité cosinus. Ces chunks constituent le contexte pertinent.

---

### 3.6 Configuration du LLM
```python
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama3-8b-8192",
    temperature=0.7
)
```
**Explication :** On utilise le modèle **LLaMA3-8B** via l'API Groq. 
- `temperature=0.7` : contrôle la créativité des réponses (0=strict, 1=créatif)
- `8192` : taille de la fenêtre de contexte en tokens

---

### 3.7 Construction du Prompt
```python
prompt = PromptTemplate.from_template("""
Tu es MusicBot, un assistant spécialisé dans la musique.
Utilise uniquement le contexte fourni pour répondre.
Contexte : {context}
Question : {question}
Réponse :
""")
```
**Explication :** Le prompt est un template qui combine le **contexte** (chunks récupérés) et la **question** de l'utilisateur. Il donne aussi des instructions au LLM sur comment répondre.

---

### 3.8 Chaîne RAG (LCEL)
```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```
**Explication :** C'est la chaîne principale qui connecte toutes les étapes :
1. `retriever` → récupère les chunks pertinents
2. `format_docs` → formate les chunks en texte
3. `prompt` → construit le prompt final
4. `llm` → génère la réponse
5. `StrOutputParser` → extrait le texte de la réponse

---

## 4. Technologies et Justifications

| Technologie | Version | Justification |
|---|---|---|
| **Python** | 3.14 | Langage standard pour l'IA |
| **LangChain** | 1.3+ | Framework RAG le plus populaire |
| **Groq** | Latest | API gratuite, ultra-rapide (300 tokens/sec) |
| **LLaMA3-8B** | 8192 ctx | Modèle open-source performant |
| **ChromaDB** | 1.5+ | Base vectorielle légère et simple |
| **HuggingFace** | all-MiniLM-L6-v2 | Modèle d'embedding léger et efficace |
| **Gradio** | 6.0+ | Interface chat simple et rapide |

---

## 5. Base de Connaissances

| Fichier | Contenu | Taille |
|---|---|---|
| `histoire_musique.txt` | Histoire de la musique de l'Antiquité à nos jours | ~4.4 KB |
| `genres_musicaux.txt` | Jazz, Blues, Rock, Pop, Hip-Hop, Électronique... | ~4.7 KB |
| `artistes_celebres.txt` | Michael Jackson, Beatles, Mozart, Beyoncé... | ~5.0 KB |
| `musique_arabe.txt` | Oum Kalthoum, Raï, Musique Tunisienne... | ~4.6 KB |

---

## 6. Limites du Système

| Limite | Description |
|---|---|
| **Base de connaissances fixe** | Le système ne peut répondre que sur les documents fournis |
| **Pas de mémoire conversationnelle** | Chaque question est traitée indépendamment |
| **Chunking fixe** | La taille des chunks est fixe, pas adaptative |
| **Langue** | Optimisé pour le français uniquement |
| **Dépendance API** | Nécessite une connexion internet pour Groq |

---

## 7. Améliorations Futures

| Amélioration | Description | Complexité |
|---|---|---|
| **Mémoire conversationnelle** | Garder l'historique de la conversation | Moyenne |
| **Chunking dynamique** | Adapter la taille des chunks au contenu | Moyenne |
| **Recherche hybride** | Combiner recherche vectorielle + mots-clés | Haute |
| **Upload de documents** | Permettre à l'utilisateur d'ajouter ses propres documents | Moyenne |
| **Citations de sources** | Afficher la source de chaque réponse | Faible |
| **Support multilingue** | Répondre en arabe et en anglais | Moyenne |

---

## 8. Glossaire

| Terme | Définition |
|---|---|
| **RAG** | Retrieval-Augmented Generation : technique qui enrichit le LLM avec des documents externes |
| **LLM** | Large Language Model : modèle de langage de grande taille |
| **Embedding** | Représentation vectorielle numérique d'un texte |
| **Chunk** | Morceau de texte découpé depuis un document |
| **ChromaDB** | Base de données vectorielle open-source |
| **Token** | Unité de base du texte pour les LLMs (~0.75 mot) |
| **Temperature** | Paramètre contrôlant la créativité du LLM |
| **Retriever** | Composant qui récupère les documents pertinents |
