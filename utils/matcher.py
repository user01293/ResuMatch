"""
matcher.py  (v2 — Hybrid NLP Engine)
─────────────────────────────────────
Scoring pipeline:

  1. NLTK preprocessing  → lemmatise + stem corpus & query
  2. sklearn TF-IDF      → sparse cosine similarity  (weight: W_TFIDF)
  3. Embedding cosine    → BERT or LSA dense vectors  (weight: W_EMBED)
  4. Skill-overlap ratio → exact skill keyword match  (weight: W_SKILL)

  Final score = W_TFIDF * tfidf_sim
              + W_EMBED * embed_sim
              + W_SKILL * skill_overlap

The weights adapt to the available embedding tier:
  Tier 1 (BERT)   → 0.30 TF-IDF + 0.45 BERT  + 0.25 skill
  Tier 2 (LSA)    → 0.35 TF-IDF + 0.35 LSA   + 0.30 skill
  Tier 3 (none)   → 0.60 TF-IDF + 0.00        + 0.40 skill
"""

from __future__ import annotations
import re
import math
from collections import Counter
from typing import Any

import numpy as np

# ── Local imports ─────────────────────────────────────────────────
from utils.nlp_preprocessor import preprocess_for_tfidf, extract_noun_phrases
from utils import embeddings as emb

# sklearn – guaranteed available (checked in tests)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sk_cosine
from scipy.sparse import hstack as sp_hstack

# ─────────────────────────────────────────────────────────────────
# Scoring weights (selected at module load based on embedding tier)
# ─────────────────────────────────────────────────────────────────
_TIER = emb.get_tier()
if _TIER == 1:
    W_TFIDF, W_EMBED, W_SKILL = 0.30, 0.45, 0.25
elif _TIER == 2:
    W_TFIDF, W_EMBED, W_SKILL = 0.35, 0.35, 0.30
else:
    W_TFIDF, W_EMBED, W_SKILL = 0.60, 0.00, 0.40

print(f"[Matcher] weights -> TF-IDF:{W_TFIDF}  Embed:{W_EMBED}  Skill:{W_SKILL}")

