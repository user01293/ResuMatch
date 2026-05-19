"""
dataset_loader.py
─────────────────
Loads jobs from one of three sources (priority order):

  1. Kaggle LinkedIn Job Postings 2023-2024 (arshkon/linkedin-job-postings)
     → postings.csv  (~124,000 rows, real job data)
     → Place the CSV at:  data/postings.csv
     → Download from:  https://www.kaggle.com/datasets/arshkon/linkedin-job-postings

  2. Any generic CSV the user drops in data/jobs.csv
     → Must have columns: title, description  (others optional)

  3. Built-in curated dataset (32 hand-crafted roles)
     → Always available, no download required

Auto-detection: whichever file exists first wins.
"""

from __future__ import annotations
import os, re, csv, hashlib
from typing import Optional

_HERE = os.path.dirname(os.path.abspath(__file__))

KAGGLE_CSV  = os.path.join(_HERE, 'postings.csv')
GENERIC_CSV = os.path.join(_HERE, 'jobs.csv')

# Max rows from CSV (set None = load all ~124k; 10_000 is fast for demos)
MAX_ROWS: int | None = 10_000
MIN_DESC_LEN = 80   # discard stub postings


def _clean(text: str) -> str:
    if not text: return ''
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'&[a-z]+;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _safe(val) -> str:
    return '' if val is None else str(val).strip()


def _salary(row: dict) -> str:
    try:
        lo = float(row.get('min_salary') or 0)
        hi = float(row.get('max_salary') or 0)
        if lo > 0 and hi > 0:
            return f'${lo:,.0f} – ${hi:,.0f}'
        if hi > 0: return f'Up to ${hi:,.0f}'
        if lo > 0: return f'From ${lo:,.0f}'
    except (ValueError, TypeError):
        pass
    for col in ('salary', 'salary_range', 'compensation', 'med_salary'):
        v = _safe(row.get(col))
        if v and v not in ('0', '0.0', 'nan', 'None'): return v
    return 'Not disclosed'


def _category(title: str) -> str:
    t = title.lower()
    if any(k in t for k in ('machine learning','ml engineer','ai engineer','deep learning','nlp engineer')): return 'AI/ML'
    if any(k in t for k in ('data scientist','data science')): return 'AI/ML'
    if any(k in t for k in ('data engineer','etl','pipeline','spark','databricks')): return 'Data Engineering'
    if any(k in t for k in ('data analyst','bi analyst','business intelligence','reporting analyst')): return 'Data & Analytics'
    if any(k in t for k in ('frontend','front-end','front end','react developer','vue','angular')): return 'Frontend'
    if any(k in t for k in ('backend','back-end','back end','api developer')): return 'Backend'
    if any(k in t for k in ('full stack','fullstack','full-stack')): return 'Full Stack'
    if any(k in t for k in ('devops','site reliability','sre','platform engineer','cloud engineer','infrastructure engineer')): return 'DevOps & Cloud'
    if any(k in t for k in ('security','cybersecurity','infosec','penetration','soc analyst')): return 'Security'
    if any(k in t for k in ('product manager','product owner','program manager')): return 'Product'
    if any(k in t for k in ('ux designer','ui designer','ux/ui','user experience designer')): return 'Design'
    if any(k in t for k in ('mobile','ios developer','android developer','flutter','react native')): return 'Mobile'
    if any(k in t for k in ('marketing','seo','content writer','growth hacker')): return 'Marketing'
    if any(k in t for k in ('financial analyst','finance','accounting','controller')): return 'Finance'
    if any(k in t for k in ('hr ','human resource','recruiter','talent acquisition','people ops')): return 'Human Resources'
    if any(k in t for k in ('sales','account executive','business development','bdr','sdr')): return 'Sales'
    if any(k in t for k in ('scrum master','agile coach','project manager')): return 'Project Management'
    if any(k in t for k in ('embedded','firmware','iot','hardware engineer')): return 'Embedded / IoT'
    if any(k in t for k in ('blockchain','web3','solidity','smart contract')): return 'Blockchain'
    if any(k in t for k in ('software engineer','software developer','sde ','swe ')): return 'Engineering'
    return 'Engineering'


def _work_type(row: dict) -> str:
    for col in ('work_type', 'formatted_work_type', 'employment_type', 'job_type'):
        v = _safe(row.get(col))
        if v: return v.replace('_', ' ').title()
    return 'Full-time'


