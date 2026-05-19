"""
embeddings.py
─────────────
Sentence-embedding layer with three tiers:

  Tier 1 — sentence-transformers (BERT-based)
            Model: "all-MiniLM-L6-v2" (80 MB, very fast, high quality)
            Falls back automatically if not installed or no GPU.

  Tier 2 — sklearn TF-IDF + TruncatedSVD (LSA)
            Word n-gram (1-2) + char n-gram (3-5) stacked → 128-d dense
            embedding.  Gives BERT-like semantic generalisation without
            requiring PyTorch.

  Tier 3 — Pure cosine on raw TF-IDF (already in matcher.py).
            Used only if sklearn itself is unavailable (very rare).

Both Tier 1 and Tier 2 return L2-normalised float32 numpy arrays so
the calling code is identical regardless of which tier is active.
"""

from __future__ import annotations
import numpy as np
import re

# ── Tier tracking ─────────────────────────────────────────────────
_TIER: int = 3          # updated below
_MODEL = None           # sentence_transformers model
_WORD_VEC = None        # sklearn TfidfVectorizer (word)
_CHAR_VEC = None        # sklearn TfidfVectorizer (char)
_SVD = None             # TruncatedSVD
_FITTED = False         # whether Tier-2 pipeline is fitted

# ─────────────────────────────────────────────────────────────────
# Tier 1: sentence-transformers / BERT
# ─────────────────────────────────────────────────────────────────
try:
    from sentence_transformers import SentenceTransformer
    _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    _TIER = 1
    print("[Embed] ✅  Tier 1 — sentence-transformers/all-MiniLM-L6-v2 (BERT)")
except Exception as _e1:
    # Try transformers + torch directly
    try:
        import torch
        from transformers import AutoTokenizer, AutoModel

        _TOKENIZER = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        _HF_MODEL  = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        _HF_MODEL.eval()

        class _HFWrapper:
            """Thin wrapper so it matches SentenceTransformer.encode() API."""
            def encode(self, sentences, convert_to_numpy=True, show_progress_bar=False):
                if isinstance(sentences, str):
                    sentences = [sentences]
                encoded = _TOKENIZER(sentences, padding=True, truncation=True,
                                     max_length=256, return_tensors="pt")
                with torch.no_grad():
                    out = _HF_MODEL(**encoded)
                # Mean-pool last hidden state
                mask = encoded["attention_mask"].unsqueeze(-1).float()
                vecs = (out.last_hidden_state * mask).sum(1) / mask.sum(1)
                vecs = torch.nn.functional.normalize(vecs, p=2, dim=1)
                return vecs.numpy() if convert_to_numpy else vecs

        _MODEL = _HFWrapper()
        _TIER  = 1
        print("[Embed] ✅  Tier 1 — HuggingFace transformers (all-MiniLM-L6-v2)")
    except Exception as _e2:
        print(f"[Embed] ⚠️  Tier 1 unavailable ({_e1}). Trying Tier 2 (LSA).")

# ─────────────────────────────────────────────────────────────────
# Tier 2: sklearn LSA embeddings
# ─────────────────────────────────────────────────────────────────
if _TIER == 3:
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.decomposition import TruncatedSVD
        from sklearn.preprocessing import normalize
        from scipy.sparse import hstack as sp_hstack

        _WORD_VEC = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=12_000,
            analyzer="word",
            min_df=1,
        )
        _CHAR_VEC = TfidfVectorizer(
            ngram_range=(3, 5),
            sublinear_tf=True,
            max_features=12_000,
            analyzer="char_wb",
            min_df=1,
        )
        _SVD = TruncatedSVD(n_components=128, random_state=42, n_iter=7)
        _TIER = 2
        print("[Embed] ✅  Tier 2 — sklearn LSA embeddings (word+char TF-IDF → SVD-128)")
    except Exception as _e3:
        print(f"[Embed] ⚠️  Tier 2 unavailable ({_e3}). Using raw TF-IDF cosine only.")


# ─────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────

def get_tier() -> int:
    """Return active embedding tier (1=BERT, 2=LSA, 3=TF-IDF only)."""
    return _TIER


def get_tier_name() -> str:
    names = {
        1: "BERT (sentence-transformers/all-MiniLM-L6-v2)",
        2: "LSA Embeddings (word+char TF-IDF → TruncatedSVD-128)",
        3: "TF-IDF Cosine Only",
    }
    return names.get(_TIER, "Unknown")


def fit(corpus: list[str]) -> None:
    """
    Fit the Tier-2 pipeline on the given corpus.
    For Tier 1 (BERT) this is a no-op.
    Must be called once before encode() when using Tier 2.
    """
    global _FITTED
    if _TIER != 2 or _FITTED:
        return

    from scipy.sparse import hstack as sp_hstack
    from sklearn.preprocessing import normalize

    Xw = _WORD_VEC.fit_transform(corpus)
    Xc = _CHAR_VEC.fit_transform(corpus)
    X  = sp_hstack([Xw, Xc])
    _SVD.fit(X)
    _FITTED = True


def encode(texts: list[str]) -> np.ndarray:
    """
    Encode a list of strings into L2-normalised dense vectors.

    Returns
    -------
    np.ndarray of shape (len(texts), dim)
      dim = 384 for BERT / 128 for LSA / empty for Tier 3
    """
    if not texts:
        return np.zeros((0, 128), dtype=np.float32)

    # ── Tier 1: BERT ──────────────────────────────────────────────
    if _TIER == 1:
        vecs = _MODEL.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return (vecs / norms).astype(np.float32)

    # ── Tier 2: LSA ───────────────────────────────────────────────
    if _TIER == 2:
        from scipy.sparse import hstack as sp_hstack
        from sklearn.preprocessing import normalize as sk_normalize

        if not _FITTED:
            raise RuntimeError("Call embeddings.fit(corpus) before encode().")

        Xw   = _WORD_VEC.transform(texts)
        Xc   = _CHAR_VEC.transform(texts)
        X    = sp_hstack([Xw, Xc])
        vecs = _SVD.transform(X)
        return sk_normalize(vecs, norm="l2").astype(np.float32)

    # ── Tier 3: return zeros (caller uses TF-IDF only) ────────────
    return np.zeros((len(texts), 1), dtype=np.float32)


def cosine_sim_matrix(query_vecs: np.ndarray, corpus_vecs: np.ndarray) -> np.ndarray:
    """
    Fast batch cosine similarity.
    Both inputs must be L2-normalised → dot product == cosine similarity.

    Returns shape (n_queries, n_corpus).
    """
    if query_vecs.shape[1] == 1 or corpus_vecs.shape[1] == 1:
        # Tier 3 fallback — return zeros; caller will rely on TF-IDF alone
        return np.zeros((query_vecs.shape[0], corpus_vecs.shape[0]))
    return query_vecs @ corpus_vecs.T
