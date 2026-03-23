import streamlit as st
from transformers import pipeline
import requests
import datetime
import hashlib
import csv
import io

st.set_page_config(
    page_title="Cinelytix",
    page_icon="🎬",
    layout="wide"
)

OMDB_KEY = "YOUR_KEY_HERE"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@300;400;500;600&display=swap');

* { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem; max-width: 1400px; }

.stApp { background: #f8f8f6; }

section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #ebebeb;
}

.nav-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #1a1a1a;
    padding: 1.5rem 0 0.3rem;
    display: block;
    letter-spacing: -0.5px;
}

.nav-sub {
    font-size: 9px;
    letter-spacing: 0.2em;
    color: #aaaaaa !important;
    text-transform: uppercase;
    margin-bottom: 2rem;
    display: block;
}

.nav-stat {
    font-size: 11px;
    color: #aaaaaa !important;
    margin-top: 4px;
    display: block;
}

.stButton button {
    background: #1a1a1a !important;
    color: #ffffff !important;
    font-weight: 500 !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    transition: all 0.2s !important;
}

.stButton button:hover {
    background: #333333 !important;
    transform: translateY(-1px) !important;
}

.stTextArea textarea {
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 10px !important;
    color: #1a1a1a !important;
    font-size: 14px !important;
}

.stTextInput input {
    background: #ffffff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 8px !important;
    color: #1a1a1a !important;
    font-size: 14px !important;
}

.hero-section {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 20px;
    padding: 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero-accent {
    position: absolute;
    top: 0; right: 0;
    width: 300px; height: 300px;
    background: radial-gradient(circle at top right,
        rgba(99,102,241,0.06), transparent 70%);
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}

.hero-title span { color: #6366f1; }

.hero-sub {
    font-size: 14px;
    color: #888888;
    margin-bottom: 2rem;
    line-height: 1.7;
}

.hero-badge {
    display: inline-block;
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    color: #6b7280;
    font-size: 11px;
    padding: 4px 12px;
    border-radius: 20px;
    margin-right: 6px;
    margin-bottom: 6px;
}

.stat-card {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 14px;
    padding: 1.25rem;
    text-align: center;
    transition: box-shadow 0.2s;
}

.stat-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}

.stat-val {
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
    color: #1a1a1a;
}

.stat-lbl {
    font-size: 10px;
    color: #aaaaaa;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 5px;
}

.movie-card {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s;
}

.movie-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}

.movie-title {
    font-size: 16px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 4px;
    font-family: 'Playfair Display', serif;
}

.movie-meta {
    font-size: 10px;
    color: #aaaaaa;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 12px;
}