# ─────────────────────────────────────────────────────────────────
# Skill keyword catalogue  (100+ terms across domains)
# ─────────────────────────────────────────────────────────────────
SKILL_PATTERNS: dict[str, list[str]] = {
    # Programming Languages
    "Python":       ["python"],
    "Java":         [r"\bjava\b"],
    "JavaScript":   ["javascript", r"\bjs\b"],
    "TypeScript":   ["typescript", r"\bts\b"],
    "C++":          [r"c\+\+", "cplusplus"],
    "C#":           [r"c#", "csharp"],
    "Go":           [r"\bgolang\b", r"\bgo\b"],
    "Rust":         [r"\brust\b"],
    "Swift":        ["swift"],
    "Kotlin":       ["kotlin"],
    "R":            [r"\blanguage r\b", r"\busing r\b", r"\bin r\b", r"\bwith r\b"],
    "PHP":          [r"\bphp\b"],
    "Ruby":         ["ruby"],
    "Scala":        ["scala"],
    "MATLAB":       ["matlab"],
    "Shell/Bash":   [r"\bbash\b", r"\bshell script"],
    # Web Frameworks
    "React":        ["react"],
    "Angular":      ["angular"],
    "Vue.js":       [r"vue\.?js", "vuejs"],
    "Next.js":      [r"next\.?js", "nextjs"],
    "Node.js":      [r"node\.?js", "nodejs"],
    "Django":       ["django"],
    "FastAPI":      ["fastapi"],
    "Flask":        [r"\bflask\b"],
    "Spring Boot":  ["spring boot", "springboot"],
    "GraphQL":      ["graphql"],
    "REST APIs":    ["rest api", "restful", "restapi"],
    # ML / AI
    "TensorFlow":   ["tensorflow"],
    "PyTorch":      ["pytorch"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "Keras":        ["keras"],
    "Pandas":       ["pandas"],
    "NumPy":        ["numpy"],
    "Machine Learning":      ["machine learning"],
    "Deep Learning":         ["deep learning"],
    "NLP":                   ["natural language processing", r"\bnlp\b"],
    "Computer Vision":       ["computer vision"],
    "LLM":                   [r"\bllm\b", "large language model"],
    "Transformers":          ["hugging face", "transformers"],
    "LangChain":             ["langchain"],
    "RAG":                   [r"\brag\b", "retrieval augmented"],
    "Reinforcement Learning":["reinforcement learning"],
    "MLOps":                 ["mlops", "ml ops"],
    # Cloud / DevOps
    "AWS":          [r"\baws\b", "amazon web services"],
    "Azure":        [r"\bazure\b"],
    "GCP":          [r"\bgcp\b", "google cloud"],
    "Docker":       ["docker"],
    "Kubernetes":   ["kubernetes", r"\bk8s\b"],
    "Terraform":    ["terraform"],
    "Ansible":      ["ansible"],
    "CI/CD":        [r"ci/cd", "cicd", "continuous integration"],
    "Jenkins":      ["jenkins"],
    "Linux":        ["linux"],
    "Git":          [r"\bgit\b"],
    "GitHub Actions":["github actions"],
    # Databases
    "SQL":          [r"\bsql\b"],
    "PostgreSQL":   ["postgresql", "postgres"],
    "MySQL":        ["mysql"],
    "MongoDB":      ["mongodb"],
    "Redis":        ["redis"],
    "Snowflake":    ["snowflake"],
    "BigQuery":     ["bigquery"],
    "Redshift":     ["redshift"],
    "Cassandra":    ["cassandra"],
    "Elasticsearch":["elasticsearch"],
    # Data / Analytics
    "Apache Spark": ["apache spark", "pyspark"],
    "Kafka":        ["kafka"],
    "Airflow":      ["airflow"],
    "dbt":          [r"\bdbt\b"],
    "Tableau":      ["tableau"],
    "Power BI":     ["power bi", "powerbi"],
    "Looker":       ["looker"],
    "ETL":          [r"\betl\b"],
    # Mobile
    "iOS":          [r"\bios\b"],
    "Android":      ["android"],
    "Flutter":      ["flutter"],
    "React Native": ["react native"],
    "SwiftUI":      ["swiftui"],
    # Security
    "Cybersecurity":          ["cybersecurity", "information security"],
    "Penetration Testing":    ["penetration testing", "pen testing", "pentest"],
    "SIEM":                   [r"\bsiem\b"],
    "CISSP":                  [r"\bcissp\b"],
    "NIST":                   [r"\bnist\b"],
    # Design
    "Figma":        ["figma"],
    "Sketch":       [r"\bsketch\b"],
    "Adobe XD":     ["adobe xd"],
    "Photoshop":    ["photoshop"],
    # Methodologies
    "Agile":        ["agile"],
    "Scrum":        ["scrum"],
    "Kanban":       ["kanban"],
    "SAFe":         [r"\bsafe\b", "scaled agile"],
    # Tools
    "JIRA":         ["jira"],
    "Confluence":   ["confluence"],
    "Postman":      ["postman"],
    "Selenium":     ["selenium"],
    "Cypress":      ["cypress"],
    "Playwright":   ["playwright"],
    # Business / Soft
    "Leadership":          ["leadership", "lead a team", "team lead"],
    "Communication":       ["communication"],
    "Stakeholder Mgmt":    ["stakeholder"],
    "Project Management":  ["project management"],
    "Financial Modeling":  ["financial modeling", "financial modelling"],
    "Excel":               [r"\bexcel\b"],
    "Tableau":             ["tableau"],
    "SAP":                 [r"\bsap\b"],
    "Salesforce":          ["salesforce"],
    "HubSpot":             ["hubspot"],
}

# Pre-compile all patterns for speed
_COMPILED: dict[str, list[re.Pattern]] = {
    skill: [re.compile(p, re.IGNORECASE) for p in patterns]
    for skill, patterns in SKILL_PATTERNS.items()
}

# High-value skills that get 2x weight in skill-overlap score
_PREMIUM_SKILLS = {
    "Python","TensorFlow","PyTorch","AWS","Docker","Kubernetes","Scikit-learn",
    "NLP","Machine Learning","Deep Learning","LLM","Transformers","LangChain",
    "Apache Spark","Kafka","React","TypeScript","GraphQL","Snowflake","dbt",
    "MLOps","Reinforcement Learning","RAG","Flutter","Rust","Go","Scala",
}

# ─────────────────────────────────────────────────────────────────
# Corpus-level TF-IDF vectorisers  (fitted once at startup)
# ─────────────────────────────────────────────────────────────────
_TFIDF_WORD = TfidfVectorizer(
    ngram_range=(1, 2),
    sublinear_tf=True,
    max_features=15_000,
    min_df=1,
    analyzer="word",
    token_pattern=r"[a-z0-9][a-z0-9_]{1,}",
)
_TFIDF_CHAR = TfidfVectorizer(
    ngram_range=(3, 5),
    sublinear_tf=True,
    max_features=10_000,
    min_df=1,
    analyzer="char_wb",
)

_CORPUS_MATRIX   = None          # sparse, shape (n_jobs, n_features)
_CORPUS_TEXTS:  list[str] = []
_CORPUS_EMBEDS: np.ndarray | None = None   # dense, shape (n_jobs, dim)
_JOBS_CACHE:    list[dict] = []


def _build_job_text(job: dict) -> str:
    """Combine job fields into a single text blob for vectorisation."""
    skills_str = " ".join(job.get("skills", []))
    return (
        f"{job['title']} {job['title']} {job['title']} "
        f"{job['category']} {job['category']} "
        f"{skills_str} {skills_str} "
        f"{job['description']} "
        f"{job.get('experience','')} {job.get('education','')}"
    )


def _fit_corpus(jobs: list[dict]) -> None:
    """Fit TF-IDF + embedding model on the job corpus. Called once."""
    global _CORPUS_MATRIX, _CORPUS_TEXTS, _CORPUS_EMBEDS, _JOBS_CACHE

    raw_texts  = [_build_job_text(j) for j in jobs]
    proc_texts = [preprocess_for_tfidf(t) for t in raw_texts]
    _CORPUS_TEXTS = proc_texts
    _JOBS_CACHE   = jobs

    # TF-IDF fit
    Xw = _TFIDF_WORD.fit_transform(proc_texts)
    Xc = _TFIDF_CHAR.fit_transform(proc_texts)
    _CORPUS_MATRIX = sp_hstack([Xw, Xc], format="csr")

    # Embedding fit & encode
    emb.fit(proc_texts)
    _CORPUS_EMBEDS = emb.encode(proc_texts)

    print(f"[Matcher] Corpus fitted: {len(jobs)} jobs | "
          f"TF-IDF {_CORPUS_MATRIX.shape} | embed {_CORPUS_EMBEDS.shape}")


# ─────────────────────────────────────────────────────────────────
# Public: skill extraction helpers
# ─────────────────────────────────────────────────────────────────

def extract_skills(text: str) -> list[str]:
    """Return list of skill names found in text (order: SKILL_PATTERNS)."""
    return [s for s, pats in _COMPILED.items()
            if any(p.search(text) for p in pats)]


def extract_experience_years(text: str) -> int:
    """Return max years of experience found in text."""
    patterns = [
        r"(\d+)\+?\s*years?\s+(?:of\s+)?(?:professional\s+)?experience",
        r"(\d+)\+?\s*yrs?\s+(?:of\s+)?experience",
        r"experience\s+(?:of\s+)?(\d+)\+?\s*years?",
    ]
    max_y = 0
    for pat in patterns:
        for m in re.findall(pat, text, re.IGNORECASE):
            try: max_y = max(max_y, int(m))
            except ValueError: pass
    return max_y


def extract_education(text: str) -> str:
    """Return highest detected education level."""
    tl = text.lower()
    if re.search(r"\bph\.?d\b|\bdoctorate\b|\bdoctoral\b", tl):        return "Ph.D."
    if re.search(r"\bmaster'?s?\b|\bm\.s\.?\b|\bm\.sc\.?\b|\bmba\b|\bm\.eng\b|\bmtech\b", tl): return "Master's"
    if re.search(r"\bbachelor'?s?\b|\bb\.s\.?\b|\bb\.sc\.?\b|\bb\.e\.?\b|\bb\.tech\b|\bundergraduate\b", tl): return "Bachelor's"
    if re.search(r"\bassociate'?s?\b", tl):                              return "Associate's"
    return "Not specified"


# ─────────────────────────────────────────────────────────────────
# Weighted skill-overlap
# ─────────────────────────────────────────────────────────────────

def _skill_overlap(resume_skills: set[str], job_skills: list[str]) -> float:
    if not job_skills:
        return 0.0
    total, matched = 0.0, 0.0
    for s in job_skills:
        w = 2.0 if s in _PREMIUM_SKILLS else 1.0
        total += w
        if s in resume_skills:
            matched += w
    return matched / total if total else 0.0


# ─────────────────────────────────────────────────────────────────
# Main matching function
# ─────────────────────────────────────────────────────────────────

def match_resume_to_jobs(
    resume_text: str,
    jobs_dataset: list[dict],
    top_n: int = 10,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Hybrid match: NLTK preprocessing → sklearn TF-IDF → embeddings → skill overlap.

    Returns (matches, resume_info).
    """
    if not resume_text or len(resume_text.strip()) < 30:
        return [], {}

    # Fit corpus on first call
    if _CORPUS_MATRIX is None:
        _fit_corpus(jobs_dataset)

    # Preprocess resume
    proc_resume = preprocess_for_tfidf(resume_text)

    # TF-IDF similarity
    Rw = _TFIDF_WORD.transform([proc_resume])
    Rc = _TFIDF_CHAR.transform([proc_resume])
    R_sparse   = sp_hstack([Rw, Rc], format="csr")
    tfidf_sims = sk_cosine(R_sparse, _CORPUS_MATRIX)[0]   # (n_jobs,)

    # Embedding similarity
    R_embed    = emb.encode([proc_resume])                 # (1, dim)
    embed_sims = emb.cosine_sim_matrix(R_embed, _CORPUS_EMBEDS)[0]  # (n_jobs,)

    # Skill extraction
    resume_skills_raw  = extract_skills(resume_text)
    resume_skills_set  = set(resume_skills_raw)
    resume_years       = extract_experience_years(resume_text)
    resume_education   = extract_education(resume_text)
    resume_phrases     = extract_noun_phrases(resume_text)

    # Score each job
    results: list[dict] = []
    for i, job in enumerate(jobs_dataset):
        job_skills = job.get("skills", [])
        skill_ov   = _skill_overlap(resume_skills_set, job_skills)

        combined = (
            W_TFIDF * float(tfidf_sims[i]) +
            W_EMBED * float(embed_sims[i]) +
            W_SKILL * skill_ov
        )

        # Scale combined score [0,~0.7] → [0,100]
        match_pct = round(min(99, max(1, combined * 175)))

        matched = [s for s in job_skills if s in resume_skills_set]
        missing = [s for s in job_skills if s not in resume_skills_set]

        results.append({
            "job":               job,
            "match_score":       match_pct,
            "tfidf_score":       round(float(tfidf_sims[i]) * 100, 1),
            "embed_score":       round(float(embed_sims[i]) * 100, 1),
            "skill_overlap_pct": round(skill_ov * 100, 1),
            "matched_skills":    matched,
            "missing_skills":    missing[:7],
            "skill_match_count": len(matched),
            "total_skills":      len(job_skills),
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    resume_info = {
        "skills":           resume_skills_raw,
        "noun_phrases":     resume_phrases[:10],
        "experience_years": resume_years,
        "education":        resume_education,
        "skill_count":      len(resume_skills_raw),
        "embedding_tier":   emb.get_tier_name(),
        "weights": {
            "tfidf": W_TFIDF,
            "embed": W_EMBED,
            "skill": W_SKILL,
        },
    }

    return results[:top_n], resume_info
