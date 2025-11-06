import streamlit as st
from textblob import TextBlob
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

# Page config
st.set_page_config(page_title="Sentiment Analyzer Pro", layout="wide", initial_sidebar_state="expanded")

# Initialize session state
if "history" not in st.session_state:
    st.session_state["history"] = []
if "show_details" not in st.session_state:
    st.session_state["show_details"] = False

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 15px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    .header-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .main-title {
        font-size: 48px;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #ffffff 0%, #e0e7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255,255,255,0.9);
        font-size: 18px;
        font-weight: 300;
    }
    
    .result-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.85) 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(10px);
    }
    
    .sentiment-emoji {
        font-size: 80px;
        text-align: center;
        margin: 20px 0;
        animation: bounceIn 0.6s ease;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .history-item {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .history-item:hover {
        transform: translateX(5px);
    }
    
    .stat-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 5px;
    }
    
    .positive-badge { background: #d4edda; color: #155724; }
    .negative-badge { background: #f8d7da; color: #721c24; }
    .neutral-badge { background: #fff3cd; color: #856404; }
    
    div[data-testid="stMetricValue"] {
        font-size: 28px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <div class="main-title">🎭 Sentiment Analyzer Pro</div>
    <div class="subtitle">Analyze emotions and sentiments in your text with AI-powered insights</div>
</div>
""", unsafe_allow_html=True)

# Main input area
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    user_input = st.text_input(
        "Enter your text here:",
        placeholder="Type or paste any text to analyze its sentiment...",
        label_visibility="collapsed"
    )

# Analyze button
if user_input:
    # Perform sentiment analysis
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determine sentiment
    if polarity > 0.1:
        sentiment = "Positive"
        emoji = "😊"
        color = "#10b981"
    elif polarity < -0.1:
        sentiment = "Negative"
        emoji = "😢"
        color = "#ef4444"
    else:
        sentiment = "Neutral"
        emoji = "😐"
        color = "#f59e0b"
    
    # Add to history
    st.session_state["history"].append({
        "text": user_input,
        "sentiment": sentiment,
        "polarity": polarity,
        "subjectivity": subjectivity,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "emoji": emoji
    })
    
    # Display result
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"<div class='sentiment-emoji'>{emoji}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"### Sentiment: **{sentiment}**")
        st.markdown(f"*Analyzed text has a {sentiment.lower()} tone*")
        
        # Progress bar for polarity
        polarity_normalized = (polarity + 1) / 2 * 100
        st.progress(polarity_normalized / 100)
    
    with col3:
        st.metric("Confidence", f"{abs(polarity):.2f}")
        st.metric("Subjectivity", f"{subjectivity:.2f}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Detailed metrics
    if st.checkbox("Show Detailed Analysis", value=st.session_state["show_details"]):
        st.session_state["show_details"] = True
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Polarity Score</div>
                <div class='metric-value'>{polarity:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Subjectivity</div>
                <div class='metric-value'>{subjectivity:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            word_count = len(user_input.split())
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Word Count</div>
                <div class='metric-value'>{word_count}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            char_count = len(user_input)
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-label'>Characters</div>
                <div class='metric-value'>{char_count}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Interpretation
        st.markdown("#### 📊 Interpretation")
        st.info(f"""
        **Polarity** ranges from -1 (very negative) to +1 (very positive). Your text scored **{polarity:.3f}**, indicating a **{sentiment.lower()}** sentiment.
        
        **Subjectivity** ranges from 0 (very objective) to 1 (very subjective). Your text scored **{subjectivity:.3f}**, meaning it is {'more subjective and opinion-based' if subjectivity > 0.5 else 'more objective and factual'}.
        """)

# Sidebar - Statistics and History
with st.sidebar:
    st.markdown("### 📊 Statistics")
    
    if st.session_state["history"]:
        # Calculate stats
        total_analyses = len(st.session_state["history"])
        positive_count = sum(1 for x in st.session_state["history"] if x["sentiment"] == "Positive")
        negative_count = sum(1 for x in st.session_state["history"] if x["sentiment"] == "Negative")
        neutral_count = sum(1 for x in st.session_state["history"] if x["sentiment"] == "Neutral")
        
        avg_polarity = sum(x["polarity"] for x in st.session_state["history"]) / total_analyses
        avg_subjectivity = sum(x["subjectivity"] for x in st.session_state["history"]) / total_analyses
        
        # Display stats
        st.metric("Total Analyses", total_analyses)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("😊", positive_count)
        with col2:
            st.metric("😢", negative_count)
        with col3:
            st.metric("😐", neutral_count)
        
        st.metric("Avg Polarity", f"{avg_polarity:.3f}")
        st.metric("Avg Subjectivity", f"{avg_subjectivity:.3f}")
        
        # Sentiment distribution chart
        st.markdown("#### Sentiment Distribution")
        fig = go.Figure(data=[go.Pie(
            labels=['Positive', 'Negative', 'Neutral'],
            values=[positive_count, negative_count, neutral_count],
            hole=0.4,
            marker=dict(colors=['#10b981', '#ef4444', '#f59e0b'])
        )])
        fig.update_layout(
            showlegend=True,
            height=250,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Polarity trend
        if len(st.session_state["history"]) > 1:
            st.markdown("#### Polarity Trend")
            polarities = [x["polarity"] for x in st.session_state["history"]]
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                y=polarities,
                mode='lines+markers',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            fig2.update_layout(
                showlegend=False,
                height=200,
                margin=dict(l=20, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(range=[-1, 1], gridcolor='rgba(255,255,255,0.2)'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.2)')
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Clear history button
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state["history"] = []
            st.rerun()
    else:
        st.info("No analyses yet. Start by entering some text above!")

# History section
if st.session_state["history"]:
    st.markdown("---")
    st.markdown("### 📝 Recent Analysis History")
    
    # Show last 5 entries
    for entry in reversed(st.session_state["history"][-5:]):
        badge_class = f"{entry['sentiment'].lower()}-badge"
        st.markdown(f"""
        <div class='history-item'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <span style='font-size: 24px;'>{entry['emoji']}</span>
                <span class='stat-badge {badge_class}'>{entry['sentiment']}</span>
            </div>
            <p style='margin: 10px 0; color: #374151;'><strong>{entry['text'][:100]}{'...' if len(entry['text']) > 100 else ''}</strong></p>
            <div style='display: flex; justify-content: space-between; font-size: 12px; color: #6b7280;'>
                <span>Polarity: {entry['polarity']:.3f}</span>
                <span>Subjectivity: {entry['subjectivity']:.3f}</span>
                <span>{entry['timestamp']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Export option
    if st.button("📥 Export History as CSV"):
        df = pd.DataFrame(st.session_state["history"])
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="sentiment_analysis_history.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.7); padding: 20px;'>
    <p>Powered by TextBlob & Streamlit | Built with ❤️</p>
</div>
""", unsafe_allow_html=True)