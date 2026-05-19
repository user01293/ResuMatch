"""
app.py — ResuMatch v3 (Massive Dataset + Hybrid NLP)
Flask backend: auto-loads Kaggle 124k CSV or built-in 32-role dataset.
"""
from __future__ import annotations
import os, sys, json, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory
from data.dataset_loader import load_jobs
from utils.resume_parser import extract_resume_text
from utils.matcher import match_resume_to_jobs, _fit_corpus
from utils import embeddings as emb

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

# ── Load dataset & warm-up corpus at startup ─────────────────────
JOBS_DATASET, DATASET_SOURCE = load_jobs()
_fit_corpus(JOBS_DATASET)


@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/how-it-works')
def how_it_works():
    return send_from_directory('templates', 'bert_explainer.html')


@app.route('/api/match', methods=['POST'])
def match_resume():
    try:
        resume_text = ''
        filename    = 'resume.txt'

        if 'resume' in request.files:
            f = request.files['resume']
            if not f.filename:
                return jsonify({'error': 'No file selected'}), 400
            filename = f.filename
            data = f.read()
            if not data:
                return jsonify({'error': 'Empty file'}), 400
            resume_text = extract_resume_text(data, filename)

        elif request.is_json:
            body = request.get_json(force=True)
            resume_text = body.get('resume_text', '')
            filename    = body.get('filename', 'resume.txt')

        elif 'resume_text' in request.form:
            resume_text = request.form['resume_text']

        else:
            return jsonify({'error': 'No resume provided.'}), 400

        if not resume_text or len(resume_text.strip()) < 50:
            return jsonify({'error': 'Could not extract enough text. Please check the file is readable.'}), 400

        top_n = int(request.args.get('top_n', 10))
        matches, info = match_resume_to_jobs(resume_text, JOBS_DATASET, top_n=top_n)

        results = []
        for m in matches:
            job = m['job']
            results.append({
                'id':                job['id'],
                'title':             job['title'],
                'company':           job['company'],
                'location':          job['location'],
                'type':              job['type'],
                'salary':            job['salary'],
                'category':          job['category'],
                'experience':        job['experience'],
                'education':         job['education'],
                'description':       job['description'].strip()[:600] + '…',
                'source':            job.get('source', 'Built-in'),
                # scores
                'match_score':       m['match_score'],
                'tfidf_score':       m['tfidf_score'],
                'embed_score':       m['embed_score'],
                'skill_overlap_pct': m['skill_overlap_pct'],
                # skills
                'matched_skills':    m['matched_skills'],
                'missing_skills':    m['missing_skills'],
                'skill_match_count': m['skill_match_count'],
                'total_skills':      m['total_skills'],
            })

        return jsonify({
            'success': True,
            'resume_info': {
                'filename':         filename,
                'detected_skills':  info['skills'],
                'noun_phrases':     info.get('noun_phrases', []),
                'experience_years': info['experience_years'],
                'education':        info['education'],
                'skill_count':      info['skill_count'],
                'embedding_tier':   info['embedding_tier'],
                'weights':          info['weights'],
                'text_length':      len(resume_text),
            },
            'matches':             results,
            'total_jobs_analyzed': len(JOBS_DATASET),
            'dataset_source':      DATASET_SOURCE,
        })

    except Exception:
        traceback.print_exc()
        return jsonify({'error': 'Internal server error — see console.'}), 500


@app.route('/api/health')
def health():
    return jsonify({
        'status':           'ok',
        'jobs_loaded':      len(JOBS_DATASET),
        'dataset_source':   DATASET_SOURCE,
        'embedding_tier':   emb.get_tier_name(),
        'embedding_level':  emb.get_tier(),
    })


@app.route('/api/jobs')
def get_jobs():
    return jsonify({
        'jobs':   [{k: j[k] for k in ('id','title','company','location','category','salary','type')}
                   for j in JOBS_DATASET[:200]],   # cap response size
        'total':  len(JOBS_DATASET),
        'source': DATASET_SOURCE,
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f'\n🚀  ResuMatch v3 → http://localhost:{port}')
    print(f'📂  {len(JOBS_DATASET):,} jobs | {DATASET_SOURCE}')
    print(f'🤖  Embeddings: {emb.get_tier_name()}\n')
    app.run(debug=True, port=port, host='0.0.0.0')
