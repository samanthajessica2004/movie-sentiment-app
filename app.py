import streamlit as st
from transformers import pipeline
import random

st.set_page_config(
    page_title="CineScore",
    page_icon="🎬",
    layout="wide"
)

# ── CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@300;400;500;600&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: #07070f;
}

/* Hide streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 2rem; max-width: 1400px; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0d1a !important;
    border-right: 1px solid #1a1a2e;
}
section[data-testid="stSidebar"] * { color: #888 !important; }

/* Nav header */
.nav-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    color: #c8a96e !important;
    font-weight: 700;
    padding: 1.5rem 0 0.5rem;
    display: block;
    text-shadow: 0 0 20px rgba(200,169,110,0.3);
}
.nav-sub {
    font-size: 10px;
    letter-spacing: 0.15em;
    color: #333 !important;
    text-transform: uppercase;
    margin-bottom: 2rem;
    display: block;
}

/* Cards */
.movie-card {
    background: #0d0d1a;
    border: 1px solid #1a1a2e;
    border-radius: 16px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    position: relative;
    transition: border-color 0.3s;
}
.movie-card:hover { border-color: #7b5ea7; }

.sentiment-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.badge-pos { background: #0d2b1a; color: #4db87a; border: 1px solid #1a4a2e; }
.badge-neg { background: #2b0d0d; color: #e05858; border: 1px solid #4a1a1a; }
.badge-mix { background: #201a0c; color: #c8a96e; border: 1px solid #3a2e0c; }

.score-large {
    font-size: 2rem;
    font-weight: 700;
    font-family: 'Playfair Display', serif;
}
.score-pos { color: #4db87a; }
.score-neg { color: #e05858; }
.score-mix { color: #c8a96e; }

.progress-bar-wrap {
    background: #1a1a2e;
    border-radius: 50px;
    height: 6px;
    overflow: hidden;
    margin: 8px 0;
}
.progress-bar-fill-pos {
    height: 100%;
    background: linear-gradient(90deg, #1a7a40, #4db87a);
    border-radius: 50px;
}
.progress-bar-fill-neg {
    height: 100%;
    background: linear-gradient(90deg, #7a1a1a, #e05858);
    border-radius: 50px;
}
.progress-bar-fill-mix {
    height: 100%;
    background: linear-gradient(90deg, #7a5a0a, #c8a96e);
    border-radius: 50px;
}

.stat-card {
    background: #0d0d1a;
    border: 1px solid #1a1a2e;
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
}
.stat-val {
    font-size: 1.8rem;
    font-weight: 700;
    color: #c8a96e;
    font-family: 'Playfair Display', serif;
}
.stat-lbl {
    font-size: 10px;
    color: #444;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}

.trending-tag {
    font-size: 9px;
    padding: 2px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.08em;
}
.tag-up { background: #0d2b1a; color: #4db87a; }
.tag-steady { background: #201a0c; color: #c8a96e; }
.tag-down { background: #2b0d0d; color: #e05858; }

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #e8e0d0;
    margin: 1.5rem 0 1rem;
    border-left: 3px solid #c8a96e;
    padding-left: 12px;
}

.page-header {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #e8e0d0;
    margin: 1.5rem 0 0.3rem;
}

.page-subheader {
    font-size: 13px;
    color: #444;
    margin-bottom: 1.5rem;
}

.result-box-pos {
    background: linear-gradient(135deg, #0a1f12, #0d2b1a);
    border: 2px solid #4db87a;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
}
.result-box-neg {
    background: linear-gradient(135deg, #1f0a0a, #2b0d0d);
    border: 2px solid #e05858;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
}

.watchlist-item {
    background: #0d0d1a;
    border: 1px solid #1a1a2e;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.footer {
    text-align: center;
    padding: 2rem;
    border-top: 1px solid #1a1a2e;
    color: #222;
    font-size: 11px;
    margin-top: 3rem;
    letter-spacing: 0.05em;
}

.stButton button {
    background: linear-gradient(135deg, #c8a96e, #a07840) !important;
    color: #07070f !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    font-size: 13px !important;
    letter-spacing: 0.5px !important;
}

.stTextArea textarea {
    background: #0d0d1a !important;
    border: 1px solid #1a1a2e !important;
    border-radius: 12px !important;
    color: #e8e0d0 !important;
    font-size: 14px !important;
}

.stTextInput input {
    background: #0d0d1a !important;
    border: 1px solid #1a1a2e !important;
    border-radius: 10px !important;
    color: #e8e0d0 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────
TRENDING_MOVIES = [
    {"title": "Dune: Part Two",      "genre": "SCI-FI",      "year": 2024, "score": 91, "trend": "up",     "change": "+14%"},
    {"title": "Oppenheimer",         "genre": "DRAMA",       "year": 2023, "score": 88, "trend": "steady",  "change": "+2%"},
    {"title": "Poor Things",         "genre": "FANTASY",     "year": 2023, "score": 85, "trend": "up",     "change": "+9%"},
    {"title": "The Zone of Interest","genre": "HISTORICAL",  "year": 2023, "score": 79, "trend": "steady",  "change": "+1%"},
    {"title": "Saltburn",            "genre": "THRILLER",    "year": 2023, "score": 62, "trend": "down",   "change": "-5%"},
    {"title": "Past Lives",          "genre": "ROMANCE",     "year": 2023, "score": 94, "trend": "up",     "change": "+7%"},
    {"title": "Killers of the Flower Moon", "genre": "WESTERN", "year": 2023, "score": 83, "trend": "steady", "change": "+3%"},
    {"title": "Priscilla",           "genre": "BIOGRAPHY",   "year": 2023, "score": 71, "trend": "down",   "change": "-3%"},
    {"title": "The Holdovers",       "genre": "COMEDY",      "year": 2023, "score": 89, "trend": "up",     "change": "+11%"},
]

# ── Session State ─────────────────────────────────────────────────────
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []
if "page" not in st.session_state:
    st.session_state.page = "Sentiment"
if "analyzed" not in st.session_state:
    st.session_state.analyzed = []

# ── Model ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="Samantha-16/movie-sentiment-distilbert"
    )

classifier = load_model()

# ── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<span class='nav-logo'>CineScore</span>", unsafe_allow_html=True)
    st.markdown("<span class='nav-sub'>Cinematic Intelligence</span>", unsafe_allow_html=True)

    if st.button("🎬  Sentiment Analysis", use_container_width=True):
        st.session_state.page = "Sentiment"
    if st.button("📈  Trending Movies", use_container_width=True):
        st.session_state.page = "Trending"
    if st.button("⭐  My Watchlist", use_container_width=True):
        st.session_state.page = "Watchlist"

    st.markdown("---")
    st.markdown(
        f"<div style='font-size:11px;color:#333;'>Watchlist: {len(st.session_state.watchlist)} films</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div style='font-size:11px;color:#333;margin-top:4px;'>Analyzed: {len(st.session_state.analyzed)} reviews</div>",
        unsafe_allow_html=True
    )

# ── Helper functions ──────────────────────────────────────────────────
def score_color(score):
    if score >= 75: return "score-pos"
    if score >= 50: return "score-mix"
    return "score-neg"

def score_badge(score):
    if score >= 75: return "badge-pos", "Positive"
    if score >= 50: return "badge-mix", "Mixed"
    return "badge-neg", "Negative"

def bar_class(score):
    if score >= 75: return "progress-bar-fill-pos"
    if score >= 50: return "progress-bar-fill-mix"
    return "progress-bar-fill-neg"

def trend_tag(trend, change):
    cls = {"up": "tag-up", "steady": "tag-steady", "down": "tag-down"}[trend]
    icon = {"up": "↑", "steady": "→", "down": "↓"}[trend]
    return f"<span class='trending-tag {cls}'>{icon} {change}</span>"

# ══════════════════════════════════════════════════════════════════════
# PAGE 1 — SENTIMENT ANALYSIS
# ══════════════════════════════════════════════════════════════════════
if st.session_state.page == "Sentiment":

    st.markdown("<div class='page-header'>Sentiment Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subheader'>Analyze any movie review with DistilBERT AI</div>", unsafe_allow_html=True)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("<div class='stat-card'><div class='stat-val'>86.4%</div><div class='stat-lbl'>Model Accuracy</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='stat-card'><div class='stat-val'>66M</div><div class='stat-lbl'>Parameters</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card'><div class='stat-val'>{len(st.session_state.analyzed)}</div><div class='stat-lbl'>Reviews Analyzed</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='stat-card'><div class='stat-val'>5K</div><div class='stat-lbl'>Training Samples</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Analyze a Review</div>", unsafe_allow_html=True)

    col_input, col_result = st.columns([1.2, 1])

    with col_input:
        review = st.text_area(
            "Movie review",
            placeholder="Type or paste any movie review here...",
            height=160,
            label_visibility="collapsed"
        )

        movie_name = st.text_input(
            "Movie title (optional)",
            placeholder="e.g. Inception, Dune, Oppenheimer...",
            label_visibility="collapsed"
        )

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            analyze = st.button("Analyze Sentiment", use_container_width=True)
        with col_btn2:
            add_watch = st.button("+ Add to Watchlist", use_container_width=True)

        if add_watch and movie_name:
            if movie_name not in [w["title"] for w in st.session_state.watchlist]:
                st.session_state.watchlist.append({
                    "title": movie_name,
                    "status": "Want to Watch",
                    "sentiment": "—"
                })
                st.success(f"Added '{movie_name}' to watchlist!")
            else:
                st.warning("Already in watchlist!")

        st.markdown("<div style='margin-top:1rem;font-size:11px;color:#333;text-transform:uppercase;letter-spacing:0.1em;'>Try a sample</div>", unsafe_allow_html=True)

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
            if r1[i].button(s[:22]+"...", key=f"sa{i}"):
                st.session_state["sample_review"] = s

        r2 = st.columns(3)
        for i, s in enumerate(samples[3:]):
            if r2[i].button(s[:22]+"...", key=f"sb{i}"):
                st.session_state["sample_review"] = s

        if "sample_review" in st.session_state:
            review = st.session_state["sample_review"]

    with col_result:
        if analyze and review.strip():
            with st.spinner("Analyzing..."):
                result     = classifier(review)[0]
                label      = "POSITIVE" if result["label"] == "LABEL_1" else "NEGATIVE"
                confidence = round(result["score"] * 100, 2)

            st.session_state.analyzed.append({
                "review": review[:60],
                "label": label,
                "confidence": confidence,
                "movie": movie_name or "Unknown"
            })

            if label == "POSITIVE":
                st.markdown(f"""
                <div class='result-box-pos'>
                    <div style='font-size:48px;margin-bottom:8px;'>🎬</div>
                    <div style='font-size:32px;font-weight:700;color:#4db87a;
                                letter-spacing:4px;margin-bottom:6px;'>POSITIVE</div>
                    <div style='color:#9ee8b8;font-size:13px;margin-bottom:20px;'>
                        Positive sentiment detected
                    </div>
                    <div style='background:#0a1f12;border-radius:50px;
                                height:10px;overflow:hidden;margin:0 auto 12px;'>
                        <div style='width:{confidence}%;height:100%;
                                    background:linear-gradient(90deg,#1a7a40,#4db87a);
                                    border-radius:50px;'></div>
                    </div>
                    <div style='font-size:28px;font-weight:700;color:#4db87a;'>
                        {confidence}%
                    </div>
                    <div style='font-size:11px;color:#4a7a5a;margin-top:4px;'>
                        Confidence score
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-box-neg'>
                    <div style='font-size:48px;margin-bottom:8px;'>🎭</div>
                    <div style='font-size:32px;font-weight:700;color:#e05858;
                                letter-spacing:4px;margin-bottom:6px;'>NEGATIVE</div>
                    <div style='color:#f0a0a0;font-size:13px;margin-bottom:20px;'>
                        Negative sentiment detected
                    </div>
                    <div style='background:#1f0a0a;border-radius:50px;
                                height:10px;overflow:hidden;margin:0 auto 12px;'>
                        <div style='width:{confidence}%;height:100%;
                                    background:linear-gradient(90deg,#7a1a1a,#e05858);
                                    border-radius:50px;'></div>
                    </div>
                    <div style='font-size:28px;font-weight:700;color:#e05858;'>
                        {confidence}%
                    </div>
                    <div style='font-size:11px;color:#7a4a4a;margin-top:4px;'>
                        Confidence score
                    </div>
                </div>
                """, unsafe_allow_html=True)

        elif not analyze:
            st.markdown("""
            <div style='background:#0d0d1a;border:1px dashed #1a1a2e;
                        border-radius:20px;padding:3rem;text-align:center;
                        height:100%;'>
                <div style='font-size:48px;margin-bottom:12px;'>🎬</div>
                <div style='color:#333;font-size:13px;'>
                    Enter a review and click Analyze
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Recent analysis history
    if st.session_state.analyzed:
        st.markdown("<div class='section-title'>Recent Analysis</div>", unsafe_allow_html=True)
        for item in reversed(st.session_state.analyzed[-4:]):
            badge_cls = "badge-pos" if item["label"] == "POSITIVE" else "badge-neg"
            st.markdown(f"""
            <div class='movie-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                        <div style='font-size:13px;color:#888;margin-bottom:4px;'>
                            {item['movie']}
                        </div>
                        <div style='font-size:14px;color:#c8c0b0;'>
                            "{item['review']}..."
                        </div>
                    </div>
                    <div style='text-align:right;margin-left:1rem;flex-shrink:0;'>
                        <span class='sentiment-badge {badge_cls}'>{item['label']}</span>
                        <div style='font-size:18px;font-weight:700;
                                    color:{"#4db87a" if item["label"]=="POSITIVE" else "#e05858"};
                                    margin-top:4px;'>
                            {item['confidence']}%
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# PAGE 2 — TRENDING MOVIES
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Trending":

    st.markdown("<div class='page-header'>Trending Movies</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subheader'>Real-time sentiment scores across top films</div>", unsafe_allow_html=True)

    # Summary stats
    pos_count  = sum(1 for m in TRENDING_MOVIES if m["score"] >= 75)
    mix_count  = sum(1 for m in TRENDING_MOVIES if 50 <= m["score"] < 75)
    neg_count  = sum(1 for m in TRENDING_MOVIES if m["score"] < 50)
    avg_score  = round(sum(m["score"] for m in TRENDING_MOVIES) / len(TRENDING_MOVIES))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='stat-card'><div class='stat-val' style='color:#c8a96e;'>{avg_score}%</div><div class='stat-lbl'>Avg Sentiment</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='stat-card'><div class='stat-val' style='color:#4db87a;'>{pos_count}</div><div class='stat-lbl'>Positive Films</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='stat-card'><div class='stat-val' style='color:#c8a96e;'>{mix_count}</div><div class='stat-lbl'>Mixed Films</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='stat-card'><div class='stat-val' style='color:#e05858;'>{neg_count}</div><div class='stat-lbl'>Negative Films</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Now Trending</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]

    for i, movie in enumerate(TRENDING_MOVIES):
        badge_cls, badge_txt = score_badge(movie["score"])
        bar_cls = bar_class(movie["score"])
        sc_cls  = score_color(movie["score"])

        with cols[i % 3]:
            st.markdown(f"""
            <div class='movie-card'>
                <div style='display:flex;justify-content:space-between;
                            align-items:flex-start;margin-bottom:8px;'>
                    <div>
                        <div style='font-size:15px;font-weight:600;
                                    color:#e8e0d0;margin-bottom:4px;'>
                            {movie['title']}
                        </div>
                        <div style='font-size:10px;color:#444;
                                    text-transform:uppercase;letter-spacing:0.1em;'>
                            {movie['genre']} · {movie['year']}
                        </div>
                    </div>
                    {trend_tag(movie['trend'], movie['change'])}
                </div>
                <div style='display:flex;align-items:center;
                            justify-content:space-between;margin:12px 0 8px;'>
                    <span class='sentiment-badge {badge_cls}'>{badge_txt}</span>
                    <span class='score-large {sc_cls}'>{movie['score']}%</span>
                </div>
                <div class='progress-bar-wrap'>
                    <div class='{bar_cls}' style='width:{movie["score"]}%;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"+ Watchlist", key=f"w{i}", use_container_width=True):
                if movie["title"] not in [w["title"] for w in st.session_state.watchlist]:
                    st.session_state.watchlist.append({
                        "title": movie["title"],
                        "status": "Want to Watch",
                        "sentiment": f"{movie['score']}%"
                    })
                    st.success(f"Added '{movie['title']}'!")
                else:
                    st.info("Already in watchlist!")

# ══════════════════════════════════════════════════════════════════════
# PAGE 3 — WATCHLIST
# ══════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Watchlist":

    st.markdown("<div class='page-header'>My Watchlist</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subheader'>Track films you want to watch</div>", unsafe_allow_html=True)

    # Add movie manually
    st.markdown("<div class='section-title'>Add a Film</div>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        new_movie = st.text_input(
            "Movie title",
            placeholder="Enter movie title...",
            label_visibility="collapsed"
        )
    with col_b:
        status = st.selectbox(
            "Status",
            ["Want to Watch", "Watching", "Watched"],
            label_visibility="collapsed"
        )
    with col_c:
        if st.button("Add Film", use_container_width=True):
            if new_movie:
                if new_movie not in [w["title"] for w in st.session_state.watchlist]:
                    st.session_state.watchlist.append({
                        "title": new_movie,
                        "status": status,
                        "sentiment": "—"
                    })
                    st.success(f"Added '{new_movie}'!")
                else:
                    st.warning("Already in watchlist!")

    st.markdown("<div class='section-title'>My Films</div>", unsafe_allow_html=True)

    if not st.session_state.watchlist:
        st.markdown("""
        <div style='background:#0d0d1a;border:1px dashed #1a1a2e;
                    border-radius:16px;padding:3rem;text-align:center;'>
            <div style='font-size:40px;margin-bottom:12px;'>⭐</div>
            <div style='color:#333;font-size:13px;'>
                Your watchlist is empty. Add films from Trending or Sentiment pages.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Stats
        watched_count = sum(1 for w in st.session_state.watchlist if w["status"] == "Watched")
        watching_count = sum(1 for w in st.session_state.watchlist if w["status"] == "Watching")
        want_count = sum(1 for w in st.session_state.watchlist if w["status"] == "Want to Watch")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"<div class='stat-card'><div class='stat-val'>{want_count}</div><div class='stat-lbl'>Want to Watch</div></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='stat-card'><div class='stat-val'>{watching_count}</div><div class='stat-lbl'>Watching</div></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div class='stat-card'><div class='stat-val'>{watched_count}</div><div class='stat-lbl'>Watched</div></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        for i, film in enumerate(st.session_state.watchlist):
            status_color = {
                "Watched":        "#4db87a",
                "Watching":       "#c8a96e",
                "Want to Watch":  "#7b5ea7"
            }.get(film["status"], "#888")

            col_film, col_status, col_sent, col_del = st.columns([3, 1.5, 1, 0.5])
            with col_film:
                st.markdown(f"""
                <div style='padding:12px 0;'>
                    <div style='font-size:14px;font-weight:600;color:#e8e0d0;'>
                        {film['title']}
                    </div>
                    <div style='font-size:11px;color:#333;margin-top:2px;'>
                        Sentiment: {film['sentiment']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_status:
                st.markdown(f"""
                <div style='padding:12px 0;'>
                    <span style='background:#0d0d1a;border:1px solid {status_color}33;
                                 color:{status_color};font-size:11px;
                                 padding:4px 10px;border-radius:20px;'>
                        {film['status']}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            with col_sent:
                new_status = st.selectbox(
                    "Update",
                    ["Want to Watch", "Watching", "Watched"],
                    index=["Want to Watch", "Watching", "Watched"].index(film["status"]),
                    key=f"sel{i}",
                    label_visibility="collapsed"
                )
                if new_status != film["status"]:
                    st.session_state.watchlist[i]["status"] = new_status
                    st.rerun()
            with col_del:
                if st.button("✕", key=f"del{i}"):
                    st.session_state.watchlist.pop(i)
                    st.rerun()

            st.markdown("<hr style='border-color:#1a1a2e;margin:0;'>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    © 2026 Samantha Jessica Monis · All rights reserved<br>
    <span style='color:#1a1a2e;'>·</span>
    CineScore · Built with DistilBERT · Fine-tuned on IMDB ·
    86.4% Accuracy
    <span style='color:#1a1a2e;'>·</span>
    Model:
    <a href='https://huggingface.co/Samantha-16/movie-sentiment-distilbert'
       style='color:#2a2a3a;text-decoration:none;'>
        Samantha-16/movie-sentiment-distilbert
    </a>
</div>
""", unsafe_allow_html=True)
