import streamlit as st
from transformers import pipeline
import random

st.set_page_config(
    page_title="Cinelytix",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@300;400;500;600&display=swap');

* { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem; max-width: 1400px; }

.stApp { background: #06060e; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a18 0%, #0d0d1f 100%) !important;
    border-right: 1px solid #1e1e3a;
}

.nav-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 1.5rem 0 0.3rem;
    display: block;
    letter-spacing: -0.5px;
}

.nav-sub {
    font-size: 9px;
    letter-spacing: 0.2em;
    color: #3a3a5a !important;
    text-transform: uppercase;
    margin-bottom: 2rem;
    display: block;
}

.nav-stat {
    font-size: 11px;
    color: #3a3a5a !important;
    margin-top: 4px;
    display: block;
}

.stButton button {
    background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
    color: #fff !important;
    font-weight: 500 !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, #8b5cf6, #6d28d9) !important;
    transform: translateY(-1px) !important;
}

.stTextArea textarea {
    background: #0d0d1f !important;
    border: 1px solid #1e1e3a !important;
    border-radius: 12px !important;
    color: #e8e4f0 !important;
    font-size: 14px !important;
}

.stTextInput input {
    background: #0d0d1f !important;
    border: 1px solid #1e1e3a !important;
    border-radius: 10px !important;
    color: #e8e4f0 !important;
    font-size: 14px !important;
}

.stSelectbox select {
    background: #0d0d1f !important;
    border: 1px solid #1e1e3a !important;
    color: #e8e4f0 !important;
}

.hero-section {
    background: linear-gradient(135deg, #0d0d1f 0%, #12103a 50%, #0d0d1f 100%);
    border: 1px solid #1e1e3a;
    border-radius: 24px;
    padding: 3rem 3rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero-glow {
    position: absolute;
    top: -50px; right: -50px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(124,58,237,0.15), transparent);
    border-radius: 50%;
}

.hero-glow2 {
    position: absolute;
    bottom: -80px; left: -80px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(139,92,246,0.08), transparent);
    border-radius: 50%;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}

.hero-sub {
    font-size: 14px;
    color: #6060a0;
    margin-bottom: 2rem;
    letter-spacing: 0.05em;
}

.hero-badge {
    display: inline-block;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    color: #a78bfa;
    font-size: 11px;
    padding: 4px 14px;
    border-radius: 20px;
    margin-right: 8px;
    margin-bottom: 8px;
    letter-spacing: 0.05em;
}

