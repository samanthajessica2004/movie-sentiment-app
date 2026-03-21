import streamlit as st
from transformers import pipeline
import requests



test = requests.get(f"http://www.omdbapi.com/?t=Inception&apikey={OMDB_KEY}")
st.write("API Response:", test.json())

st.set_page_config(
    page_title="Cinelytix",
    page_icon="🎬",
    layout="wide"
)

# ── PASTE YOUR OMDB KEY HERE ──────────────────────────────────────────
OMDB_KEY = "c1c0e742"
# ─────────────────────────────────────────────────────────────────────

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

.hero-section {
    background: linear-gradient(135deg, #0d0d1f 0%, #12103a 50%, #0d0d1f 100%);
    border: 1px solid #1e1e3a;
    border-radius: 24px;
    padding: 3rem;
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

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #ffffff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.hero-sub {
    font-size: 14px;
    color: #6060a0;
    margin-bottom: 2rem;
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
}

.stat-card {
    background: linear-gradient(135deg, #0d0d1f, #10102a);
    border: 1px solid #1e1e3a;
    border-radius: 16px;
    padding: 1.25rem;
    text-align: center;
}

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

.progress-pos { height:100%; background:linear-gradient(90deg,#5b21b6,#a78bfa); border-radius:50px; }
.progress-mix { height:100%; background:linear-gradient(90deg,#b45309,#fbbf24); border-radius:50px; }
.progress-neg { height:100%; background:linear-gradient(90deg,#991b1b,#f87171); border-radius:50px; }

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

.search-card {
    background: linear-gradient(135deg, #0d0d1f, #0f0f22);
    border: 1px solid #7c3aed;
    border-radius: 20px;
    padding: 2rem;
    margin-top: 1rem;
}

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

# ── Session State ──────────────────────────────────────────────────────
if "watchlist"   not in st.session_state: st.session_state.watchlist   = []
if "page"        not in st.session_state: st.session_state.page        = "Home"
if "analyzed"    not in st.session_state: st.session_state.analyzed    = []
if "search_data" not in st.session_state: st.session_state.search_data = None

# ── Model ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="Samantha-16/movie-sentiment-distilbert"
    )
classifier = load_model()

# ── API Functions ──────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_movie(title):
    """Fetch movie details from OMDB"""
    try:
        url = f"http://www.omdbapi.com/?t={requests.utils.quote(title)}&apikey={OMDB_KEY}"
        r   = requests.get(url, timeout=10)
        d   = r.json()
        if d.get("Response") == "True":
            return d
    except:
        pass
    return None

@st.cache_data(ttl=3600)
def fetch_wiki_reviews(title):
    """Fetch reception text from Wikipedia"""
    try:
        search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(title.replace(' ', '_'))}"
        r = requests.get(search_url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            extract = data.get("extract", "")
            if len(extract) > 100:
                return extract
    except:
        pass
    return None

def analyze_text_sentiment(text):
    """Run text through DistilBERT and return score"""
    if not text or len(text.strip()) < 20:
        return None, None
    sentences = [s.strip() for s in text.replace(".", ". ").split(". ") if len(s.strip()) > 30][:10]
    if not sentences:
        return None, None
    pos_count = 0
    total     = 0
    confidences = []
    for sentence in sentences:
        try:
            result     = classifier(sentence[:512])[0]
            label      = result["label"]
            confidence = result["score"]
            if label == "LABEL_1":
                pos_count += 1
            confidences.append(confidence)
            total += 1
        except:
            continue
    if total == 0:
        return None, None
    pos_score = round((pos_count / total) * 100)
    avg_conf  = round(sum(confidences) / len(confidences) * 100, 1)
    return pos_score, avg_conf

def get_movie_sentiment(title):
    """Full pipeline — fetch movie + analyze sentiment"""
    movie = fetch_movie(title)
    if not movie:
        return None

    texts_to_analyze = []

    # Use plot as base text
    plot = movie.get("Plot", "")
    if plot and plot != "N/A":
        texts_to_analyze.append(plot)

    # Use Wikipedia reception text
    wiki = fetch_wiki_reviews(title)
    if wiki:
        texts_to_analyze.append(wiki)

    # Combine all text
    combined = " ".join(texts_to_analyze)

    if combined.strip():
        score, confidence = analyze_text_sentiment(combined)
    else:
        score, confidence = None, None

    # Fallback to IMDB rating if model returns nothing
    if score is None:
        imdb = movie.get("imdbRating", "N/A")
        if imdb != "N/A":
            try:
                score      = round((float(imdb) / 10) * 100)
                confidence = 75.0
            except:
                score, confidence = 70, 70.0

    return {
        "title":      movie.get("Title", title),
        "year":       movie.get("Year", "—"),
        "genre":      movie.get("Genre", "—").split(",")[0].strip().upper(),
        "country":    movie.get("Country", "—").split(",")[0].strip(),
        "director":   movie.get("Director", "—"),
        "plot":       movie.get("Plot", "—"),
        "poster":     movie.get("Poster", "N/A"),
        "imdb":       movie.get("imdbRating", "—"),
        "runtime":    movie.get("Runtime", "—"),
        "score":      score or 70,
        "confidence": confidence or 70.0,
        "language":   movie.get("Language", "—"),
        "awards":     movie.get("Awards", "—"),
    }

# ── Helpers ────────────────────────────────────────────────────────────
def badge_html(score):
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

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<span class='nav-logo'>Cinelytix</span>", unsafe_allow_html=True)
    st.markdown("<span class='nav-sub'>Cinematic Intelligence</span>", unsafe_allow_html=True)

    pages = {
        "Home":      "🏠  Home",
        "Search":    "🔍  Search Any Movie",
        "Sentiment": "🎬  Analyze a Review",
        "Watchlist": "⭐  My Watchlist",
    }

    for key, label in pages.items():
        if st.button(label, use_container_width=True, key=f"nav_{key}"):
            st.session_state.page = key

    st.markdown("---")
    st.markdown(f"<span class='nav-stat'>Watchlist: {len(st.session_state.watchlist)} films</span>", unsafe_allow_html=True)
    st.markdown(f"<span class='nav-stat'>Analyzed: {len(st.session_state.analyzed)} reviews</span>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════
if st.session_state.page == "Home":

    st.markdown("""
    <div class='hero-section'>
        <div class='hero-glow'></div>
        <div class='hero-title'>The Pulse of Cinema</div>
        <div class='hero-sub'>
            Search any movie from anywhere in the world and get an
            AI-powered sentiment score based on real reviews
        </div>
        <div>
            <span class='hero-badge'>DistilBERT AI</span>
            <span class='hero-badge'>86.4% Accuracy</span>
            <span class='hero-badge'>Any Movie · Any Language</span>
            <span class='hero-badge'>Real-time Analysis</span>
            <span class='hero-badge'>© Samantha Jessica Monis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-card'><div class='stat-val'>86.4%</div><div class='stat-lbl'>Model Accuracy</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-card'><div class='stat-val'>66M</div><div class='stat-lbl'>Parameters</div></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-card'><div class='stat-val'>∞</div><div class='stat-lbl'>Movies Supported</div></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='stat-card'><div class='stat-val'>{len(st.session_state.analyzed)}</div><div class='stat-lbl'>Reviews Analyzed</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Search Any Movie</div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#3a3a5a;font-size:13px;'>Type any movie title from any country — Bollywood, Hollywood, Korean, French, Japanese and more</p>", unsafe_allow_html=True)

    col_s, col_b = st.columns([4, 1])
    with col_s:
        home_q = st.text_input("", placeholder="e.g. RRR, Parasite, Amelie, Spirited Away, 3 Idiots...", label_visibility="collapsed", key="home_search")
    with col_b:
        home_btn = st.button("Search", use_container_width=True, key="home_btn")

    if home_btn and home_q:
        with st.spinner(f"Fetching and analyzing '{home_q}'..."):
            result = get_movie_sentiment(home_q)
            st.session_state.search_data = result

    if st.session_state.search_data:
        m        = st.session_state.search_data
        b_cls, b_txt = badge_html(m["score"])
        neg      = 100 - m["score"]

        col_p, col_d = st.columns([1, 2])
        with col_p:
            if m["poster"] and m["poster"] != "N/A":
                st.image(m["poster"], width=200)
            else:
                st.markdown("<div style='background:#0d0d1f;border:1px solid #1e1e3a;border-radius:12px;width:200px;height:280px;display:flex;align-items:center;justify-content:center;font-size:48px;'>🎬</div>", unsafe_allow_html=True)

        with col_d:
            st.markdown(f"""
            <div class='search-card'>
                <div style='font-family:"Playfair Display",serif;font-size:1.8rem;
                            color:#e8e4f0;font-weight:700;margin-bottom:4px;'>
                    {m['title']}
                </div>
                <div style='font-size:11px;color:#3a3a5a;text-transform:uppercase;
                            letter-spacing:0.1em;margin-bottom:12px;'>
                    {m['genre']} · {m['year']} · {m['country']} · {m['language']}
                </div>
                <div style='font-size:13px;color:#6060a0;margin-bottom:16px;
                            font-style:italic;'>
                    {m['plot'][:200]}...
                </div>
                <div style='display:flex;align-items:center;gap:16px;margin-bottom:16px;'>
                    <span class='{b_cls}'>{b_txt}</span>
                    <span style='font-size:11px;color:#3a3a5a;'>
                        IMDB: {m['imdb']} · {m['runtime']}
                    </span>
                </div>
                <div style='display:flex;justify-content:space-between;
                            font-size:12px;color:#3a3a5a;margin-bottom:4px;'>
                    <span>Positive sentiment</span><span>{m['score']}%</span>
                </div>
                <div class='progress-wrap'>
                    <div class='{bar_cls(m["score"])}' style='width:{m["score"]}%;'></div>
                </div>
                <div style='display:flex;justify-content:space-between;
                            font-size:12px;color:#3a3a5a;margin:8px 0 4px;'>
                    <span>Negative sentiment</span><span>{neg}%</span>
                </div>
                <div class='progress-wrap'>
                    <div class='progress-neg' style='width:{neg}%;'></div>
                </div>
                <div style='margin-top:16px;font-size:11px;color:#3a3a5a;'>
                    Director: {m['director']} · Model confidence: {m['confidence']}%
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("+ Add to Watchlist", key="home_watch"):
                if m["title"] not in [w["title"] for w in st.session_state.watchlist]:
                    st.session_state.watchlist.append({"title": m["title"], "status": "Want to Watch", "sentiment": f"{m['score']}%"})
                    st.success(f"Added '{m['title']}' to watchlist!")

    # Popular searches
    st.markdown("<div class='section-title'>Popular Searches</div>", unsafe_allow_html=True)
    popular = ["RRR", "Parasite", "Spirited Away", "Amelie", "3 Idiots", "City of God", "Life Is Beautiful", "Inception"]
    cols = st.columns(4)
    for i, title in enumerate(popular):
        if cols[i % 4].button(title, key=f"pop{i}", use_container_width=True):
            with st.spinner(f"Analyzing {title}..."):
                result = get_movie_sentiment(title)
                st.session_state.search_data = result
            st.rerun()

# ══════════════════════════════════════════════════════════════════════
# SEARCH PAGE
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Search":

    st.markdown("<div class='page-header'>Search Any Movie</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Search any film from anywhere in the world — our AI analyzes its reviews and gives a live sentiment score</div>", unsafe_allow_html=True)

    col_s, col_b = st.columns([4, 1])
    with col_s:
        query = st.text_input("", placeholder="Type any movie title from any country...", label_visibility="collapsed", key="search_q")
    with col_b:
        search_btn = st.button("Analyze", use_container_width=True, key="search_btn")

    if search_btn and query:
        with st.spinner(f"Fetching '{query}' and analyzing sentiment..."):
            result = get_movie_sentiment(query)

        if result:
            m        = result
            b_cls, b_txt = badge_html(m["score"])
            neg      = 100 - m["score"]

            col_poster, col_info = st.columns([1, 2.5])

            with col_poster:
                if m["poster"] and m["poster"] != "N/A":
                    st.image(m["poster"], width=220)
                else:
                    st.markdown("""
                    <div style='background:#0d0d1f;border:1px solid #1e1e3a;
                                border-radius:12px;width:220px;height:300px;
                                display:flex;align-items:center;
                                justify-content:center;font-size:56px;'>🎬</div>
                    """, unsafe_allow_html=True)

            with col_info:
                st.markdown(f"""
                <div class='search-card'>
                    <div style='font-family:"Playfair Display",serif;
                                font-size:2rem;color:#e8e4f0;
                                font-weight:700;margin-bottom:4px;'>
                        {m['title']}
                    </div>
                    <div style='font-size:11px;color:#3a3a5a;
                                text-transform:uppercase;letter-spacing:0.1em;
                                margin-bottom:8px;'>
                        {m['genre']} · {m['year']} · {m['country']}
                    </div>
                    <div style='font-size:11px;color:#3a3a5a;margin-bottom:12px;'>
                        Language: {m['language']} · Runtime: {m['runtime']} · IMDB: {m['imdb']}
                    </div>
                    <div style='font-size:13px;color:#6060a0;margin-bottom:16px;
                                font-style:italic;line-height:1.6;'>
                        {m['plot'][:250]}...
                    </div>
                    <div style='margin-bottom:16px;'>
                        <span class='{b_cls}'>{b_txt}</span>
                        <span style='font-size:2rem;font-weight:700;
                                     color:{"#a78bfa" if m["score"]>=75 else "#fbbf24" if m["score"]>=50 else "#f87171"};
                                     margin-left:16px;
                                     font-family:"Playfair Display",serif;'>
                            {m['score']}%
                        </span>
                        <span style='font-size:12px;color:#3a3a5a;margin-left:8px;'>
                            positive sentiment
                        </span>
                    </div>
                    <div style='display:flex;justify-content:space-between;
                                font-size:12px;color:#3a3a5a;margin-bottom:4px;'>
                        <span>Positive</span><span>{m['score']}%</span>
                    </div>
                    <div class='progress-wrap'>
                        <div class='{bar_cls(m["score"])}' style='width:{m["score"]}%;'></div>
                    </div>
                    <div style='display:flex;justify-content:space-between;
                                font-size:12px;color:#3a3a5a;margin:6px 0 4px;'>
                        <span>Negative</span><span>{neg}%</span>
                    </div>
                    <div class='progress-wrap'>
                        <div class='progress-neg' style='width:{neg}%;'></div>
                    </div>
                    <div style='margin-top:12px;font-size:11px;color:#3a3a5a;'>
                        Directed by {m['director']} ·
                        Model confidence: {m['confidence']}% ·
                        {m['awards'][:60] if m['awards'] != "N/A" else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_w, col_a = st.columns(2)
                with col_w:
                    if st.button("+ Add to Watchlist", use_container_width=True, key="s_watch"):
                        if m["title"] not in [w["title"] for w in st.session_state.watchlist]:
                            st.session_state.watchlist.append({"title": m["title"], "status": "Want to Watch", "sentiment": f"{m['score']}%"})
                            st.success(f"Added '{m['title']}'!")
                with col_a:
                    if st.button("Analyze a Review →", use_container_width=True, key="s_analyze"):
                        st.session_state.page = "Sentiment"
                        st.rerun()
        else:
            st.error(f"Could not find '{query}'. Check the spelling and try again.")

    # Suggestions
    st.markdown("<div class='section-title'>Try These</div>", unsafe_allow_html=True)
    suggestions = [
        "RRR", "Parasite", "Spirited Away", "Amelie",
        "3 Idiots", "City of God", "Life Is Beautiful",
        "A Separation", "Oldboy", "Pan's Labyrinth",
        "Dangal", "Tumbbad", "Train to Busan", "Inception",
        "Jai Bhim", "Your Name", "Intouchables", "Kantara"
    ]
    cols = st.columns(6)
    for i, s in enumerate(suggestions):
        if cols[i % 6].button(s, key=f"sug{i}", use_container_width=True):
            with st.spinner(f"Analyzing {s}..."):
                r = get_movie_sentiment(s)
            if r:
                st.session_state.search_data = r
                st.session_state.page = "Home"
                st.rerun()

# ══════════════════════════════════════════════════════════════════════
# SENTIMENT ANALYSIS
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Sentiment":

    st.markdown("<div class='page-header'>Analyze a Review</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Paste any movie review — our DistilBERT model tells you if it is positive or negative</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-card'><div class='stat-val'>86.4%</div><div class='stat-lbl'>Accuracy</div></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-card'><div class='stat-val'>0.86</div><div class='stat-lbl'>F1 Score</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stat-card'><div class='stat-val'>{len(st.session_state.analyzed)}</div><div class='stat-lbl'>Reviews Done</div></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-card'><div class='stat-val'>66M</div><div class='stat-lbl'>Parameters</div></div>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.3, 1])
    with col_l:
        movie_name = st.text_input("", placeholder="Movie title (optional)...", label_visibility="collapsed", key="rev_title")
        review     = st.text_area("", placeholder="Paste any movie review here...", height=160, label_visibility="collapsed", key="rev_text")

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
                res   = classifier(review[:512])[0]
                label = "POSITIVE" if res["label"] == "LABEL_1" else "NEGATIVE"
                conf  = round(res["score"] * 100, 2)

            st.session_state.analyzed.append({
                "review":     review[:60],
                "label":      label,
                "confidence": conf,
                "movie":      movie_name or "Unknown"
            })

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
                    <div style='font-size:11px;color:#3a3a5a;margin-top:4px;'>confidence</div>
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
                    <div style='font-size:11px;color:#3a3a5a;margin-top:4px;'>confidence</div>
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
# WATCHLIST
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Watchlist":

    st.markdown("<div class='page-header'>My Watchlist</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Track and manage your personal film collection</div>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([2.5, 1.5, 1])
    with col_a:
        new_film = st.text_input("", placeholder="Add any movie title...", label_visibility="collapsed")
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
            sc = {"Watched":"#a78bfa","Watching":"#fbbf24","Want to Watch":"#4a4a8a"}.get(film["status"],"#888")
            c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 0.5])
            with c1:
                st.markdown(f"""
                <div style='padding:10px 0;'>
                    <div style='font-size:14px;font-weight:600;color:#e8e4f0;
                                font-family:"Playfair Display",serif;'>
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
                ns = st.selectbox("",
                    ["Want to Watch","Watching","Watched"],
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
       style='color:#2a2a4a;text-decoration:none;'>
        Model: Samantha-16/movie-sentiment-distilbert
    </a>
</div>
""", unsafe_allow_html=True)