.badge-pos {
    display: inline-block;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #16a34a;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}

.badge-neg {
    display: inline-block;
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #dc2626;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}

.badge-mix {
    display: inline-block;
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #d97706;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}

.progress-wrap {
    background: #f3f4f6;
    border-radius: 50px;
    height: 6px;
    overflow: hidden;
    margin: 8px 0;
}

.progress-pos { height:100%; background: #22c55e; border-radius:50px; }
.progress-mix { height:100%; background: #f59e0b; border-radius:50px; }
.progress-neg { height:100%; background: #ef4444; border-radius:50px; }

.result-pos {
    background: #f0fdf4;
    border: 1.5px solid #bbf7d0;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
}

.result-neg {
    background: #fef2f2;
    border: 1.5px solid #fecaca;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
}

.search-card {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 20px;
    padding: 2rem;
    margin-top: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #1a1a1a;
    margin: 1.5rem 0 1rem;
    font-weight: 600;
}

.section-line {
    width: 32px;
    height: 2px;
    background: #6366f1;
    border-radius: 2px;
    margin-bottom: 1rem;
}

.page-header {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    color: #1a1a1a;
    margin: 1.5rem 0 0.3rem;
    font-weight: 700;
}

.page-sub {
    font-size: 13px;
    color: #aaaaaa;
    margin-bottom: 1.5rem;
}

.winner-card {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    text-align: center;
    margin: 1rem 0;
    color: #ffffff;
}

.compare-card {
    background: #ffffff;
    border: 1.5px solid #ebebeb;
    border-radius: 16px;
    padding: 1.5rem;
}

.compare-card-winner {
    background: #ffffff;
    border: 2px solid #6366f1;
    border-radius: 16px;
    padding: 1.5rem;
}

.daily-card {
    background: #ffffff;
    border: 1px solid #ebebeb;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}

.tag-up     { font-size:10px; padding:2px 8px; border-radius:4px; background:#f0fdf4; color:#16a34a; font-weight:600; }
.tag-steady { font-size:10px; padding:2px 8px; border-radius:4px; background:#fffbeb; color:#d97706; font-weight:600; }
.tag-down   { font-size:10px; padding:2px 8px; border-radius:4px; background:#fef2f2; color:#dc2626; font-weight:600; }

.footer {
    text-align: center;
    padding: 2rem;
    border-top: 1px solid #ebebeb;
    color: #cccccc;
    font-size: 11px;
    margin-top: 3rem;
    letter-spacing: 0.05em;
    line-height: 2;
}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────
if "watchlist"   not in st.session_state: st.session_state.watchlist   = []
if "page"        not in st.session_state: st.session_state.page        = "Home"
if "analyzed"    not in st.session_state: st.session_state.analyzed    = []
if "search_data" not in st.session_state: st.session_state.search_data = None
if "history"     not in st.session_state: st.session_state.history     = []

# ── Model ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="Samantha-16/movie-sentiment-distilbert"
    )
classifier = load_model()

# ── API ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_movie(title):
    try:
        url = f"https://www.omdbapi.com/?t={requests.utils.quote(title)}&apikey={OMDB_KEY}"
        r   = requests.get(url, timeout=10)
        d   = r.json()
        if d.get("Response") == "True":
            return d
        url2 = f"https://www.omdbapi.com/?s={requests.utils.quote(title)}&apikey={OMDB_KEY}"
        r2   = requests.get(url2, timeout=10)
        d2   = r2.json()
        if d2.get("Response") == "True":
            fid  = d2["Search"][0]["imdbID"]
            url3 = f"https://www.omdbapi.com/?i={fid}&apikey={OMDB_KEY}"
            return requests.get(url3, timeout=10).json()
    except:
        pass
    return None

def calculate_score(movie_data):
    scores = []
    imdb = movie_data.get("imdbRating", "N/A")
    if imdb != "N/A":
        try: scores.append((float(imdb) / 10) * 100)
        except: pass
    for r in movie_data.get("Ratings", []):
        if r.get("Source") == "Rotten Tomatoes":
            try: scores.append(int(r["Value"].replace("%","")))
            except: pass
        if r.get("Source") == "Metacritic":
            try: scores.append(int(r["Value"].split("/")[0]))
            except: pass
    return round(sum(scores)/len(scores)) if scores else 70

@st.cache_data(ttl=3600)
def get_movie_data(title):
    movie = fetch_movie(title)
    if not movie: return None
    return {
        "title":    movie.get("Title",    title),
        "year":     movie.get("Year",     "—"),
        "genre":    movie.get("Genre",    "—").split(",")[0].strip().upper(),
        "country":  movie.get("Country",  "—").split(",")[0].strip(),
        "director": movie.get("Director", "—"),
        "plot":     movie.get("Plot",     "—"),
        "poster":   movie.get("Poster",   "N/A"),
        "imdb":     movie.get("imdbRating","—"),
        "runtime":  movie.get("Runtime",  "—"),
        "language": movie.get("Language", "—").split(",")[0].strip(),
        "awards":   movie.get("Awards",   "N/A"),
        "actors":   movie.get("Actors",   "—"),
        "score":    calculate_score(movie),
    }

def get_daily_movie():
    picks = [
        "Inception","Parasite","RRR","Spirited Away","3 Idiots",
        "City of God","Amelie","Oldboy","Dangal","Life Is Beautiful",
        "Intouchables","A Separation","Train to Busan","Your Name",
        "Pan's Labyrinth","Jai Bhim","Interstellar","Tumbbad"
    ]
    today = datetime.date.today().strftime("%Y-%m-%d")
    idx   = int(hashlib.md5(today.encode()).hexdigest(), 16) % len(picks)
    return picks[idx]

# ── Helpers ────────────────────────────────────────────────────────────
def badge_html(score):
    if score >= 70: return "badge-pos", "Positive"
    if score >= 50: return "badge-mix", "Mixed"
    return "badge-neg", "Negative"

def bar_cls(score):
    if score >= 70: return "progress-pos"
    if score >= 50: return "progress-mix"
    return "progress-neg"

def score_color(score):
    if score >= 70: return "#16a34a"
    if score >= 50: return "#d97706"
    return "#dc2626"

def show_result(m, key_suffix=""):
    b_cls, b_txt = badge_html(m["score"])
    neg          = 100 - m["score"]
    sc           = score_color(m["score"])

    col_p, col_d = st.columns([1, 2.5])
    with col_p:
        if m["poster"] and m["poster"] != "N/A":
            st.image(m["poster"], width=200)
        else:
            st.markdown("""
            <div style='background:#f3f4f6;border:1px solid #e5e7eb;
                        border-radius:12px;width:200px;height:280px;
                        display:flex;align-items:center;
                        justify-content:center;font-size:48px;'>🎬</div>
            """, unsafe_allow_html=True)

    with col_d:
        st.markdown(f"""
        <div class='search-card'>
            <div style='font-family:"Playfair Display",serif;font-size:1.8rem;
                        color:#1a1a1a;font-weight:700;margin-bottom:4px;'>
                {m['title']}
            </div>
            <div style='font-size:11px;color:#aaaaaa;text-transform:uppercase;
                        letter-spacing:0.1em;margin-bottom:8px;'>
                {m['genre']} · {m['year']} · {m['country']} · {m['language']}
            </div>
            <div style='font-size:13px;color:#888888;margin-bottom:12px;
                        line-height:1.6;font-style:italic;'>
                {m['plot'][:220]}...
            </div>
            <div style='font-size:12px;color:#aaaaaa;margin-bottom:16px;'>
                🎬 {m.get('actors','—')[:80]}
            </div>
            <div style='display:flex;align-items:center;gap:12px;margin-bottom:16px;'>
                <span class='{b_cls}'>{b_txt}</span>
                <span style='font-size:2.2rem;font-weight:700;color:{sc};
                             font-family:"Playfair Display",serif;'>
                    {m['score']}%
                </span>
                <span style='font-size:12px;color:#aaaaaa;'>audience score</span>
            </div>
            <div style='display:flex;justify-content:space-between;
                        font-size:12px;color:#aaaaaa;margin-bottom:4px;'>
                <span>Positive reception</span><span style='color:{sc};font-weight:500;'>{m['score']}%</span>
            </div>
            <div class='progress-wrap'>
                <div class='{bar_cls(m["score"])}' style='width:{m["score"]}%;'></div>
            </div>
            <div style='display:flex;justify-content:space-between;
                        font-size:12px;color:#aaaaaa;margin:6px 0 4px;'>
                <span>Negative reception</span><span style='color:#ef4444;font-weight:500;'>{neg}%</span>
            </div>
            <div class='progress-wrap'>
                <div class='progress-neg' style='width:{neg}%;'></div>
            </div>
            <div style='margin-top:12px;font-size:11px;color:#cccccc;'>
                Dir: {m['director']} · IMDB: {m['imdb']} · {m['runtime']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("+ Add to Watchlist",
                         key=f"w_{key_suffix}",
                         use_container_width=True):
                if m["title"] not in [w["title"] for w in st.session_state.watchlist]:
                    st.session_state.watchlist.append({
                        "title":     m["title"],
                        "status":    "Want to Watch",
                        "sentiment": f"{m['score']}%"
                    })
                    st.success(f"Added '{m['title']}' to watchlist!")
                else:
                    st.info("Already in watchlist!")
        with c2:
            share = f"🎬 {m['title']} scores {m['score']}% on Cinelytix · cinelytix.streamlit.app"
            st.code(share, language=None)

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<span class='nav-logo'>Cinelytix</span>",
                unsafe_allow_html=True)
    st.markdown("<span class='nav-sub'>Cinematic Intelligence</span>",
                unsafe_allow_html=True)

    if st.button("🏠  Home",             use_container_width=True, key="n1"):
        st.session_state.page = "Home";      st.rerun()
    if st.button("🔍  Search Movies",    use_container_width=True, key="n2"):
        st.session_state.page = "Search";    st.rerun()
    if st.button("⚖️  Compare Movies",   use_container_width=True, key="n3"):
        st.session_state.page = "Compare";   st.rerun()
    if st.button("🎬  Analyze a Review", use_container_width=True, key="n4"):
        st.session_state.page = "Sentiment"; st.rerun()
    if st.button("⭐  My Watchlist",     use_container_width=True, key="n5"):
        st.session_state.page = "Watchlist"; st.rerun()

    st.markdown("---")
    st.markdown(f"<span class='nav-stat'>Watchlist: {len(st.session_state.watchlist)} films</span>", unsafe_allow_html=True)
    st.markdown(f"<span class='nav-stat'>Analyzed: {len(st.session_state.analyzed)} reviews</span>", unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("---")
        st.markdown("<span style='font-size:10px;color:#aaaaaa;text-transform:uppercase;letter-spacing:0.15em;'>Recent searches</span>", unsafe_allow_html=True)
        for h in reversed(st.session_state.history[-5:]):
            if st.button(h, key=f"hist_{h}", use_container_width=True):
                with st.spinner(f"Loading {h}..."):
                    r = get_movie_data(h)
                st.session_state.search_data = r
                st.session_state.page = "Home"
                st.rerun()

# ══════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════
if st.session_state.page == "Home":

    st.markdown("""
    <div class='hero-section'>
        <div class='hero-accent'></div>
        <div class='hero-title'>The Pulse of <span>Cinema</span></div>
        <div class='hero-sub'>
            Search any movie from anywhere in the world and get a
            real audience sentiment score powered by AI
        </div>
        <div>
            <span class='hero-badge'>DistilBERT AI</span>
            <span class='hero-badge'>IMDB + Rotten Tomatoes</span>
            <span class='hero-badge'>Any Movie · Any Country</span>
            <span class='hero-badge'>86.4% Accuracy</span>
            <span class='hero-badge'>© Samantha Jessica Monis 2026
