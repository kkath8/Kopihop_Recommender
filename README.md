#  ☕︎ྀི KopiHop Recommender

**KopiHop** is a context-aware cafe recommendation web app for **Santa Rosa, Laguna, Philippines**. Users describe what they're looking for — in English, Tagalog, or Taglish, and the app recommends the best local cafes to visit, complete with menus, tags, hours, and price ranges.

---

## Features

- **Voice & Text Input** — speak or type your query; voice uses the browser's Web Speech API (`en-PH` locale)
- **Multilingual NLP** — understands English, Filipino (Tagalog), and Taglish with a built-in keyword expansion and synonym map
- **Smart Keyword Scoring** — tag-based scoring engine ranks cafes by relevance to your query (vibe, budget, occasion, time of day, etc.)
- **Optional Ollama AI Backend** — if enabled, passes top-matched cafes to a local LLaMA 3 model for a richer, natural-language response
- **Cafe Detail Pages** — full menus organized by category, address, hours, and description
- **Voice Query Logging** — every query is logged with detected language, input method, and recommended cafe IDs
- **pgvector Ready** — the database schema supports 384-dimensional embeddings for future semantic/vector search
- **State Restore** — last search results survive page navigation via `sessionStorage`

---

## Project Structure

```
kopihop_recommender/
├── app.py                  # Flask application factory
├── config.py               # Config class (loads from .env)
├── Procfile                # Gunicorn entry point (for Railway / Heroku)
├── requirements.txt        # Python dependencies
├── .env                    # Local environment variables (not committed)
│
├── database/
│   ├── db.py               # SQLAlchemy instance + init_db()
│   ├── models.py           # ORM models: Cafe, MenuItem, UserSession, VoiceLog
│   ├── schema.sql          # Raw SQL schema (with pgvector extension)
│   └── seed.py             # Seeds all 22 Santa Rosa cafes + menu items
│
├── routes/
│   ├── main.py             # GET / — home page
│   ├── cafes.py            # GET /cafes/, GET /cafes/<id> — cafe list & detail
│   └── ai.py               # POST /ai/recommend — recommendation engine
│
├── static/
│   ├── css/style.css       # App-wide styles
│   ├── js/voice.js         # Voice assistant (SpeechRecognition + UI logic)
│   └── images/             # Cafe photo
│
└── templates/
    ├── base.html           # Base layout
    ├── home.html           # Landing page with mic button and results grid
    ├── cafes.html          # Browse all cafes
    └── cafe_detail.html    # Individual cafe page with menu
```

---

## Cafes in the Database

KopiHop ships with **22 real cafes** in Santa Rosa, Laguna:

|   | Cafe 
|---|------
| 1 | Caffe Arabica
| 2 | Grayscale Coffee Club
| 3 | Cafe De Rosa 
| 4 | Cafe Maestro 
| 5 | Evrydycoffee 
| 6 | Kafe Lando 
| 7 | Sweet Avenue 
| 8 | Cafe Royal 
| 9 | Camila's Maison
| 10 | Dudin's 
| 11 | PickUp Coffee (SM Branch) 
| 12 | WDYT (What Do You Think) 
| 13 | Zus Coffee 
| 14 | BrewHilda
| 15 | Bean Here Cafe
| 16 | But First Coffee 
| 17 | Starbucks
| 18 | Bigbrew
| 19 | Bad H
| 20 | Soho Cafe
| 21 | Three Monkey Brew & Bites
| 22 | JCO

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13 · Flask 3.1 · Flask-SQLAlchemy 3.1 |
| Database | PostgreSQL · pgvector (vector search extension) |
| ORM | SQLAlchemy 2.0 |
| AI (optional) | Ollama (LLaMA 3) via local HTTP API |
| Frontend | Jinja2 templates · Vanilla JS · Web Speech API |
| Server | Gunicorn (production) |
| Deployment | Railway / Heroku (Procfile included) |

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL with the `pgvector` extension installed
- *(Optional)* [Ollama](https://ollama.com) running locally with `llama3` pulled

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd kopihop_recommender
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# PostgreSQL connection string
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/kopihop

# Flask
SECRET_KEY=change-this-to-any-random-string
DEBUG=true

# Ollama (optional — set USE_OLLAMA=false to use keyword engine only)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3
USE_OLLAMA=false
```

> ⚠️ **Never commit your `.env` file.** Add it to `.gitignore`.

### 5. Create the Database

```bash
# Connect to PostgreSQL and create the database
psql -U postgres -c "CREATE DATABASE kopihop;"

# Enable pgvector (run inside the kopihop database)
psql -U postgres -d kopihop -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Apply the schema
psql -U postgres -d kopihop -f database/schema.sql
```

### 6. Seed the Database

```bash
python database/seed.py
```

This inserts all 22 cafes and their menu items.

### 7. Run the App

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000).

---

## AI Engine Modes

KopiHop supports two recommendation engines, switchable via `.env`:

### Keyword Engine (default)

Always active. Uses a curated Tagalog → English keyword map and synonym expansion to score cafes by their tags. Fast, offline, no external dependencies.

```
USE_OLLAMA=false
```

### Ollama AI Engine (optional)

When enabled, the keyword engine selects top candidates, then passes them to a locally running LLaMA 3 model for a natural-language response. Falls back to keyword mode if Ollama is unavailable or times out.

```
USE_OLLAMA=true
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

To install Ollama and pull the model:

```bash
# Install Ollama from https://ollama.com
ollama pull llama3
ollama serve
```

---

## API Reference

### `POST /ai/recommend`

Returns cafe recommendations based on a natural-language query.

**Request body (JSON):**

```json
{
  "query": "may tahimik na lugar para mag-aral na may wifi?",
  "conversation_history": [],
  "input_method": "voice"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | User's query in English, Tagalog, or Taglish |
| `conversation_history` | array | Previous turns for Ollama context (optional) |
| `input_method` | string | `"voice"` or `"text"` — used for logging |

**Response (JSON):**

```json
{
  "recommendations": [
    {
      "id": 2,
      "name": "Grayscale Coffee Club",
      "address": "Bittersweet St., Santa Rosa, Laguna",
      "description": "...",
      "image": "GrayScale.jpg",
      "tags": ["24hours", "student", "wifi", "study"],
      "hours": "Daily: Open 24 Hours",
      "price_range": "₱100–₱300",
      "reason": "Grayscale is a great pick — it's ideal for studying with fast wifi and open 24 hours."
    }
  ],
  "ai_message": "Found 3 great cafes matching your request!",
  "detected_lang": "tl",
  "engine": "keyword"
}
```

### `GET /cafes/`

Returns all cafes as an HTML page.

### `GET /cafes/<id>`

Returns the detail page for a single cafe, including its full menu organized by category.

### `GET /`

Home page with the voice/text query interface.

---

## Database Schema

```
cafes           — cafe info, tags, hours, price_range, embedding (vector)
menu_items      — items linked to cafes (category, name, price)
user_sessions   — anonymous session tracking via session token
voice_logs      — every query: text, language, input method, recommended IDs
```

The `embedding` column (384-dim vector) is ready for sentence-transformer integration for semantic search.

---

## Deployment (Railway / Heroku)

The app includes a `Procfile` for one-command deployment:

```
web: gunicorn "app:create_app()"
```

Set the following environment variables in your deployment platform's dashboard:

```
DATABASE_URL      (Railway provides this automatically)
SECRET_KEY
USE_OLLAMA=false  (Ollama is not available on cloud platforms without a dedicated server)
```

> **Railway note:** The `config.py` automatically converts `postgres://` URLs (provided by Railway) to `postgresql://` as required by SQLAlchemy.

---

## Supported Query Concepts

KopiHop understands queries about:

| Category | Examples |
|----------|---------|
| **Vibe** | quiet, chill, cozy, aesthetic, minimalist |
| **Occasion** | barkada, date, family, solo, kwentuhan |
| **Time** | gabi, late-night, 24 hours, umaga, hapon |
| **Budget** | mura, sulit, budget, affordable, mahal |
| **Needs** | wifi, charging, study, laptop, thesis |
| **Food** | kain, merienda, almusal, dessert, silog |
| **Ambiance** | outdoor, garden, labas, hardin, live-band, KTV |
| **Language** | English · Tagalog · Taglish |

---

## Development Notes

- The `seed.py` script is safe to re-run — it drops and re-inserts all data.
- Voice recognition is set to `en-PH` locale and works best in Chrome or Edge.
- The `VOICE_LOG_ENABLED` flag in `config.py` can be set to `False` to disable logging.
- `pool_pre_ping=True` is set in the SQLAlchemy engine options to handle idle connection drops.

---

## License

This project is for educational purposes. Cafe names, addresses, and menu data are publicly available local information specific to Santa Rosa, Laguna, Philippines.
