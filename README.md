# 🎵 MusicBot - Chatbot RAG Intelligent sur la Musique

![Python](https://img.shields.io/badge/Python-3.14-blue)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)
![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple)
![Gradio](https://img.shields.io/badge/UI-Gradio-yellow)

## 📌 Description

MusicBot est un chatbot intelligent basé sur la technique **RAG (Retrieval-Augmented Generation)**. Il permet de répondre à des questions sur la musique en utilisant une base de connaissances locale composée de documents textuels.

Ce projet a été réalisé dans le cadre du module **IA Générative (LLM)** en utilisant des technologies modernes comme LangChain, Groq, ChromaDB et Gradio.

---

## 🏗️ Architecture RAG

```
Question Utilisateur
        ↓
  [Génération Embedding]
        ↓
  [Recherche Sémantique] ←── ChromaDB (Base Vectorielle)
        ↓
  [Récupération Chunks]
        ↓
  [Construction Prompt]
        ↓
    [LLM Groq]
        ↓
   Réponse Finale
```

---

## 🛠️ Technologies Utilisées

| Technologie | Rôle |
|---|---|
| **Python 3.14** | Langage de programmation |
| **LangChain** | Framework RAG |
| **Groq (LLaMA3)** | Modèle de langage (LLM) |
| **ChromaDB** | Base de données vectorielle |
| **HuggingFace Embeddings** | Génération des embeddings |
| **Gradio** | Interface utilisateur |
| **python-dotenv** | Gestion des variables d'environnement |

---

## 📁 Structure du Projet

```
musicbot-rag/
│
├── documents/                  # Base de connaissances
│   ├── histoire_musique.txt    # Histoire de la musique
│   ├── genres_musicaux.txt     # Les genres musicaux
│   ├── artistes_celebres.txt   # Les artistes célèbres
│   └── musique_arabe.txt       # La musique arabe et orientale
│
├── chroma_db/                  # Base vectorielle (générée automatiquement)
├── app.py                      # Code principal
├── requirements.txt            # Dépendances Python
├── .env                        # Clé API (non inclus dans GitHub)
└── README.md                   # Documentation
```

---

## 🚀 Installation et Lancement

### 1. Cloner le repository
```bash
git clone https://github.com/votre-username/musicbot-rag.git
cd musicbot-rag
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer la clé API
Créer un fichier `.env` :
```
GROQ_API_KEY=votre_clé_groq_ici
```

### 4. Lancer l'application
```bash
python app.py
```

### 5. Ouvrir l'interface
Ouvrir le navigateur sur : `http://localhost:7860`

---

## 💡 Fonctionnalités

- ✅ Chargement automatique des documents TXT
- ✅ Découpage intelligent en chunks (500 tokens, overlap 50)
- ✅ Génération d'embeddings avec HuggingFace
- ✅ Stockage vectoriel avec ChromaDB
- ✅ Recherche sémantique (top 3 chunks)
- ✅ Génération de réponses avec LLaMA3 via Groq
- ✅ Interface chat interactive avec Gradio
- ✅ Questions pré-remplies pour guider l'utilisateur

---

## 🎯 Exemples de Questions

- *"Qui est Michael Jackson ?"*
- *"Quelle est l'histoire du Jazz ?"*
- *"Parle moi d'Oum Kalthoum"*
- *"Quels sont les genres musicaux ?"*
- *"Qui sont les Beatles ?"*
- *"C'est quoi le RAÏ ?"*

---

## ⚙️ Pipeline RAG Détaillé

1. **Chargement** : Les documents TXT sont chargés depuis le dossier `documents/`
2. **Chunking** : Chaque document est découpé en morceaux de 500 tokens avec un overlap de 50
3. **Embedding** : Chaque chunk est transformé en vecteur numérique
4. **Stockage** : Les vecteurs sont stockés dans ChromaDB
5. **Recherche** : La question de l'utilisateur est transformée en vecteur et les 3 chunks les plus proches sont récupérés
6. **Génération** : Le LLM génère une réponse basée sur les chunks récupérés

---

## 📊 Limites et Améliorations Futures

| Limite | Amélioration Possible |
|---|---|
| Base de connaissances limitée | Ajouter plus de documents |
| Chunking fixe | Chunking dynamique |
| Recherche vectorielle simple | Recherche hybride (vectorielle + mots-clés) |
| Pas de mémoire conversationnelle | Ajouter l'historique de conversation |

---

## 👨‍💻 Auteur

Projet réalisé dans le cadre du module **IA Générative (LLM)**
