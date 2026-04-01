import streamlit as st
from transformers import pipeline
import requests
import datetime
import hashlib
import csv
import io

# Scroll to result trigger
if "scroll_to_result" not in st.session_state:
    st.session_state.scroll_to_result = False

if st.session_state.scroll_to_result:
    st.markdown(
        """
        <script>
        const el = document.getElementById("result_section");
        if (el) {
            el.scrollIntoView({ behavior: "smooth" });
        }
        </script>
        """,
        unsafe_allow_html=True
    )
    st.session_state.scroll_to_result = False

# Scroll trigger
if "scroll_to_top" not in st.session_state:
    st.session_state.scroll_to_top = False

if st.session_state.scroll_to_top:
    st.markdown(
        """
        <script>
        window.scrollTo({ top: 0, behavior: 'smooth' });
        </script>
        """,
        unsafe_allow_html=True
    )
    st.session_state.scroll_to_top = False
st.set_page_config(
    page_title="Cinelytix",
    page_icon="🎬",
    layout="wide"
)
st.sidebar.title("🎬 Cinelytix")

page = st.sidebar.radio(
    "Navigate",
    ["Home", "Search", "Compare", "Sentiment", "Watchlist"]
)

st.session_state.page = page

OMDB_KEY = "c1c0e742"
TMDB_KEY = "6bbbb1173187da4b61ee07dd092ee315"


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@300;400;500;600&display=swap');

* { font-family: 'Inter', sans-serif; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem; max-width: 1400px; }

.stApp {
    background: linear-gradient(135deg, #e8f4fd 0%, #f0e8fd 50%, #fde8f4 100%);
    min-height: 100vh;
}

section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.7) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.5) !important;
}

.nav-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #6366f1, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 1.5rem 0 0.3rem;
    display: block;
}

.nav-sub {
    font-size: 9px;
    letter-spacing: 0.2em;
    color: #9ca3af !important;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    display: block;
}

.nav-stat {
    font-size: 11px;
    color: #9ca3af !important;
    margin-top: 4px;
    display: block;
}

.stButton button {
    background: rgba(255,255,255,0.8) !important;
    color: #374151 !important;
    font-weight: 500 !important;
    border: 1px solid rgba(255,255,255,0.9) !important;
    border-radius: 12px !important;
    font-size: 13px !important;
    backdrop-filter: blur(10px) !important;
    transition: all 0.2s !important;
}

.stButton button:hover {
    background: rgba(99,102,241,0.1) !important;
    border-color: rgba(99,102,241,0.3) !important;
    color: #6366f1 !important;
    transform: translateY(-1px) !important;
}

.stTextArea textarea {
    background: rgba(255,255,255,0.8) !important;
    border: 1px solid rgba(255,255,255,0.9) !important;
    border-radius: 14px !important;
    color: #1f2937 !important;
    font-size: 14px !important;
    backdrop-filter: blur(10px) !important;
}

.stTextInput input {
    background: rgba(255,255,255,0.8) !important;
    border: 1px solid rgba(255,255,255,0.9) !important;
    border-radius: 10px !important;
    color: #1f2937 !important;
    font-size: 14px !important;
    backdrop-filter: blur(10px) !important;
}

/* Glassmorphism card */
.glass-card {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(99,102,241,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
}

.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.12);
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    border-radius: 24px;
    padding: 3rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    color: white;
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%; right: -20%;
    width: 400px; height: 400px;
    background: rgba(255,255,255,0.1);
    border-radius: 50%;
}

.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40%; left: -10%;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.5rem;
    line-height: 1.2;
    position: relative;
    z-index: 1;
}

.hero-sub {
    font-size: 14px;
    color: rgba(255,255,255,0.8);
    margin-bottom: 1.5rem;
    position: relative;
    z-index: 1;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.3);
    color: white;
    font-size: 11px;
    padding: 4px 14px;
    border-radius: 20px;
    margin-right: 6px;
    margin-bottom: 6px;
    position: relative;
    z-index: 1;
}

/* Stat cards */
.stat-card {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 16px;
    padding: 1.25rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(99,102,241,0.06);
}

.stat-val {
    font-size: 1.8rem;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
    background: linear-gradient(135deg, #6366f1, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stat-lbl {
    font-size: 10px;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 5px;
}

/* Genre pills */
.genre-pill {
    display: inline-block;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.9);
    color: #6b7280;
    font-size: 12px;
    font-weight: 500;
    padding: 6px 16px;
    border-radius: 20px;
    margin-right: 8px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: all 0.2s;
}

.genre-pill-active {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-color: transparent;
}

/* Movie poster card */
.poster-card {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(99,102,241,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
}

.poster-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(99,102,241,0.15);
}

