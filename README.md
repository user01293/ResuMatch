## Live Demo

https://web-production-25682.up.railway.app/

# ResuMatch v2 — Hybrid NLP Resume Matcher

Matches your resume against 32+ job roles using a **three-layer NLP pipeline**:
NLTK preprocessing → sklearn TF-IDF → Sentence-Transformer (BERT) or LSA embeddings.

---

## 🚀 Quick Start

```bash
cd resume_matcher

# Install all dependencies
pip install -r requirements.txt

# Download NLTK data (automatic on first run, or manually):
python -c "import nltk; nltk.download(['punkt','stopwords','wordnet','averaged_perceptron_tagger'])"

# Start the server
python app.py
```

Open → **http://localhost:5000**

---

## 🧠 NLP Architecture

```
Resume Text
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1 — NLTK Preprocessing                                   │
│  word_tokenize → stopword removal → WordNetLemmatizer           │
│                  → PorterStemmer → tech-term normalisation       │
└────────────────────────┬────────────────────────────────────────┘
                         │ cleaned tokens
          ┌──────────────┴────────────────┐
          ▼                               ▼
┌─────────────────────┐       ┌───────────────────────────────────┐
│  Layer 2 — TF-IDF   │       │  Layer 3 — Sentence Embeddings    │
│  Word n-gram (1-2)  │       │                                   │
│  Char n-gram (3-5)  │       │  Tier 1 (best): BERT              │
│  Stacked → sparse   │       │    sentence-transformers           │
│  cosine similarity  │       │    all-MiniLM-L6-v2 (384-d)       │
└────────┬────────────┘       │                                   │
         │                    │  Tier 2 (fallback): LSA           │
         │  tfidf_sim         │    TF-IDF → TruncatedSVD (128-d)  │
         │                    │    dense cosine similarity        │
         │                    └──────────┬────────────────────────┘
         │                               │ embed_sim
         └──────────────┬────────────────┘
                        │
                        ▼
          ┌─────────────────────────────┐
          │  Layer 4 — Skill Matching   │
          │  Pattern regex (100+ terms) │
          │  Weighted overlap ratio     │
          │  Premium skills × 2.0       │
          └────────────┬────────────────┘
                       │ skill_overlap
                       ▼
          ┌─────────────────────────────────────────────┐
          │  Final Score (auto-weighted by tier)        │
          │                                             │
          │  Tier 1 (BERT):  30% TF-IDF + 45% BERT  + 25% Skill │
          │  Tier 2 (LSA):   35% TF-IDF + 35% LSA   + 30% Skill │
          │  Tier 3 (none):  60% TF-IDF + 0%        + 40% Skill │
          └─────────────────────────────────────────────┘
```

---

## 📦 Dependencies

| Package | Role |
|---------|------|
| `nltk` | Tokenisation, stopwords, lemmatisation (WordNet), stemming (Porter) |
| `scikit-learn` | `TfidfVectorizer` (word+char n-grams), `TruncatedSVD` (LSA), cosine_similarity |
| `sentence-transformers` | BERT embeddings (`all-MiniLM-L6-v2`) — **Tier 1** |
| `scipy` | Sparse matrix operations |
| `numpy` | Vector arithmetic |
| `flask` | Web server |
| `pdfminer.six` | PDF text extraction |
| `python-docx` | DOCX parsing |

---

## 📁 Project Structure

```
resume_matcher/
├── app.py                       # Flask API (pre-fits corpus at startup)
├── requirements.txt
├── README.md
├── data/
│   └── jobs_dataset.py          # 32 job descriptions
└── utils/
    ├── nlp_preprocessor.py      # NLTK pipeline (lemmatise → stem)
    ├── embeddings.py            # BERT / LSA / fallback encoder
    ├── matcher.py               # Hybrid scoring engine
    └── resume_parser.py         # PDF / DOCX / TXT extractor
```

---

## 🔌 API

### `POST /api/match`

```bash
# File upload
curl -X POST http://localhost:5000/api/match -F "resume=@cv.pdf"

# Text
curl -X POST http://localhost:5000/api/match \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"Python ML engineer 5 years TensorFlow AWS..."}'
```

**Response** includes `tfidf_score`, `embed_score`, `skill_overlap_pct` per job.

### `GET /api/health`
Returns active embedding tier.

---

## 🔒 Privacy
Resumes are processed in-memory only — nothing is stored on disk.