def _experience_level(row: dict) -> str:
    for col in ('experience_level', 'formatted_experience_level', 'seniority_level'):
        v = _safe(row.get(col))
        if v: return v.replace('_', ' ').title()
    return 'Not specified'


def _load_kaggle(path: str, max_rows: Optional[int]) -> list[dict]:
    jobs: list[dict] = []
    seen: set[str] = set()
    with open(path, newline='', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if max_rows and i >= max_rows:
                break
            title = _clean(_safe(row.get('title') or row.get('job_title', '')))
            desc  = _clean(_safe(row.get('description') or row.get('job_description', '')))
            if not title or not desc or len(desc) < MIN_DESC_LEN:
                continue
            h = hashlib.md5((title + desc[:200]).encode()).hexdigest()
            if h in seen: continue
            seen.add(h)
            jobs.append({
                'id':          len(jobs) + 1,
                'title':       title,
                'company':     _clean(_safe(row.get('company_name') or row.get('company', ''))) or 'Company',
                'location':    _clean(_safe(row.get('location') or row.get('job_location', ''))) or 'USA',
                'type':        _work_type(row),
                'salary':      _salary(row),
                'category':    _category(title),
                'experience':  _experience_level(row),
                'education':   'See description',
                'description': desc[:1500],
                'skills':      [],
                'source':      'LinkedIn (Kaggle 2023-2024)',
            })
    return jobs


def _load_generic(path: str, max_rows: Optional[int]) -> list[dict]:
    TITLE_COLS = ('title','job_title','position','job_name','role')
    DESC_COLS  = ('description','job_description','details','body','content','text')
    CO_COLS    = ('company','company_name','employer','organization')
    LOC_COLS   = ('location','city','job_location','state','place')

    def pick(row, cols):
        for c in cols:
            v = _safe(row.get(c))
            if v: return v
        return ''

    jobs: list[dict] = []
    with open(path, newline='', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if max_rows and i >= max_rows: break
            title = _clean(pick(row, TITLE_COLS))
            desc  = _clean(pick(row, DESC_COLS))
            if not title or not desc or len(desc) < MIN_DESC_LEN: continue
            jobs.append({
                'id':          len(jobs) + 1,
                'title':       title,
                'company':     _clean(pick(row, CO_COLS)) or 'Company',
                'location':    _clean(pick(row, LOC_COLS)) or 'Remote',
                'type':        _safe(row.get('type') or row.get('work_type', 'Full-time')),
                'salary':      _salary(row),
                'category':    _category(title),
                'experience':  _safe(row.get('experience', 'Not specified')),
                'education':   _safe(row.get('education', 'See description')),
                'description': desc[:1500],
                'skills':      [],
                'source':      'Custom CSV',
            })
    return jobs


def load_jobs(max_rows: Optional[int] = MAX_ROWS) -> tuple[list[dict], str]:
    """
    Returns (jobs_list, source_description_string).
    Tries Kaggle CSV → generic CSV → built-in dataset.
    """
    if os.path.exists(KAGGLE_CSV):
        print(f'[Dataset] Found Kaggle CSV: {KAGGLE_CSV}')
        try:
            jobs = _load_kaggle(KAGGLE_CSV, max_rows)
            if jobs:
                src = f'Kaggle LinkedIn Postings 2023-24 ({len(jobs):,} jobs loaded)'
                print(f'[Dataset] ✅  {src}')
                return jobs, src
        except Exception as e:
            print(f'[Dataset] ⚠️  Kaggle CSV parse failed: {e}')

    if os.path.exists(GENERIC_CSV):
        print(f'[Dataset] Found generic CSV: {GENERIC_CSV}')
        try:
            jobs = _load_generic(GENERIC_CSV, max_rows)
            if jobs:
                src = f'Custom CSV ({len(jobs):,} jobs loaded)'
                print(f'[Dataset] ✅  {src}')
                return jobs, src
        except Exception as e:
            print(f'[Dataset] ⚠️  Generic CSV parse failed: {e}')

    print('[Dataset] No CSV found — using built-in 32-role dataset.')
    print('[Dataset] 💡 For 124k real jobs, download Kaggle dataset:')
    print('[Dataset]    https://www.kaggle.com/datasets/arshkon/linkedin-job-postings')
    print('[Dataset]    Place postings.csv in the data/ folder and restart.')
    from data.jobs_dataset import JOBS_DATASET
    return JOBS_DATASET, 'Built-in curated dataset (32 roles)'
