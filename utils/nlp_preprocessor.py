"""
nlp_preprocessor.py
────────────────────
NLTK-based text preprocessing pipeline:
  - Tokenisation (word_tokenize)
  - Stop-word removal (nltk.corpus.stopwords)
  - Porter stemming  (nltk.stem.PorterStemmer)
  - Lemmatisation    (nltk.stem.WordNetLemmatizer)

Falls back to regex-based processing when NLTK is not installed,
so the app always works even without the library.
"""

from __future__ import annotations
import re
import string

# ── Try importing NLTK components ────────────────────────────────
_NLTK_AVAILABLE = False
_tokenize = None
_stop_words = None
_stemmer = None
_lemmatizer = None

try:
    import nltk

    # Silently download required corpora if missing
    for _pkg in ("punkt", "punkt_tab", "stopwords", "wordnet", "averaged_perceptron_tagger"):
        try:
            nltk.download(_pkg, quiet=True)
        except Exception:
            pass

    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer, WordNetLemmatizer

    _tokenize   = word_tokenize
    _stop_words = set(stopwords.words("english"))
    _stemmer    = PorterStemmer()
    _lemmatizer = WordNetLemmatizer()
    _NLTK_AVAILABLE = True
    print("[NLP] ✅  NLTK pipeline active (tokenise → stopwords → lemmatise → stem)")

except Exception as _e:
    print(f"[NLP] ⚠️  NLTK unavailable ({_e}). Using regex fallback.")

# ── Domain-specific additions to the stop list ───────────────────
_EXTRA_STOPS = {
    "experience", "year", "years", "work", "working", "job", "role",
    "position", "team", "company", "organization", "including", "also",
    "using", "use", "used", "build", "building", "built", "develop",
    "developed", "developing", "strong", "ability", "skills", "skill",
    "knowledge", "required", "preferred", "looking", "join", "need",
    "responsible", "responsibilities", "qualifications", "qualification",
    "plus", "bonus", "excellent", "good", "great", "ideal", "candidate",
}

# ── Tech skill normalisation map ─────────────────────────────────
_NORMALISE = {
    r"c\+\+":       "cplusplus",
    r"c#":          "csharp",
    r"\.net":       "dotnet",
    r"node\.js":    "nodejs",
    r"react\.js":   "reactjs",
    r"vue\.js":     "vuejs",
    r"next\.js":    "nextjs",
    r"nuxt\.js":    "nuxtjs",
    r"express\.js": "expressjs",
    r"three\.js":   "threejs",
    r"ci/cd":       "cicd",
    r"rest api":    "restapi",
    r"api":         "api",
    r"ml":          "machinelearning",
    r"ai":          "artificialintelligence",
    r"dl":          "deeplearning",
    r"nlp":         "naturallanguageprocessing",
    r"cv":          "computervision",
    r"llm":         "largelanguagemodel",
    r"rag":         "retrievalaugmentedgeneration",
    r"db":          "database",
}

# ── Regex fallback stop words ─────────────────────────────────────
_REGEX_STOPS = {
    "a","an","the","and","or","but","in","on","at","to","for","of","with",
    "by","from","is","it","its","be","been","being","are","was","were",
    "have","has","had","do","does","did","will","would","could","should",
    "may","might","shall","can","need","not","no","nor","so","yet","both",
    "either","neither","each","every","all","any","both","few","more",
    "most","other","some","such","than","that","this","these","those",
    "which","who","whom","whose","what","when","where","why","how","into",
    "out","about","up","if","then","there","here","very","just","now",
    *_EXTRA_STOPS,
}


def _normalise_text(text: str) -> str:
    """Apply tech-term normalisation before tokenisation."""
    text = text.lower()
    for pattern, replacement in _NORMALISE.items():
        text = re.sub(pattern, replacement, text)
    return text


def preprocess(text: str, stem: bool = True, lemmatize: bool = True) -> list[str]:
    """
    Full NLP preprocessing pipeline.

    Parameters
    ----------
    text      : raw input string
    stem      : apply Porter stemming (default True)
    lemmatize : apply WordNet lemmatisation before stemming (default True)

    Returns
    -------
    List of processed tokens.
    """
    text = _normalise_text(text)

    if _NLTK_AVAILABLE:
        tokens = _tokenize(text)
        stops  = _stop_words | _EXTRA_STOPS
        tokens = [t for t in tokens
                  if t.isalnum() and t not in stops and len(t) > 1]
        if lemmatize:
            tokens = [_lemmatizer.lemmatize(t) for t in tokens]
        if stem:
            tokens = [_stemmer.stem(t) for t in tokens]
    else:
        # Regex fallback
        tokens = re.findall(r"[a-z0-9]+", text)
        tokens = [t for t in tokens
                  if t not in _REGEX_STOPS and len(t) > 1]

    return tokens


def preprocess_for_tfidf(text: str) -> str:
    """
    Return a single string of preprocessed tokens suitable for
    sklearn's TfidfVectorizer (which does its own tokenisation).
    We still apply normalisation + stop-word removal here.
    """
    text = _normalise_text(text)

    if _NLTK_AVAILABLE:
        tokens = _tokenize(text)
        stops  = _stop_words | _EXTRA_STOPS
        tokens = [_lemmatizer.lemmatize(t)
                  for t in tokens
                  if t.isalnum() and t not in stops and len(t) > 1]
    else:
        tokens = re.findall(r"[a-z0-9]+", text)
        tokens = [t for t in tokens
                  if t not in _REGEX_STOPS and len(t) > 1]

    return " ".join(tokens)


def extract_noun_phrases(text: str) -> list[str]:
    """
    Lightweight noun-phrase extraction.
    Uses NLTK POS tagging when available; falls back to regex.
    Returns bigrams/trigrams that look like skill phrases.
    """
    phrases: list[str] = []

    if _NLTK_AVAILABLE:
        try:
            from nltk import pos_tag
            tokens = _tokenize(text.lower())
            tagged = pos_tag(tokens)
            # Simple chunker: consecutive NN/NNP/NNS or JJ+NN sequences
            chunk: list[str] = []
            for word, tag in tagged:
                if tag in ("NN", "NNP", "NNS", "NNPS", "JJ") and word.isalpha():
                    chunk.append(word)
                else:
                    if 2 <= len(chunk) <= 3:
                        phrases.append(" ".join(chunk))
                    chunk = []
            if 2 <= len(chunk) <= 3:
                phrases.append(" ".join(chunk))
        except Exception:
            pass

    # Fallback: extract capitalised multi-word terms from original text
    for m in re.finditer(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+", text):
        phrases.append(m.group().lower())

    return list(set(phrases))