.stat-card {
    background: linear-gradient(135deg, #0d0d1f, #10102a);
    border: 1px solid #1e1e3a;
    border-radius: 16px;
    padding: 1.25rem;
    text-align: center;
    transition: border-color 0.3s;
}

.stat-card:hover { border-color: #7c3aed; }

.stat-val {
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
    background: linear-gradient(135deg, #a78bfa, #7c3aed);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-lbl {
    font-size: 10px;
    color: #3a3a5a;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 5px;
}

.movie-card {
    background: linear-gradient(135deg, #0d0d1f, #0f0f22);
    border: 1px solid #1e1e3a;
    border-radius: 18px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s;
}

.movie-card:hover {
    border-color: #7c3aed;
    transform: translateY(-2px);
}

.movie-title {
    font-size: 16px;
    font-weight: 600;
    color: #e8e4f0;
    margin-bottom: 4px;
    font-family: 'Playfair Display', serif;
}

.movie-meta {
    font-size: 10px;
    color: #3a3a5a;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 12px;
}

.badge-pos {
    display: inline-block;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    color: #a78bfa;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.badge-neg {
    display: inline-block;
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.25);
    color: #f87171;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.badge-mix {
    display: inline-block;
    background: rgba(251,191,36,0.1);
    border: 1px solid rgba(251,191,36,0.25);
    color: #fbbf24;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.score-pos { color: #a78bfa; font-size: 2rem; font-weight: 700; font-family: 'Playfair Display', serif; }
.score-mix { color: #fbbf24; font-size: 2rem; font-weight: 700; font-family: 'Playfair Display', serif; }
.score-neg { color: #f87171; font-size: 2rem; font-weight: 700; font-family: 'Playfair Display', serif; }

.progress-wrap {
    background: #1a1a2e;
    border-radius: 50px;
    height: 6px;
    overflow: hidden;
    margin: 10px 0;
}

.progress-pos { height: 100%; background: linear-gradient(90deg, #5b21b6, #a78bfa); border-radius: 50px; }
.progress-mix { height: 100%; background: linear-gradient(90deg, #b45309, #fbbf24); border-radius: 50px; }
.progress-neg { height: 100%; background: linear-gradient(90deg, #991b1b, #f87171); border-radius: 50px; }

.trend-tag-up     { font-size:9px; padding:2px 8px; border-radius:4px; background:#1a0a3a; color:#a78bfa; border:1px solid #3a1a6a; font-weight:600; letter-spacing:0.08em; }
.trend-tag-steady { font-size:9px; padding:2px 8px; border-radius:4px; background:#1a180a; color:#fbbf24; border:1px solid #3a320a; font-weight:600; letter-spacing:0.08em; }
.trend-tag-down   { font-size:9px; padding:2px 8px; border-radius:4px; background:#1a0a0a; color:#f87171; border:1px solid #3a1a1a; font-weight:600; letter-spacing:0.08em; }

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #e8e4f0;
    margin: 1.5rem 0 1rem;
    border-left: 3px solid #7c3aed;
    padding-left: 12px;
}

.page-header {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    background: linear-gradient(135deg, #ffffff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 1.5rem 0 0.3rem;
    font-weight: 700;
}

.page-sub {
    font-size: 13px;
    color: #3a3a5a;
    margin-bottom: 1.5rem;
    letter-spacing: 0.03em;
}

.result-pos {
    background: linear-gradient(135deg, #0a0820, #120a35);
    border: 2px solid #7c3aed;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
}

.result-neg {
    background: linear-gradient(135deg, #1a0808, #2a0f0f);
    border: 2px solid #ef4444;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
}

.search-result-card {
    background: linear-gradient(135deg, #0d0d1f, #0f0f22);
    border: 1px solid #7c3aed;
    border-radius: 18px;
    padding: 1.5rem 2rem;
    margin-top: 1rem;
    text-align: center;
}

.watchlist-row {
    background: linear-gradient(135deg, #0d0d1f, #0f0f22);
    border: 1px solid #1e1e3a;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.5rem;
}

.footer {
    text-align: center;
    padding: 2rem;
    border-top: 1px solid #1a1a2e;
    color: #1e1e3a;
    font-size: 11px;
    margin-top: 3rem;
    letter-spacing: 0.05em;
    line-height: 2;
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────
MOVIES = [
    {"title": "Dune: Part Two",             "genre": "SCI-FI",      "year": 2024, "score": 91, "trend": "up",     "change": "+14%"},
    {"title": "Oppenheimer",                "genre": "DRAMA",       "year": 2023, "score": 88, "trend": "steady", "change": "+2%"},
    {"title": "Poor Things",                "genre": "FANTASY",     "year": 2023, "score": 85, "trend": "up",     "change": "+9%"},
    {"title": "The Zone of Interest",       "genre": "HISTORICAL",  "year": 2023, "score": 79, "trend": "steady", "change": "+1%"},
    {"title": "Saltburn",                   "genre": "THRILLER",    "year": 2023, "score": 62, "trend": "down",   "change": "-5%"},
    {"title": "Past Lives",                 "genre": "ROMANCE",     "year": 2023, "score": 94, "trend": "up",     "change": "+7%"},
    {"title": "Killers of the Flower Moon", "genre": "WESTERN",     "year": 2023, "score": 83, "trend": "steady", "change": "+3%"},
    {"title": "Priscilla",                  "genre": "BIOGRAPHY",   "year": 2023, "score": 71, "trend": "down",   "change": "-3%"},
    {"title": "The Holdovers",              "genre": "COMEDY",      "year": 2023, "score": 89, "trend": "up",     "change": "+11%"},
    {"title": "Inception",                  "genre": "SCI-FI",      "year": 2010, "score": 95, "trend": "up",     "change": "+5%"},
    {"title": "The Dark Knight",            "genre": "ACTION",      "year": 2008, "score": 97, "trend": "up",     "change": "+3%"},
    {"title": "Parasite",                   "genre": "THRILLER",    "year": 2019, "score": 93, "trend": "steady", "change": "+1%"},
    {"title": "Joker",                      "genre": "DRAMA",       "year": 2019, "score": 68, "trend": "steady", "change": "0%"},
    {"title": "Avatar",                     "genre": "SCI-FI",      "year": 2009, "score": 72, "trend": "down",   "change": "-2%"},
    {"title": "Interstellar",               "genre": "SCI-FI",      "year": 2014, "score": 91, "trend": "up",     "change": "+4%"},
]

# ── Session State ──────────────────────────────────────────────────────
if "watchlist"  not in st.session_state: st.session_state.watchlist  = []
if "page"       not in st.session_state: st.session_state.page       = "Home"
if "analyzed"   not in st.session_state: st.session_state.analyzed   = []
if "search_res" not in st.session_state: st.session_state.search_res = None

# ── Model ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="Samantha-16/movie-sentiment-distilbert"
    )
classifier = load_model()

# ── Helpers ────────────────────────────────────────────────────────────
def badge(score):
    if score >= 75: return "badge-pos", "Positive"
    if score >= 50: return "badge-mix", "Mixed"
    return "badge-neg", "Negative"

def score_cls(score):
    if score >= 75: return "score-pos"
    if score >= 50: return "score-mix"
    return "score-neg"

def bar_cls(score):
    if score >= 75: return "progress-pos"
    if score >= 50: return "progress-mix"
    return "progress-neg"

def trend_html(trend, change):
    cls = f"trend-tag-{trend}"
    icon = {"up":"↑","steady":"→","down":"↓"}[trend]
    return f"<span class='{cls}'>{icon} {change}</span>"

def search_movie(query):
    query_lower = query.lower()
    for m in MOVIES:
        if query_lower in m["title"].lower():
            return m
    return None

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<span class='nav-logo'>Cinelytix</span>", unsafe_allow_html=True)
    st.markdown("<span class='nav-sub'>Cinematic Intelligence Platform</span>", unsafe_allow_html=True)

    pages = {
        "Home":              "🏠  Home",
        "Search":            "🔍  Search Movies",
        "Sentiment":         "🎬  Sentiment Analysis",
        "Trending":          "📈  Trending Movies",
        "Watchlist":         "⭐  My Watchlist",
    }

    for key, label in pages.items():
        if st.button(label, use_container_width=True, key=f"nav_{key}"):
            st.session_state.page = key

    st.markdown("---")
    st.markdown(f"<span class='nav-stat'>Watchlist: {len(st.session_state.watchlist)} films</span>", unsafe_allow_html=True)
    st.markdown(f"<span class='nav-stat'>Analyzed: {len(st.session_state.analyzed)} reviews</span>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════
if st.session_state.page == "Home":

    st.markdown("""
    <div class='hero-section'>
        <div class='hero-glow'></div>
        <div class='hero-glow2'></div>
        <div class='hero-title'>The Pulse of Cinema</div>
        <div class='hero-sub'>
            AI-powered sentiment intelligence across the cinematic landscape
        </div>
        <div>
            <span class='hero-badge'>DistilBERT</span>
            <span class='hero-badge'>86.4% Accuracy</span>
            <span class='hero-badge'>66M Parameters</span>
            <span class='hero-badge'>Real-time Analysis</span>
            <span class='hero-badge'>IMDB Trained</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='stat-card'><div class='stat-val'>86.4%</div><div class='stat-lbl'>Model Accuracy</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='stat-card'><div class='stat-val'>66M</div><div class='stat-lbl'>Parameters</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card'><div class='stat-val'>{len(MOVIES)}</div><div class='stat-lbl'>Films Tracked</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='stat-card'><div class='stat-val'>{len(st.session_state.analyzed)}</div><div class='stat-lbl'>Reviews Analyzed</div></div>", unsafe_allow_html=True)

    # Quick search on homepage
    st.markdown("<div class='section-title'>Quick Search</div>", unsafe_allow_html=True)
    col_s, col_b = st.columns([4, 1])
    with col_s:
        home_query = st.text_input("", placeholder="Search a movie title — e.g. Inception, Dune, Parasite...", label_visibility="collapsed")
    with col_b:
        if st.button("Search", use_container_width=True):
            if home_query:
                result = search_movie(home_query)
                st.session_state.search_res = result
                st.session_state.search_query = home_query

    if st.session_state.search_res:
        m = st.session_state.search_res
        b_cls, b_txt = badge(m["score"])
        st.markdown(f"""
        <div class='search-result-card'>
            <div style='font-size:11px;color:#3a3a5a;text-transform:uppercase;
                        letter-spacing:0.15em;margin-bottom:8px;'>Search Result</div>
            <div style='font-family:"Playfair Display",serif;font-size:1.8rem;
                        color:#e8e4f0;font-weight:700;margin-bottom:4px;'>
                {m['title']}
            </div>
            <div style='font-size:11px;color:#3a3a5a;text-transform:uppercase;
                        letter-spacing:0.1em;margin-bottom:16px;'>
                {m['genre']} · {m['year']}
            </div>
            <span class='{b_cls}'>{b_txt}</span>
            <div class='{score_cls(m["score"])}' style='font-size:3rem;
                        margin:12px 0 4px;'>
                {m['score']}%
            </div>
            <div style='font-size:12px;color:#3a3a5a;margin-bottom:16px;'>
                Positive reviews
            </div>
            <div class='progress-wrap' style='max-width:400px;margin:0 auto 16px;'>
                <div class='{bar_cls(m["score"])}' style='width:{m["score"]}%;'></div>
            </div>
            {trend_html(m['trend'], m['change'])}
        </div>
        """, unsafe_allow_html=True)

    elif "search_query" in st.session_state and st.session_state.get("search_res") is None:
        st.info(f"No results found for '{st.session_state.search_query}'. Try Inception, Dune, or Oppenheimer.")

    # Top picks
    st.markdown("<div class='section-title'>Top Rated This Week</div>", unsafe_allow_html=True)
    top = sorted(MOVIES, key=lambda x: x["score"], reverse=True)[:3]
    cols = st.columns(3)
    for i, m in enumerate(top):
        b_cls, b_txt = badge(m["score"])
        with cols[i]:
            st.markdown(f"""
            <div class='movie-card'>
                <div class='movie-title'>{m['title']}</div>
                <div class='movie-meta'>{m['genre']} · {m['year']}</div>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <span class='{b_cls}'>{b_txt}</span>
                    <span class='{score_cls(m["score"])}'>{m['score']}%</span>
                </div>
                <div class='progress-wrap'>
                    <div class='{bar_cls(m["score"])}' style='width:{m["score"]}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# SEARCH PAGE
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Search":

    st.markdown("<div class='page-header'>Search Movies</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Search any movie to see its sentiment score and review breakdown</div>", unsafe_allow_html=True)

    col_s, col_b = st.columns([4, 1])
    with col_s:
        query = st.text_input("", placeholder="Type a movie title...", label_visibility="collapsed")
    with col_b:
        search_btn = st.button("Search", use_container_width=True)

    if search_btn and query:
        result = search_movie(query)
        if result:
            m = result
            b_cls, b_txt = badge(m["score"])
            pos  = m["score"]
            neg  = 100 - pos
            mix  = max(0, min(20, 100 - pos - max(0, neg - 10)))
            neg  = 100 - pos - mix

            st.markdown(f"""
            <div class='search-result-card' style='text-align:left;padding:2rem;'>
                <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                    <div>
                        <div style='font-family:"Playfair Display",serif;
                                    font-size:1.8rem;color:#e8e4f0;
                                    font-weight:700;margin-bottom:4px;'>
                            {m['title']}
                        </div>
                        <div style='font-size:11px;color:#3a3a5a;
                                    text-transform:uppercase;letter-spacing:0.1em;
                                    margin-bottom:12px;'>
                            {m['genre']} · {m['year']}
                        </div>
                        <span class='{b_cls}'>{b_txt}</span>
                        {trend_html(m['trend'], m['change'])}
                    </div>
                    <div class='{score_cls(m["score"])}' style='font-size:3.5rem;
                                font-family:"Playfair Display",serif;font-weight:700;'>
                        {m['score']}%
                    </div>
                </div>
                <div style='margin-top:1.5rem;'>
                    <div style='display:flex;justify-content:space-between;
                                font-size:12px;color:#3a3a5a;margin-bottom:4px;'>
                        <span>Positive reviews</span><span>{pos}%</span>
                    </div>
                    <div class='progress-wrap'>
                        <div class='progress-pos' style='width:{pos}%;'></div>
                    </div>
                    <div style='display:flex;justify-content:space-between;
                                font-size:12px;color:#3a3a5a;margin:8px 0 4px;'>
                        <span>Mixed reviews</span><span>{mix}%</span>
                    </div>
                    <div class='progress-wrap'>
                        <div class='progress-mix' style='width:{mix}%;'></div>
                    </div>
                    <div style='display:flex;justify-content:space-between;
                                font-size:12px;color:#3a3a5a;margin:8px 0 4px;'>
                        <span>Negative reviews</span><span>{neg}%</span>
                    </div>
                    <div class='progress-wrap'>
                        <div class='progress-neg' style='width:{neg}%;'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_w, col_a = st.columns(2)
            with col_w:
                if st.button("+ Add to Watchlist", use_container_width=True):
                    if m["title"] not in [w["title"] for w in st.session_state.watchlist]:
                        st.session_state.watchlist.append({"title": m["title"], "status": "Want to Watch", "sentiment": f"{m['score']}%"})
                        st.success(f"Added '{m['title']}' to watchlist!")
            with col_a:
                if st.button("Analyze a Review →", use_container_width=True):
                    st.session_state.page = "Sentiment"
                    st.rerun()
        else:
            st.markdown(f"""
            <div style='background:#0d0d1f;border:1px dashed #1e1e3a;
                        border-radius:16px;padding:2rem;text-align:center;
                        margin-top:1rem;'>
                <div style='font-size:32px;margin-bottom:8px;'>🔍</div>
                <div style='color:#3a3a5a;font-size:13px;'>
                    No results for "{query}".<br>
                    Try: Inception, Dune, Oppenheimer, Parasite, Joker
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Browse all
    st.markdown("<div class='section-title'>Browse All Films</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for i, m in enumerate(MOVIES):
        b_cls, b_txt = badge(m["score"])
        with cols[i % 3]:
            st.markdown(f"""
            <div class='movie-card'>
                <div class='movie-title'>{m['title']}</div>
                <div class='movie-meta'>{m['genre']} · {m['year']}</div>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;'>
                    <span class='{b_cls}'>{b_txt}</span>
                    <span class='{score_cls(m["score"])}'>{m['score']}%</span>
                </div>
                <div class='progress-wrap'>
                    <div class='{bar_cls(m["score"])}' style='width:{m["score"]}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"+ Watchlist", key=f"sw{i}", use_container_width=True):
                if m["title"] not in [w["title"] for w in st.session_state.watchlist]:
                    st.session_state.watchlist.append({"title": m["title"], "status": "Want to Watch", "sentiment": f"{m['score']}%"})
                    st.success(f"Added '{m['title']}'!")

# ══════════════════════════════════════════════════════════════════════
# SENTIMENT ANALYSIS
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Sentiment":

    st.markdown("<div class='page-header'>Sentiment Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Analyze any movie review with DistilBERT AI · 86.4% accuracy</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='stat-card'><div class='stat-val'>86.4%</div><div class='stat-lbl'>Accuracy</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='stat-card'><div class='stat-val'>66M</div><div class='stat-lbl'>Parameters</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card'><div class='stat-val'>{len(st.session_state.analyzed)}</div><div class='stat-lbl'>Reviews Done</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='stat-card'><div class='stat-val'>F1 0.86</div><div class='stat-lbl'>F1 Score</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Analyze a Review</div>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1.3, 1])

    with col_l:
        movie_name = st.text_input("", placeholder="Movie title (optional)...", label_visibility="collapsed", key="mname")
        review     = st.text_area("", placeholder="Paste any movie review here...", height=160, label_visibility="collapsed")

        col_a, col_w = st.columns(2)
        with col_a:
            analyze = st.button("Analyze Sentiment", use_container_width=True)
        with col_w:
            if st.button("+ Watchlist", use_container_width=True) and movie_name:
                if movie_name not in [w["title"] for w in st.session_state.watchlist]:
                    st.session_state.watchlist.append({"title": movie_name, "status": "Want to Watch", "sentiment": "—"})
                    st.success(f"Added '{movie_name}'!")

        st.markdown("<div style='margin-top:1rem;font-size:10px;color:#3a3a5a;text-transform:uppercase;letter-spacing:0.15em;'>Sample reviews</div>", unsafe_allow_html=True)
        samples = [
            "This movie was absolutely brilliant!",
            "Terrible film. Complete waste of time.",
            "A masterpiece of modern cinema.",
            "The plot made no sense whatsoever.",
            "Stunning visuals, weak story.",
            "One of the best I have ever seen!",
        ]
        r1 = st.columns(3)
        for i, s in enumerate(samples[:3]):
            if r1[i].button(s[:20]+"...", key=f"sa{i}"):
                st.session_state["picked"] = s
        r2 = st.columns(3)
        for i, s in enumerate(samples[3:]):
            if r2[i].button(s[:20]+"...", key=f"sb{i}"):
                st.session_state["picked"] = s
        if "picked" in st.session_state:
            review = st.session_state["picked"]

    with col_r:
        if analyze and review.strip():
            with st.spinner("Analyzing..."):
                res   = classifier(review)[0]
                label = "POSITIVE" if res["label"] == "LABEL_1" else "NEGATIVE"
                conf  = round(res["score"] * 100, 2)

            st.session_state.analyzed.append({"review": review[:60], "label": label, "confidence": conf, "movie": movie_name or "Unknown"})

            if label == "POSITIVE":
                st.markdown(f"""
                <div class='result-pos'>
                    <div style='font-size:44px;margin-bottom:8px;'>🎬</div>
                    <div style='font-size:28px;font-weight:700;color:#a78bfa;
                                letter-spacing:3px;margin-bottom:6px;'>POSITIVE</div>
                    <div style='color:#7c5cbf;font-size:12px;margin-bottom:20px;'>
                        Positive sentiment detected
                    </div>
                    <div style='background:#120830;border-radius:50px;height:8px;
                                overflow:hidden;margin:0 auto 12px;max-width:300px;'>
                        <div style='width:{conf}%;height:100%;
                                    background:linear-gradient(90deg,#5b21b6,#a78bfa);
                                    border-radius:50px;'></div>
                    </div>
                    <div style='font-size:2.5rem;font-weight:700;color:#a78bfa;
                                font-family:"Playfair Display",serif;'>{conf}%</div>
                    <div style='font-size:11px;color:#3a3a5a;margin-top:4px;'>
                        Confidence score
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-neg'>
                    <div style='font-size:44px;margin-bottom:8px;'>🎭</div>
                    <div style='font-size:28px;font-weight:700;color:#f87171;
                                letter-spacing:3px;margin-bottom:6px;'>NEGATIVE</div>
                    <div style='color:#bf5c5c;font-size:12px;margin-bottom:20px;'>
                        Negative sentiment detected
                    </div>
                    <div style='background:#1a0808;border-radius:50px;height:8px;
                                overflow:hidden;margin:0 auto 12px;max-width:300px;'>
                        <div style='width:{conf}%;height:100%;
                                    background:linear-gradient(90deg,#991b1b,#f87171);
                                    border-radius:50px;'></div>
                    </div>
                    <div style='font-size:2.5rem;font-weight:700;color:#f87171;
                                font-family:"Playfair Display",serif;'>{conf}%</div>
                    <div style='font-size:11px;color:#3a3a5a;margin-top:4px;'>
                        Confidence score
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:#0d0d1f;border:1px dashed #1e1e3a;
                        border-radius:20px;padding:3rem;text-align:center;'>
                <div style='font-size:44px;margin-bottom:12px;'>🎬</div>
                <div style='color:#2a2a4a;font-size:13px;'>
                    Enter a review and click Analyze
                </div>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.analyzed:
        st.markdown("<div class='section-title'>Recent Analysis</div>", unsafe_allow_html=True)
        for item in reversed(st.session_state.analyzed[-3:]):
            lbl_col = "#a78bfa" if item["label"] == "POSITIVE" else "#f87171"
            b_cls   = "badge-pos" if item["label"] == "POSITIVE" else "badge-neg"
            st.markdown(f"""
            <div class='movie-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <div style='font-size:12px;color:#3a3a5a;margin-bottom:3px;'>
                            {item['movie']}
                        </div>
                        <div style='font-size:13px;color:#c0bcd0;'>
                            "{item['review']}..."
                        </div>
                    </div>
                    <div style='text-align:right;margin-left:1rem;flex-shrink:0;'>
                        <span class='{b_cls}'>{item['label']}</span>
                        <div style='font-size:1.3rem;font-weight:700;
                                    color:{lbl_col};margin-top:4px;'>
                            {item['confidence']}%
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TRENDING
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Trending":

    st.markdown("<div class='page-header'>Trending Movies</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Real-time sentiment scores across top films this week</div>", unsafe_allow_html=True)

    pos_c  = sum(1 for m in MOVIES if m["score"] >= 75)
    mix_c  = sum(1 for m in MOVIES if 50 <= m["score"] < 75)
    neg_c  = sum(1 for m in MOVIES if m["score"] < 50)
    avg_s  = round(sum(m["score"] for m in MOVIES) / len(MOVIES))

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='stat-card'><div class='stat-val'>{avg_s}%</div><div class='stat-lbl'>Avg Sentiment</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stat-card'><div class='stat-val'>{pos_c}</div><div class='stat-lbl'>Positive</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-card'><div class='stat-val'>{mix_c}</div><div class='stat-lbl'>Mixed</div></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='stat-card'><div class='stat-val'>{neg_c}</div><div class='stat-lbl'>Negative</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Now Trending</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for i, m in enumerate(MOVIES):
        b_cls, b_txt = badge(m["score"])
        with cols[i % 3]:
            st.markdown(f"""
            <div class='movie-card'>
                <div style='display:flex;justify-content:space-between;
                            align-items:flex-start;margin-bottom:10px;'>
                    <div>
                        <div class='movie-title'>{m['title']}</div>
                        <div class='movie-meta'>{m['genre']} · {m['year']}</div>
                    </div>
                    {trend_html(m['trend'], m['change'])}
                </div>
                <div style='display:flex;justify-content:space-between;
                            align-items:center;margin-bottom:8px;'>
                    <span class='{b_cls}'>{b_txt}</span>
                    <span class='{score_cls(m["score"])}'>{m['score']}%</span>
                </div>
                <div class='progress-wrap'>
                    <div class='{bar_cls(m["score"])}' style='width:{m["score"]}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("+ Watchlist", key=f"tw{i}", use_container_width=True):
                if m["title"] not in [w["title"] for w in st.session_state.watchlist]:
                    st.session_state.watchlist.append({"title": m["title"], "status": "Want to Watch", "sentiment": f"{m['score']}%"})
                    st.success(f"Added '{m['title']}'!")
                else:
                    st.info("Already in watchlist!")

# ══════════════════════════════════════════════════════════════════════
# WATCHLIST
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Watchlist":

    st.markdown("<div class='page-header'>My Watchlist</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Track and manage your personal film collection</div>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([2.5, 1.5, 1])
    with col_a:
        new_film = st.text_input("", placeholder="Add a movie title...", label_visibility="collapsed")
    with col_b:
        new_status = st.selectbox("", ["Want to Watch", "Watching", "Watched"], label_visibility="collapsed")
    with col_c:
        if st.button("Add", use_container_width=True):
            if new_film:
                if new_film not in [w["title"] for w in st.session_state.watchlist]:
                    st.session_state.watchlist.append({"title": new_film, "status": new_status, "sentiment": "—"})
                    st.success(f"Added '{new_film}'!")
                else:
                    st.warning("Already in watchlist!")

    if st.session_state.watchlist:
        want  = sum(1 for w in st.session_state.watchlist if w["status"] == "Want to Watch")
        watch = sum(1 for w in st.session_state.watchlist if w["status"] == "Watching")
        done  = sum(1 for w in st.session_state.watchlist if w["status"] == "Watched")

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-card'><div class='stat-val'>{want}</div><div class='stat-lbl'>Want to Watch</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-card'><div class='stat-val'>{watch}</div><div class='stat-lbl'>Watching</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-card'><div class='stat-val'>{done}</div><div class='stat-lbl'>Watched</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>My Films</div>", unsafe_allow_html=True)

        for i, film in enumerate(st.session_state.watchlist):
            sc = {"Watched": "#a78bfa", "Watching": "#fbbf24", "Want to Watch": "#4a4a8a"}.get(film["status"], "#888")
            c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 0.5])
            with c1:
                st.markdown(f"""
                <div style='padding:10px 0;'>
                    <div style='font-size:14px;font-weight:600;
                                color:#e8e4f0;font-family:"Playfair Display",serif;'>
                        {film['title']}
                    </div>
                    <div style='font-size:11px;color:#3a3a5a;margin-top:2px;'>
                        Sentiment: {film['sentiment']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style='padding:10px 0;'>
                    <span style='background:#0d0d1f;border:1px solid {sc}33;
                                 color:{sc};font-size:11px;
                                 padding:4px 10px;border-radius:20px;'>
                        {film['status']}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                ns = st.selectbox("", ["Want to Watch","Watching","Watched"],
                    index=["Want to Watch","Watching","Watched"].index(film["status"]),
                    key=f"sel{i}", label_visibility="collapsed")
                if ns != film["status"]:
                    st.session_state.watchlist[i]["status"] = ns
                    st.rerun()
            with c4:
                if st.button("✕", key=f"del{i}"):
                    st.session_state.watchlist.pop(i)
                    st.rerun()
            st.markdown("<hr style='border-color:#1a1a2e;margin:2px 0;'>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:#0d0d1f;border:1px dashed #1e1e3a;
                    border-radius:16px;padding:3rem;text-align:center;'>
            <div style='font-size:40px;margin-bottom:12px;'>⭐</div>
            <div style='color:#2a2a4a;font-size:13px;'>
                Your watchlist is empty.<br>
                Add films from Search or Trending pages.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    © 2026 Samantha Jessica Monis · All rights reserved<br>
    Cinelytix · AI Movie Sentiment Intelligence · Built with DistilBERT · Fine-tuned on IMDB · 86.4% Accuracy<br>
    <a href='https://huggingface.co/Samantha-16/movie-sentiment-distilbert'
       style='color:#2a2a4a;text-decoration:none;'>
        Model: Samantha-16/movie-sentiment-distilbert
    </a>
</div>
""", unsafe_allow_html=True)