/* Badges */
.badge-pos {
    display: inline-block;
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    color: #065f46;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}

.badge-neg {
    display: inline-block;
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    color: #991b1b;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}

.badge-mix {
    display: inline-block;
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    color: #92400e;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    text-transform: uppercase;
}

/* Progress bars */
.progress-wrap {
    background: rgba(0,0,0,0.06);
    border-radius: 50px;
    height: 8px;
    overflow: hidden;
    margin: 8px 0;
}

.progress-pos { height:100%; background:linear-gradient(90deg,#34d399,#10b981); border-radius:50px; }
.progress-mix { height:100%; background:linear-gradient(90deg,#fbbf24,#f59e0b); border-radius:50px; }
.progress-neg { height:100%; background:linear-gradient(90deg,#f87171,#ef4444); border-radius:50px; }

/* Result cards */
.result-pos {
    background: linear-gradient(135deg, rgba(209,250,229,0.8), rgba(167,243,208,0.8));
    backdrop-filter: blur(20px);
    border: 1.5px solid rgba(167,243,208,0.9);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
}

.result-neg {
    background: linear-gradient(135deg, rgba(254,226,226,0.8), rgba(254,202,202,0.8));
    backdrop-filter: blur(20px);
    border: 1.5px solid rgba(254,202,202,0.9);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
}

.search-result-card {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 1rem;
    box-shadow: 0 8px 32px rgba(99,102,241,0.1);
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #1f2937;
    margin: 1.5rem 0 0.3rem;
    font-weight: 600;
}

.section-sub {
    font-size: 12px;
    color: #9ca3af;
    margin-bottom: 1rem;
}

.page-header {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    background: linear-gradient(135deg, #6366f1, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 1.5rem 0 0.3rem;
    font-weight: 700;
}

.page-sub {
    font-size: 13px;
    color: #9ca3af;
    margin-bottom: 1.5rem;
}

.daily-card {
    background: linear-gradient(135deg,
        rgba(99,102,241,0.12), rgba(236,72,153,0.08));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
}

.winner-banner {
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    text-align: center;
    color: white;
    margin: 1rem 0;
}

.compare-card {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 16px;
    padding: 1.5rem;
}

.compare-card-winner {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(20px);
    border: 2px solid rgba(99,102,241,0.5);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px rgba(99,102,241,0.15);
}

.footer {
    text-align: center;
    padding: 2rem;
    border-top: 1px solid rgba(255,255,255,0.5);
    color: #d1d5db;
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
        url = f"https://www.omdbapi.com/?t={title}&apikey={OMDB_KEY}"
        res = requests.get(url, timeout=5).json()

        if res.get("Response") == "True":
            return res
        else:
            return None

    except Exception as e:
        return None
    
@st.cache_data(ttl=3600)
def get_trending_movies():
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={TMDB_KEY}"
    data = requests.get(url).json()
    return data.get("results", [])

@st.cache_data(ttl=3600)
def get_movies_by_genre(genre_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&query={genre_name}"
    data = requests.get(url).json()
    return data.get("results", [])


def calculate_score(movie_data):
    scores = []
    imdb = movie_data.get("imdbRating","N/A")
    if imdb != "N/A":
        try: scores.append((float(imdb)/10)*100)
        except: pass
    for r in movie_data.get("Ratings",[]):
        if r.get("Source") == "Rotten Tomatoes":
            try: scores.append(int(r["Value"].replace("%","")))
            except: pass
        if r.get("Source") == "Metacritic":
            try: scores.append(int(r["Value"].split("/")[0]))
            except: pass
    return round(sum(scores)/len(scores)) if scores else 70

def smart_search(query):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&query={query}"
    data = requests.get(url).json()

    if data.get("results"):
        return data["results"][0]["title"]  # best match
    
    return query

@st.cache_data(ttl=3600)
def get_movie_data(title):
    movie = fetch_movie(title)
    if not movie: return None
    return {
        "title":    movie.get("Title",    title),
        "year":     movie.get("Year",     "—"),
        "genre":    movie.get("Genre",    "—").split(",")[0].strip(),
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
    idx   = int(hashlib.md5(today.encode()).hexdigest(),16) % len(picks)
    return picks[idx]

# ── Helpers ────────────────────────────────────────────────────────────
def badge_html(score):
    if score >= 70: return "badge-pos","Positive"
    if score >= 50: return "badge-mix","Mixed"
    return "badge-neg","Negative"

def bar_cls(score):
    if score >= 70: return "progress-pos"
    if score >= 50: return "progress-mix"
    return "progress-neg"

def score_color(score):
    if score >= 70: return "#10b981"
    if score >= 50: return "#f59e0b"
    return "#ef4444"

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
            <div style='background:rgba(255,255,255,0.6);
                        backdrop-filter:blur(10px);
                        border:1px solid rgba(255,255,255,0.8);
                        border-radius:16px;width:200px;height:280px;
                        display:flex;align-items:center;
                        justify-content:center;font-size:48px;'>🎬</div>
            """, unsafe_allow_html=True)

    with col_d:
        st.markdown(f"""
        <div class='search-result-card'>
            <div style='font-family:"Playfair Display",serif;
                        font-size:1.8rem;color:#1f2937;
                        font-weight:700;margin-bottom:4px;'>
                {m['title']}
            </div>
            <div style='font-size:11px;color:#9ca3af;
                        text-transform:uppercase;letter-spacing:0.1em;
                        margin-bottom:8px;'>
                {m['genre']} · {m['year']} · {m['country']} · {m['language']}
            </div>
            <div style='font-size:13px;color:#6b7280;margin-bottom:12px;
                        line-height:1.6;'>
                {m['plot'][:220]}...
            </div>
            <div style='font-size:12px;color:#9ca3af;margin-bottom:16px;'>
                🎬 {m.get("actors","—")[:80]}
            </div>
            <div style='display:flex;align-items:center;
                        gap:12px;margin-bottom:16px;'>
                <span class='{b_cls}'>{b_txt}</span>
                <span style='font-size:2.2rem;font-weight:700;
                             color:{sc};font-family:"Playfair Display",serif;'>
                    {m['score']}%
                </span>
                <span style='font-size:12px;color:#9ca3af;'>
                    audience score
                </span>
            </div>
            <div style='display:flex;justify-content:space-between;
                        font-size:12px;color:#9ca3af;margin-bottom:4px;'>
                <span>Positive</span>
                <span style='color:{sc};font-weight:500;'>{m['score']}%</span>
            </div>
            <div class='progress-wrap'>
                <div class='{bar_cls(m["score"])}' style='width:{m["score"]}%;'>
                </div>
            </div>
            <div style='display:flex;justify-content:space-between;
                        font-size:12px;color:#9ca3af;margin:6px 0 4px;'>
                <span>Negative</span>
                <span style='color:#ef4444;font-weight:500;'>{neg}%</span>
            </div>
            <div class='progress-wrap'>
                <div class='progress-neg' style='width:{neg}%;'></div>
            </div>
            <div style='margin-top:12px;font-size:11px;color:#d1d5db;'>
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
            share = (f"🎬 {m['title']} scores {m['score']}% "
                     f"on Cinelytix · cinelytix.streamlit.app")
            st.code(share, language=None)

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<span class='nav-logo'>Cinelytix</span>",
                unsafe_allow_html=True)
    st.markdown("<span class='nav-sub'>Cinematic Intelligence</span>",
                unsafe_allow_html=True)

    for key, label in {
        "Home":      "🏠  Home",
        "Search":    "🔍  Search Movies",
        "Compare":   "⚖️  Compare Movies",
        "Sentiment": "🎬  Analyze a Review",
        "Watchlist": "⭐  My Watchlist",
    }.items():
        if st.button(label, use_container_width=True, key=f"nav_{key}"):
            st.session_state.page = key
            st.rerun()

    st.markdown("---")
    st.markdown(f"<span class='nav-stat'>Watchlist: {len(st.session_state.watchlist)} films</span>", unsafe_allow_html=True)
    st.markdown(f"<span class='nav-stat'>Analyzed: {len(st.session_state.analyzed)} reviews</span>", unsafe_allow_html=True)

    if st.session_state.history:
        st.markdown("---")
        st.markdown("<span style='font-size:10px;color:#9ca3af;text-transform:uppercase;letter-spacing:0.15em;'>Recent</span>", unsafe_allow_html=True)
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

    # Hero banner
    st.markdown("""
    <div class='hero-banner'>
        <div class='hero-title'>The Pulse of Cinema</div>
        <div class='hero-sub'>
            Search any movie from anywhere in the world and get a
            real AI-powered sentiment score
        </div>
        <div>
            <span class='hero-badge'>🤖 DistilBERT AI</span>
            <span class='hero-badge'>⭐ IMDB + Rotten Tomatoes</span>
            <span class='hero-badge'>🌍 Any Movie · Any Country</span>
            <span class='hero-badge'>✨ 86.4% Accuracy</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-card'><div class='stat-val'>86.4%</div><div class='stat-lbl'>Model Accuracy</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-card'><div class='stat-val'>66M</div><div class='stat-lbl'>Parameters</div></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-card'><div class='stat-val'>∞</div><div class='stat-lbl'>Movies Supported</div></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='stat-card'><div class='stat-val'>{len(st.session_state.watchlist)}</div><div class='stat-lbl'>Watchlist Films</div></div>", unsafe_allow_html=True)

    # Movie of the day
    daily_title = get_daily_movie()
    st.markdown("<div class='section-title'>🎬 Movie of the Day</div>", unsafe_allow_html=True)
    col_d1, col_d2 = st.columns([3, 1])
    with col_d1:
        st.markdown(f"""
        <div class='daily-card'>
            <div style='font-size:10px;color:#9ca3af;text-transform:uppercase;
                        letter-spacing:0.15em;margin-bottom:6px;'>
                Today · {datetime.date.today().strftime("%B %d, %Y")}
            </div>
            <div style='font-family:"Playfair Display",serif;font-size:1.4rem;
                        background:linear-gradient(135deg,#6366f1,#ec4899);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        font-weight:700;margin-bottom:4px;'>
                {daily_title}
            </div>
            <div style='font-size:12px;color:#9ca3af;'>
                Click to get the AI sentiment score for today's featured film
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_d2:
        if st.button("Analyze Today's Film", use_container_width=True, key="daily"):
            with st.spinner(f"Loading {daily_title}..."):
                corrected = smart_search(daily_title)
                r = get_movie_data(corrected)
                
            st.session_state.search_data = r
            if daily_title not in st.session_state.history:
                st.session_state.history.append(daily_title)
            st.rerun()

    # Search bar
    st.markdown("<div class='section-title'>Search Any Movie</div>", unsafe_allow_html=True)
    col_s, col_b = st.columns([4, 1])
    with col_s:
        home_q = st.text_input(
            "", placeholder="RRR, Parasite, Amelie, 3 Idiots, Spirited Away...",
            label_visibility="collapsed", key="home_q"
        )
    with col_b:
        if st.button("Search", use_container_width=True, key="home_btn"):
            if home_q.strip():
                with st.spinner(f"Finding '{home_q}'..."):
                    corrected = smart_search(home_q)
                    r = get_movie_data(corrected)
                st.session_state.search_data = r
                st.session_state.scroll_to_result = True   # ✅ ADD THIS
                st.rerun()
                if home_q not in st.session_state.history:
                    st.session_state.history.append(home_q)
                if not r:
                    st.error(f"Could not find '{home_q}'.")
                    
# Anchor (place BEFORE results)
st.markdown('<div id="result_section"></div>', unsafe_allow_html=True)

# Show result ONLY ONCE
if st.session_state.search_data:
    show_result(st.session_state.search_data, "home")

# Scroll trigger (separate block)
if st.session_state.get("scroll_to_result"):
    st.markdown("""
        <script>
        const el = document.getElementById("result_section");
        if (el) {
            el.scrollIntoView({ behavior: "smooth" });
        }
        </script>
    """, unsafe_allow_html=True)

    st.session_state.scroll_to_result = False

    
# Popular around the world
if st.session_state.page == "Home":
  st.markdown("<div class='section-title' style='margin-top:1.5rem;'>Popular Around the World</div>", unsafe_allow_html=True)
  st.markdown("<div class='section-sub'>Click any film to get its sentiment score instantly</div>", unsafe_allow_html=True)
  movies = get_trending_movies()

  cols = st.columns(4)

  for i, movie in enumerate(movies[:12]):
    with cols[i % 4]:
        poster = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None
        
        if poster:
            st.image(poster, use_container_width=True)

        if st.button(movie["title"], key=f"genre_{i}", use_container_width=True):
          r = get_movie_data(movie["title"])
          st.session_state.search_data = r
          st.session_state.scroll_to_top = True
          st.rerun()

GENRE_MAP = {
    "Action": 28,
    "Comedy": 35,
    "Drama": 18,
    "Romance": 10749,
    "Thriller": 53
}
def get_movies_by_genre(genre):
    genre_id = GENRE_MAP.get(genre)
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_KEY}&with_genres={genre_id}&sort_by=popularity.desc"
    return requests.get(url).json().get("results", [])
GENRES = ["Action", "Comedy", "Drama", "Romance", "Thriller"]

st.markdown("<div class='section-title'>Browse by Genre</div>", unsafe_allow_html=True)

gcols = st.columns(len(GENRES))

for i, g in enumerate(GENRES):
    if gcols[i].button(g, key=f"g_{g}", use_container_width=True):
        st.session_state.selected_genre = g
        st.rerun()

BOLLYWOOD_MOVIES = {
    "Action": [
        "Pathaan", "War", "KGF Chapter 2", "Jawan", "RRR"
    ],
    "Comedy": [
        "3 Idiots", "Hera Pheri", "Bhool Bhulaiyaa", "Chup Chup Ke", "Welcome"
    ],
    "Drama": [
        "Dangal", "Taare Zameen Par", "Jai Bhim", "Swades", "Article 15"
    ],
    "Romance": [
        "Dilwale Dulhania Le Jayenge", "Kabir Singh", "Ae Dil Hai Mushkil", "Veer-Zaara"
    ],
    "Thriller": [
        "Andhadhun", "Drishyam", "Kahaani", "Talaash", "Badla"
    ]
}

selected_genre = st.session_state.get("selected_genre")

if selected_genre:
    st.markdown(f"### 🎬 {selected_genre} Movies")

    # ✅ Get LIVE movies from TMDb
    tmdb_movies = get_movies_by_genre(selected_genre)

    # ✅ Add Bollywood manually
    bollywood = BOLLYWOOD_MOVIES.get(selected_genre, [])

    # Combine
    all_movies = tmdb_movies[:10]

    # Add Bollywood as fake TMDb-style dict
    for b in bollywood:
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&query={b}"
        res = requests.get(search_url).json().get("results")

        if res:
          all_movies.append(res[0])

    # ✅ Horizontal layout
    cols = st.columns(5)

    for i, movie in enumerate(all_movies[:10]):
        with cols[i % 5]:
            poster = (
                f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                if movie.get("poster_path")
                else None
            )

            if poster:
                st.image(poster, use_container_width=True)

            if st.button(movie["title"], key=f"genre_{i}_{movie['title']}", use_container_width=True):

               with st.spinner(f"Loading {movie['title']}..."):
                movie_data = get_movie_data(movie["title"])

               if movie_data:
                st.session_state.search_data = movie_data
                if movie["title"] not in st.session_state.history:
                  st.session_state.history.append(movie["title"])
                  st.rerun()
               else:
                  st.error("Movie data not found")    

elif st.session_state.page == "Search":           
# ══════════════════════════════════════════════════════════════════════
# SEARCH
# ══════════════════════════════════════════════════════════════════════


    st.markdown("<div class='page-header'>Search Any Movie</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Find any film from any country — scores from IMDB, Rotten Tomatoes and Metacritic</div>", unsafe_allow_html=True)

   # 🔍 Smart search function (ADD THIS ABOVE SEARCH SECTION if not added)







    st.markdown("<div class='section-title'>Try These Films</div>",
                unsafe_allow_html=True)
    suggestions = [
        "RRR",        "Parasite",    "Spirited Away",  "Amelie",
        "3 Idiots",   "City of God", "Inception",      "Dangal",
        "Tumbbad",    "Jai Bhim",    "Train to Busan", "Your Name",
        "Kantara",    "Oldboy",      "Intouchables",   "Interstellar",
        "Capernaum",  "A Separation","Life Is Beautiful","Pan's Labyrinth",
    ]
    cols = st.columns(5)
    for i, s in enumerate(suggestions):
        if cols[i % 5].button(s, key=f"sg{i}", use_container_width=True):
            with st.spinner(f"Loading {s}..."):
                r = get_movie_data(s)
            if r:
                if s not in st.session_state.history:
                    st.session_state.history.append(s)
                show_result(r, f"sg_{i}")

# ══════════════════════════════════════════════════════════════════════
# COMPARE
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Compare":

    st.markdown("<div class='page-header'>Compare Movies</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Search two movies and compare their sentiment scores side by side</div>", unsafe_allow_html=True)

    col_a, col_vs, col_b = st.columns([2, 0.3, 2])
    with col_a:
        m1q = st.text_input("", placeholder="First movie...",
                            label_visibility="collapsed", key="m1q")
    with col_vs:
        st.markdown("<div style='text-align:center;padding-top:8px;font-size:18px;color:#9ca3af;font-weight:700;'>VS</div>", unsafe_allow_html=True)
    with col_b:
        m2q = st.text_input("", placeholder="Second movie...",
                            label_visibility="collapsed", key="m2q")

    if st.button("Compare Now", use_container_width=True, key="cmp"):
        if m1q and m2q:
            with st.spinner("Fetching both movies..."):
                m1 = get_movie_data(m1q)
                m2 = get_movie_data(m2q)

            if m1 and m2:
                winner = m1 if m1["score"] >= m2["score"] else m2
                st.markdown(f"""
                <div class='winner-banner'>
                    <div style='font-size:11px;color:rgba(255,255,255,0.7);
                                text-transform:uppercase;letter-spacing:0.15em;
                                margin-bottom:4px;'>Winner</div>
                    <div style='font-family:"Playfair Display",serif;
                                font-size:1.5rem;font-weight:700;'>
                        🏆 {winner['title']} — {winner['score']}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

                c1, c2 = st.columns(2)
                for col, m in [(c1, m1), (c2, m2)]:
                    b_cls, b_txt = badge_html(m["score"])
                    neg          = 100 - m["score"]
                    sc           = score_color(m["score"])
                    is_win       = m["title"] == winner["title"]
                    card_cls     = "compare-card-winner" if is_win else "compare-card"

                    with col:
                        if m["poster"] and m["poster"] != "N/A":
                            st.image(m["poster"], width=180)
                        st.markdown(f"""
                        <div class='{card_cls}' style='margin-top:8px;'>
                            {"<div style='font-size:10px;background:linear-gradient(135deg,#6366f1,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:600;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:6px;'>✓ Higher Score</div>" if is_win else ""}
                            <div style='font-family:"Playfair Display",serif;
                                        font-size:1.2rem;color:#1f2937;
                                        font-weight:700;margin-bottom:4px;'>
                                {m['title']}
                            </div>
                            <div style='font-size:10px;color:#9ca3af;
                                        text-transform:uppercase;margin-bottom:12px;'>
                                {m['genre']} · {m['year']} · {m['country']}
                            </div>
                            <div style='font-size:2.5rem;font-weight:700;
                                        color:{sc};font-family:"Playfair Display",serif;
                                        margin-bottom:4px;'>
                                {m['score']}%
                            </div>
                            <span class='{b_cls}'>{b_txt}</span>
                            <div class='progress-wrap' style='margin-top:12px;'>
                                <div class='{bar_cls(m["score"])}'
                                     style='width:{m["score"]}%;'></div>
                            </div>
                            <div style='margin-top:12px;font-size:11px;color:#9ca3af;'>
                                IMDB: {m['imdb']} · {m['runtime']}<br>
                                Dir: {m['director']}
                            </div>
                            <div style='margin-top:10px;font-size:12px;
                                        color:#6b7280;line-height:1.5;'>
                                {m['plot'][:150]}...
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button(f"+ Watchlist",
                                     key=f"cw_{m['title']}_{m['year']}",
                                     use_container_width=True):
                            if m["title"] not in [w["title"] for w in st.session_state.watchlist]:
                                st.session_state.watchlist.append({
                                    "title":     m["title"],
                                    "status":    "Want to Watch",
                                    "sentiment": f"{m['score']}%"
                                })
                                st.success(f"Added '{m['title']}'!")
            else:
                st.error("Could not find one or both movies.")

    st.markdown("<div class='section-title'>Popular Comparisons</div>",
                unsafe_allow_html=True)
    comparisons = [
        ("Inception",    "Interstellar"),
        ("Parasite",     "Oldboy"),
        ("RRR",          "Baahubali 2"),
        ("3 Idiots",     "Dangal"),
        ("Spirited Away","Your Name"),
        ("Amelie",       "Intouchables"),
    ]
    cols = st.columns(3)
    for i, (a, b) in enumerate(comparisons):
        if cols[i % 3].button(f"{a} vs {b}", key=f"qc{i}",
                              use_container_width=True):
            with st.spinner("Comparing..."):
                m1 = get_movie_data(a)
                m2 = get_movie_data(b)
            if m1 and m2:
                winner = m1 if m1["score"] >= m2["score"] else m2
                st.markdown(f"""
                <div class='winner-banner'>
                    <div style='font-size:11px;color:rgba(255,255,255,0.7);
                                text-transform:uppercase;margin-bottom:4px;'>
                        Winner
                    </div>
                    <div style='font-family:"Playfair Display",serif;
                                font-size:1.4rem;font-weight:700;'>
                        🏆 {winner['title']} — {winner['score']}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                for col, m in [(c1, m1), (c2, m2)]:
                    sc = score_color(m["score"])
                    b_cls, b_txt = badge_html(m["score"])
                    with col:
                        st.markdown(f"""
                        <div class='glass-card'>
                            <div style='font-family:"Playfair Display",serif;
                                        font-size:1.1rem;color:#1f2937;
                                        font-weight:700;margin-bottom:4px;'>
                                {m['title']}
                            </div>
                            <div style='font-size:1.8rem;font-weight:700;color:{sc};
                                        font-family:"Playfair Display",serif;'>
                                {m['score']}%
                            </div>
                            <span class='{b_cls}'>{b_txt}</span>
                            <div class='progress-wrap' style='margin-top:8px;'>
                                <div class='{bar_cls(m["score"])}'
                                     style='width:{m["score"]}%;'></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# SENTIMENT
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Sentiment":

    st.markdown("<div class='page-header'>Analyze a Review</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Paste any movie review — DistilBERT classifies it as positive or negative</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-card'><div class='stat-val'>86.4%</div><div class='stat-lbl'>Accuracy</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-card'><div class='stat-val'>0.86</div><div class='stat-lbl'>F1 Score</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-card'><div class='stat-val'>{len(st.session_state.analyzed)}</div><div class='stat-lbl'>Reviews Done</div></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-card'><div class='stat-val'>66M</div><div class='stat-lbl'>Parameters</div></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.3, 1])
    with col_l:
        mname  = st.text_input("", placeholder="Movie title (optional)...",
                               label_visibility="collapsed", key="mn")
        review = st.text_area("", placeholder="Paste any movie review here...",
                              height=160, label_visibility="collapsed", key="rv")
        ca, cw = st.columns(2)
        with ca:
            go = st.button("Analyze", use_container_width=True)
        with cw:
            if st.button("+ Watchlist", use_container_width=True) and mname:
                if mname not in [w["title"] for w in st.session_state.watchlist]:
                    st.session_state.watchlist.append({
                        "title": mname,"status":"Want to Watch","sentiment":"—"
                    })
                    st.success(f"Added '{mname}'!")

        st.markdown("<div style='margin-top:1rem;font-size:10px;color:#9ca3af;text-transform:uppercase;letter-spacing:0.15em;'>Samples</div>", unsafe_allow_html=True)
        samples = [
            "This movie was absolutely brilliant!",
            "Terrible film. Complete waste of time.",
            "A masterpiece of modern cinema.",
            "The plot made no sense whatsoever.",
            "Stunning visuals but weak story.",
            "One of the best I have ever seen!",
        ]
        r1 = st.columns(3)
        for i, s in enumerate(samples[:3]):
            if r1[i].button(s[:18]+"...", key=f"sa{i}"):
                st.session_state["picked"] = s
        r2 = st.columns(3)
        for i, s in enumerate(samples[3:]):
            if r2[i].button(s[:18]+"...", key=f"sb{i}"):
                st.session_state["picked"] = s
        if "picked" in st.session_state:
            review = st.session_state["picked"]

    with col_r:
        if go and review.strip():
            with st.spinner("Analyzing..."):
                res   = classifier(review[:512])[0]
                label = "POSITIVE" if res["label"] == "LABEL_1" else "NEGATIVE"
                conf  = round(res["score"] * 100, 2)
            st.session_state.analyzed.append({
                "review": review[:60],"label": label,
                "confidence": conf,"movie": mname or "Unknown"
            })
            if label == "POSITIVE":
                st.markdown(f"""
                <div class='result-pos'>
                    <div style='font-size:44px;margin-bottom:8px;'>🎬</div>
                    <div style='font-size:28px;font-weight:700;color:#065f46;
                                letter-spacing:3px;margin-bottom:6px;'>POSITIVE</div>
                    <div style='color:#6ee7b7;font-size:12px;margin-bottom:20px;'>
                        Positive sentiment detected
                    </div>
                    <div style='background:rgba(0,0,0,0.06);border-radius:50px;
                                height:8px;overflow:hidden;margin:0 auto 12px;
                                max-width:300px;'>
                        <div style='width:{conf}%;height:100%;
                                    background:linear-gradient(90deg,#34d399,#10b981);
                                    border-radius:50px;'></div>
                    </div>
                    <div style='font-size:2.5rem;font-weight:700;color:#065f46;
                                font-family:"Playfair Display",serif;'>{conf}%</div>
                    <div style='font-size:11px;color:#6ee7b7;margin-top:4px;'>
                        confidence
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-neg'>
                    <div style='font-size:44px;margin-bottom:8px;'>🎭</div>
                    <div style='font-size:28px;font-weight:700;color:#991b1b;
                                letter-spacing:3px;margin-bottom:6px;'>NEGATIVE</div>
                    <div style='color:#fca5a5;font-size:12px;margin-bottom:20px;'>
                        Negative sentiment detected
                    </div>
                    <div style='background:rgba(0,0,0,0.06);border-radius:50px;
                                height:8px;overflow:hidden;margin:0 auto 12px;
                                max-width:300px;'>
                        <div style='width:{conf}%;height:100%;
                                    background:linear-gradient(90deg,#f87171,#ef4444);
                                    border-radius:50px;'></div>
                    </div>
                    <div style='font-size:2.5rem;font-weight:700;color:#991b1b;
                                font-family:"Playfair Display",serif;'>{conf}%</div>
                    <div style='font-size:11px;color:#fca5a5;margin-top:4px;'>
                        confidence
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:rgba(255,255,255,0.6);
                        backdrop-filter:blur(20px);
                        border:1px dashed rgba(99,102,241,0.2);
                        border-radius:20px;padding:3rem;text-align:center;'>
                <div style='font-size:44px;margin-bottom:12px;'>🎬</div>
                <div style='color:#9ca3af;font-size:13px;'>
                    Enter a review and click Analyze
                </div>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.analyzed:
        st.markdown("<div class='section-title'>Recent Analysis</div>",
                    unsafe_allow_html=True)
        for item in reversed(st.session_state.analyzed[-3:]):
            lc   = "#10b981" if item["label"] == "POSITIVE" else "#ef4444"
            bcls = "badge-pos" if item["label"] == "POSITIVE" else "badge-neg"
            st.markdown(f"""
            <div class='glass-card'>
                <div style='display:flex;justify-content:space-between;
                            align-items:center;'>
                    <div>
                        <div style='font-size:12px;color:#9ca3af;
                                    margin-bottom:3px;'>{item['movie']}</div>
                        <div style='font-size:13px;color:#374151;'>
                            "{item['review']}..."
                        </div>
                    </div>
                    <div style='text-align:right;margin-left:1rem;flex-shrink:0;'>
                        <span class='{bcls}'>{item['label']}</span>
                        <div style='font-size:1.3rem;font-weight:700;
                                    color:{lc};margin-top:4px;'>
                            {item['confidence']}%
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# WATCHLIST
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Watchlist":

    st.markdown("<div class='page-header'>My Watchlist</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Track and manage your personal film collection</div>", unsafe_allow_html=True)

    ca, cb, cc = st.columns([2.5, 1.5, 1])
    with ca:
        nf = st.text_input("", placeholder="Add any movie...",
                           label_visibility="collapsed", key="nf")
    with cb:
        ns = st.selectbox("",["Want to Watch","Watching","Watched"],
                          label_visibility="collapsed", key="ns")
    with cc:
        if st.button("Add Film", use_container_width=True):
            if nf:
                if nf not in [w["title"] for w in st.session_state.watchlist]:
                    st.session_state.watchlist.append({
                        "title": nf,"status": ns,"sentiment": "—"
                    })
                    st.success(f"Added '{nf}'!")
                else:
                    st.warning("Already in watchlist!")

    if st.session_state.watchlist:
        want  = sum(1 for w in st.session_state.watchlist if w["status"]=="Want to Watch")
        watch = sum(1 for w in st.session_state.watchlist if w["status"]=="Watching")
        done  = sum(1 for w in st.session_state.watchlist if w["status"]=="Watched")

        c1, c2, c3 = st.columns(3)
        with c1: st.markdown(f"<div class='stat-card'><div class='stat-val'>{want}</div><div class='stat-lbl'>Want to Watch</div></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='stat-card'><div class='stat-val'>{watch}</div><div class='stat-lbl'>Watching</div></div>", unsafe_allow_html=True)
        with c3: st.markdown(f"<div class='stat-card'><div class='stat-val'>{done}</div><div class='stat-lbl'>Watched</div></div>", unsafe_allow_html=True)

        # Export CSV
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["title","status","sentiment"])
        writer.writeheader()
        writer.writerows(st.session_state.watchlist)
        st.download_button(
            "📥 Export Watchlist as CSV",
            data=output.getvalue(),
            file_name="cinelytix_watchlist.csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown("<div class='section-title'>My Films</div>",
                    unsafe_allow_html=True)
        for i, film in enumerate(st.session_state.watchlist):
            sc = {"Watched":"#10b981","Watching":"#f59e0b",
                  "Want to Watch":"#6366f1"}.get(film["status"],"#9ca3af")
            c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 0.5])
            with c1:
                st.markdown(f"""
                <div style='padding:10px 0;'>
                    <div style='font-size:14px;font-weight:600;color:#1f2937;
                                font-family:"Playfair Display",serif;'>
                        {film['title']}
                    </div>
                    <div style='font-size:11px;color:#9ca3af;margin-top:2px;'>
                        Score: {film['sentiment']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style='padding:10px 0;'>
                    <span style='background:rgba(99,102,241,0.08);
                                 border:1px solid {sc}44;color:{sc};
                                 font-size:11px;padding:4px 10px;
                                 border-radius:20px;'>
                        {film['status']}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                upd = st.selectbox(
                    "",["Want to Watch","Watching","Watched"],
                    index=["Want to Watch","Watching","Watched"].index(film["status"]),
                    key=f"upd{i}", label_visibility="collapsed"
                )
                if upd != film["status"]:
                    st.session_state.watchlist[i]["status"] = upd
                    st.rerun()
            with c4:
                if st.button("✕", key=f"del{i}"):
                    st.session_state.watchlist.pop(i)
                    st.rerun()
            st.markdown("<hr style='border-color:rgba(0,0,0,0.06);margin:2px 0;'>",
                        unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:rgba(255,255,255,0.6);
                    backdrop-filter:blur(20px);
                    border:1px dashed rgba(99,102,241,0.2);
                    border-radius:16px;padding:3rem;text-align:center;'>
            <div style='font-size:40px;margin-bottom:12px;'>⭐</div>
            <div style='color:#9ca3af;font-size:13px;'>
                Your watchlist is empty.<br>
                Search any movie and add it here.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    © 2026 Samantha Jessica Monis · All rights reserved<br>
    Cinelytix · AI Movie Sentiment Intelligence ·
    Built with DistilBERT · Fine-tuned on IMDB · 86.4% Accuracy<br>
    <a href='https://huggingface.co/Samantha-16/movie-sentiment-distilbert'
       style='color:#d1d5db;text-decoration:none;'>
        Model: Samantha-16/movie-sentiment-distilbert
    </a>
</div>
""", unsafe_allow_html=True)
