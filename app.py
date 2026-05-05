import streamlit as st
from agents.synthesizer import load_latest_briefing

st.set_page_config(
    page_title="AI News Briefing",
    page_icon="📡",
    layout="wide",
)

st.title("AI News Briefing")
st.caption("Four perspectives on today's AI news. You decide what matters.")
st.divider()

briefing = load_latest_briefing()

if briefing is None:
    st.info("No briefing available yet. Run the pipeline first.")
    st.stop()

st.markdown(f"**{briefing.date}** · {briefing.article_count} articles")
st.divider()

LENS_LABELS = {
    "market":  "📈 Market",
    "tech":    "🔬 Tech",
    "society": "🏛 Society",
    "user":    "👤 User",
}

for article in briefing.articles:
    st.markdown(f"### [{article.title}]({article.url})")
    st.caption(f"Source: {article.source}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**{LENS_LABELS['market']}**")
        st.markdown(article.market)
        st.markdown("")
        st.markdown(f"**{LENS_LABELS['tech']}**")
        st.markdown(article.tech)

    with col2:
        st.markdown(f"**{LENS_LABELS['society']}**")
        st.markdown(article.society)
        st.markdown("")
        st.markdown(f"**{LENS_LABELS['user']}**")
        st.markdown(article.user)

    st.divider()
