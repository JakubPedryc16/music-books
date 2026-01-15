# Narrative-Music-Matcher: A Cross-Modal Recommendation Engine

![Python](https://img.shields.io/badge/python-3.13+-green.svg)
![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688.svg)
![React](https://img.shields.io/badge/frontend-React-61DAFB.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

This repository contains the software implementation of a cross-modal recommendation engine that maps narrative texts to musical tracks. The system utilizes Transformers and acoustic feature analysis to synchronize auditory environments with textual sentiment.

## Installation and Setup

To set up the project locally, follow these steps:

1. Clone the repository:
```bash
   git clone https://github.com/JakubPedryc16/music-books.git
   cd music-books
```
2. Backend configuration:  
   Create a virtual environment and set up your environment variables.

```bash
    cd backend
    python -m venv venv

    # Activate virtual environment
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate

    pip install -r requirements.txt
```

Create a `.env` file in the `/backend` directory and fill in your credentials:

    
```makefile
   SPOTIPY_CLIENT_ID=your_spotify_client_id
   SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
   SPOTIPY_REDIRECT_URI=http://localhost:8000/callback
   SCOPE=user-read-private user-read-email
   FRONTEND_URL=http://localhost:5173
   JWT_SECRET=your_random_secret_key
```    


3. NLTK Data Download
The system requires specific NLTK packages for text processing (tokenization and tagging). Run the following command:
```bash
    python -m nltk.downloader punkt averaged_perceptron_tagger
```
4. Database Migrations:
The project uses SQLite and Alembic for database management. Initialize your local database schema with:
```bash
    alembic upgrade head
```
5. Running the Application
The backend is powered by FastAPI. Start the server using Uvicorn:
```bash
    uvicorn main:app --reload
```
6. **Frontend Configuration**  
   Create a `.env` file in the `frontend/` directory and set the backend connection:

```env
    VITE_BACKEND_URL=http://localhost:8000
```
7. **Running the Frontend**  
   Install Node modules and start the Vite development server:
```bash
    cd ../frontend
    npm install
    npm run dev
```


## System Architecture

The core of the system is a **Cascaded Filtering Pipeline** designed for high-efficiency retrieval. It bridges the semantic gap between narrative text and music metadata by processing information through a sequence of specialized neural layers, ensuring that computationally expensive operations are only performed on the most relevant candidates.

### 1. Neural Processing & Filtering Pipeline
The architecture employs a multi-stage selection strategy to ensure high accuracy while achieving **30x faster processing** compared to exhaustive search methods:

* **Multilingual Translation Layer**: Features an integrated pipeline using the `Helsinki-NLP/opus-mt-pl-en` model. This allows the system to process Polish narrative texts by converting them into English before they enter the matching stages.
* **Emotion & Sentiment Filters (L1)**: Uses **fine-tuned** models (`j-hartmann/emotion-english-distilroberta-base` and `distilbert-base-uncased-finetuned-sst-2`) to identify the emotional core (e.g., *joy, sadness, suspense*) and mood polarity. This stage prunes the database by discarding tracks that do not align with the text's emotional profile.
* **Thematic Tag Matcher (L2)**: Leverages **SBERT** (`all-MiniLM-L6-v2`) to quantify contextual similarity. It compares the thematic essence of the text against descriptive music tags, narrowing the pool to tracks with similar narrative "topics."
* **Final Embedding Matcher (L3)**: The decision-making layer. It takes the pre-filtered candidates and performs a high-precision **Vector Similarity Search (Cosine Similarity)**. By comparing dense embeddings of the text directly with music features, it selects the final track that best represents the "acoustic soul" of the scene.



### 2. Tech Stack & Engineering Excellence
* **Backend (FastAPI)**: Designed for high-performance inference. It utilizes **Lifespan Singleton Management** for Transformer models, ensuring that large weights are loaded into memory only once during the application's lifecycle.
* **Hardware Acceleration**: The system automatically detects and utilizes **CUDA-enabled GPUs** via `torch` for real-time processing, significantly reducing latency for Transformer-based tasks.
* **Data Access Layer (DAL)**: A robust abstraction layer separating business logic from database operations, handling complex joins between tracks, books, and pre-computed vector embeddings.
* **Frontend Ecosystem (React + Vite)**: A reactive interface powered by custom **React Hooks** (`useTextMatcher`, `usePlaySpotify`). It features real-time integration with the **Spotify Web Playback SDK** for seamless audio transitions and playback control.
* **Database & Migrations**: Powered by **SQLAlchemy** and **Alembic**, managing a relational schema optimized for fast retrieval of high-dimensional data.


## Project Structure

```text
music-books/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes (spotify, books, match)
│   │   ├── dal/          # Data Access Layer (SQLAlchemy queries)
│   │   ├── matchers/     # Recommendation logic & strategy implementations
│   │   ├── ml_models/    # Singleton management for Transformer models
│   │   ├── models/       # Database SQLAlchemy models
│   │   ├── services/     # Business logic (e.g., GlobalMusicContext)
│   │   └── utils/        # Exception handlers & loggers
│   ├── data/             # CSV files, databases and local tags
│   ├── alembic/          # Database migrations
│   ├── main.py           # FastAPI entry point with lifespan
│   └── .env              # Environment secrets (Spotify API, JWT)
└── frontend/
    ├── app/
    │   ├── components/   # Reusable UI elements (Navbar, Common, Pages)
    │   ├── hooks/        # Custom React hooks (useApi, useTextMatcher, usePlaySpotify)
    │   ├── content/      # Static text assets
    │   └── utils/        # Frontend API clients and helpers
    ├── public/           # Static assets
    └── package.json      # Frontend dependencies and scripts
```

## Citation

If you use this software in your research, please cite:
Pedryc, J., Krużel, F. (2026). Music Recommendation System for Narrative Texts Based on Semantic and Emotional Analysis.

## License

Distributed under the MIT License.