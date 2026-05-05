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

def render_lens(label, lens):
    st.markdown(f"**{label}**")
    st.markdown(f"*{lens.insight}*")
    for bullet in lens.bullets:
        st.markdown(f"- {bullet}")

for article in briefing.articles:
    st.markdown(f"### [{article.title}]({article.url})")
    st.caption(f"Source: {article.source}")

    col1, col2 = st.columns(2)

    with col1:
        render_lens(LENS_LABELS["market"], article.market)
        st.markdown("")
        render_lens(LENS_LABELS["tech"], article.tech)

    with col2:
        render_lens(LENS_LABELS["society"], article.society)
        st.markdown("")
        render_lens(LENS_LABELS["user"], article.user)

    st.divider()
