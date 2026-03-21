import streamlit as st
from transformers import pipeline

st.set_page_config(
    page_title="CineScore",
    page_icon="🎬",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@300;400;500&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #050508, #0a0a14, #080810);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
}

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

h1 {
    font-family: 'Playfair Display', serif !important;
    color: #c8a96e !important;
    text-align: center;
    font-size: 3.5rem !important;
    text-shadow: 0 0 40px rgba(200,169,110,0.4);
}

.subtitle {
    text-align: center;
    color: #4a4845;
    font-size: 12px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.stat-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 1.5rem 0;
}

.stat-box {
    background: rgba(20,20,30,0.7);
    border: 1px solid #1e1e2a;
    border-radius: 12px;
    padding: 14px 24px;
    text-align: center;
    min-width: 100px;
}

.stat-value {
    font-size: 22px;
    font-weight: 600;
    color: #c8a96e;
}

.stat-label {
    font-size: 11px;
    color: #4a4845;
    text-transform: uppercase;
    margin-top: 4px;
}

.positive-box {
    background: linear-gradient(135deg, #0d2b1a, #1a4a2e);
    border: 2px solid #4db87a;
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    margin-top: 1rem;
}

.negative-box {
    background: linear-gradient(135deg, #2b0d0d, #4a1a1a);
    border: 2px solid #e05858;
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    margin-top: 1rem;
}

.result-label {
    font-size: 36px;
    font-weight: 700;
    letter-spacing: 4px;
    margin-bottom: 8px;
}

.confidence {
    font-size: 18px;
    font-weight: 500;
    margin-top: 12px;
}

.stTextArea textarea {
    background: rgba(20,20,30,0.8) !important;
    border: 1px solid #2a2a35 !important;
    border-radius: 12px !important;
    color: #e2ddd6 !important;
    font-size: 15px !important;
}

.stButton button {
    background: linear-gradient(135deg, #c8a96e, #a07840) !important;
    color: #050508 !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 32px !important;
    font-size: 16px !important;
    width: 100% !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

.sample-btn {
    background: rgba(20,20,30,0.6) !important;
    border: 1px solid #252535 !important;
    border-radius: 20px !important;
    color: #888580 !important;
    font-size: 11px !important;
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="Samantha-16/movie-sentiment-distilbert"
    )

classifier = load_model()

# Title
st.markdown("<h1>CineScore</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>AI · Movie Sentiment Analysis · DistilBERT · 86.4% Accuracy</div>",
    unsafe_allow_html=True
)

# Stats
st.markdown("""
<div class='stat-container'>
    <div class='stat-box'>
        <div class='stat-value'>86.4%</div>
        <div class='stat-label'>Accuracy</div>
    </div>
    <div class='stat-box'>
        <div class='stat-value'>66M</div>
        <div class='stat-label'>Parameters</div>
    </div>
    <div class='stat-box'>
        <div class='stat-value'>5K</div>
        <div class='stat-label'>Training samples</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Input
review = st.text_area(
    "Movie Review",
    placeholder="Type any movie review here...",
    height=150,
    label_visibility="collapsed"
)

# Sample reviews
st.markdown(
    "<div style='text-align:center;font-size:11px;color:#4a4845;text-transform:uppercase;letter-spacing:0.1em;margin:0.5rem 0;'>Try a sample</div>",
    unsafe_allow_html=True
)

samples = [
    "This movie was absolutely brilliant!",
    "Terrible film. Complete waste of time.",
    "One of the best movies I have ever seen!",
    "The plot made no sense whatsoever.",
    "Stunning visuals but weak storyline.",
    "A perfect blend of action and emotion!",
]

cols = st.columns(3)
for i, sample in enumerate(samples[:3]):
    if cols[i].button(sample[:30] + "...", key=f"s{i}"):
        review = sample

cols2 = st.columns(3)
for i, sample in enumerate(samples[3:]):
    if cols2[i].button(sample[:30] + "...", key=f"s{i+3}"):
        review = sample

# Analyze button
if st.button("Analyze Sentiment"):
    if not review.strip():
        st.warning("Please enter a movie review first.")
    else:
        with st.spinner("Analyzing..."):
            result     = classifier(review)[0]
            label      = "POSITIVE" if result["label"] == "LABEL_1" else "NEGATIVE"
            confidence = round(result["score"] * 100, 2)

        if label == "POSITIVE":
            st.markdown(f"""
            <div class='positive-box'>
                <div style='font-size:56px;margin-bottom:12px;'>🎬</div>
                <div class='result-label' style='color:#4db87a;'>POSITIVE</div>
                <div style='color:#9ee8b8;font-size:15px;'>
                    The review expresses positive sentiment
                </div>
                <div style='background:#0a1f12;border-radius:50px;
                            height:12px;overflow:hidden;
                            margin:16px auto;max-width:400px;'>
                    <div style='width:{confidence}%;height:100%;
                                background:linear-gradient(90deg,#1a7a40,#4db87a);
                                border-radius:50px;'></div>
                </div>
                <div class='confidence' style='color:#4db87a;'>
                    {confidence}% Confidence
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='negative-box'>
                <div style='font-size:56px;margin-bottom:12px;'>🎭</div>
                <div class='result-label' style='color:#e05858;'>NEGATIVE</div>
                <div style='color:#f0a0a0;font-size:15px;'>
                    The review expresses negative sentiment
                </div>
                <div style='background:#1f0a0a;border-radius:50px;
                            height:12px;overflow:hidden;
                            margin:16px auto;max-width:400px;'>
                    <div style='width:{confidence}%;height:100%;
                                background:linear-gradient(90deg,#7a1a1a,#e05858);
                                border-radius:50px;'></div>
                </div>
                <div class='confidence' style='color:#e05858;'>
                    {confidence}% Confidence
                </div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='text-align:center;margin-top:3rem;
            padding:1rem;border-top:1px solid #1a1a24;
            color:#2a2a35;font-size:11px;'>
    Built with DistilBERT · Fine-tuned on IMDB ·
    Model: Samantha-16/movie-sentiment-distilbert
</div>
""", unsafe_allow_html=True)
