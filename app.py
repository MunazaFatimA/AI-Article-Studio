# ============================================================
# 🔑 API KEYS LOADER — Streamlit Cloud + Local
# ============================================================
import streamlit as st
import os

# Streamlit secrets ko environment mein daalo
# Taake utils/ ki files bhi keys padh sakein
try:
    for key_name in ["GROQ_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY", 
                     "COHERE_API_KEY", "TAVILY_API_KEY", "UNSPLASH_API_KEY", "PEXELS_API_KEY"]:
        if key_name in st.secrets:
            os.environ[key_name] = st.secrets[key_name]
except Exception:
    pass  # Local pe .env se chalti rahegi


# ============================================================

import time
import re
from utils.ai_writer import generate_article
from utils.plagiarism import check_plagiarism
from utils.humanizer import humanize_text
from utils.images import fetch_images, get_fallback_images
from utils.doc_export import export_to_docx
from utils.ai_detector import detect_ai, get_detailed_report

import sys
import warnings
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['PYTORCH_NO_CUDA_MEMORY_CACHING'] = '1'
os.environ['NUMEXPR_NUM_THREADS'] = '1'
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

from PIL import Image
st.write("Groq Key:", " found" if os.getenv("GROQ_API_KEY") else " empty")
# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="ArticleForge",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- PROFESSIONAL CSS ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .main { background: linear-gradient(180deg, #0a0e14 0%, #0d1117 100%); }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; max-width: 1180px; }
    
    h1, h2, h3, h4, h5, p, div, span, label { color: #e6edf3 !important; }
    h1 { font-size: 1.9rem !important; font-weight: 700 !important; color: #f0f6fc !important; letter-spacing: -0.4px; }
    h2 { font-size: 1.4rem !important; font-weight: 600 !important; color: #f0f6fc !important; }
    
    .stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label, .stCheckbox label, .stMultiSelect label {
        color: #8b949e !important; font-weight: 600 !important; font-size: 0.72rem !important;
        text-transform: uppercase !important; letter-spacing: 0.6px !important;
    }
    
    .stTextInput > div > div > input, .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select, .stMultiSelect > div > div {
        background: #161b22 !important; border: 1px solid #30363d !important;
        border-radius: 10px !important; color: #e6edf3 !important;
        padding: 11px 14px !important; font-size: 0.9rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #58a6ff !important; box-shadow: 0 0 0 3px rgba(88,166,255,0.18) !important;
        background: #0d1117 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
        color: #ffffff !important; border: none !important;
        border-radius: 10px !important; padding: 11px 26px !important;
        font-weight: 600 !important; font-size: 0.9rem !important; width: 100% !important;
        box-shadow: 0 2px 8px rgba(35,134,54,0.25) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2ea043 0%, #3fb950 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 14px rgba(35,134,54,0.35) !important;
    }
    .stButton > button:active { transform: translateY(0) !important; }
    
    .stContainer { background: #161b22 !important; border: 1px solid #30363d !important; border-radius: 14px !important; padding: 22px 26px !important; }
    
    section[data-testid="stSidebar"] {
        background: #0d1117 !important;
        border-right: 1px solid #21262d !important;
    }
    section[data-testid="stSidebar"] > div { background: #0d1117 !important; }
    
    .metric-card {
        background: linear-gradient(145deg, #161b22 0%, #1c2129 100%);
        border-radius: 12px; padding: 18px 20px; text-align: center;
        border: 1px solid #30363d;
        transition: transform 0.2s ease, border-color 0.2s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .metric-card:hover { transform: translateY(-2px); border-color: #484f58; }
    .metric-value { font-size: 1.85rem; font-weight: 700; color: #f0f6fc !important; letter-spacing: -0.5px; }
    .metric-label { font-size: 0.68rem; color: #8b949e !important; text-transform: uppercase; letter-spacing: 0.6px; margin-top: 4px; }
    
    .chip {
        display: inline-block; padding: 5px 13px; border-radius: 20px;
        margin: 4px 6px 4px 0; font-size: 0.75rem; font-weight: 500;
        transition: transform 0.15s ease;
    }
    .chip:hover { transform: scale(1.04); }
    .chip-short { background: rgba(88,166,255,0.12); color: #58a6ff; border: 1px solid rgba(88,166,255,0.25); }
    .chip-long { background: rgba(46,160,67,0.12); color: #3fb950; border: 1px solid rgba(46,160,67,0.25); }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #238636, #3fb950) !important;
        border-radius: 8px !important; height: 5px !important;
    }
    
    .article-container {
        background: linear-gradient(180deg, #161b22 0%, #1a1f27 100%);
        border-radius: 14px; padding: 28px 32px;
        border: 1px solid #30363d; color: #e6edf3 !important;
        line-height: 1.85; font-size: 0.95rem; max-height: 520px; overflow-y: auto;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }
    .article-container h1 { font-size: 1.55rem !important; font-weight: 700 !important; color: #f0f6fc !important; }
    .article-container h2 { font-size: 1.25rem !important; font-weight: 600 !important; color: #f0f6fc !important; margin-top: 22px; }
    .article-container h3 { font-size: 1.08rem !important; font-weight: 600 !important; color: #e6edf3 !important; margin-top: 16px; }
    .article-container p { color: #c9d1d9 !important; }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px; background: #161b22; border-radius: 10px;
        padding: 5px; border: 1px solid #30363d;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; padding: 7px 18px; font-weight: 500;
        font-size: 0.8rem; color: #8b949e !important; text-transform: uppercase;
        transition: all 0.15s ease;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #21262d, #30363d) !important;
        color: #f0f6fc !important; box-shadow: 0 1px 4px rgba(0,0,0,0.2);
    }
    
    .comparison-table {
        width: 100%; border-collapse: collapse; font-size: 0.85rem;
        background: #161b22; border-radius: 12px; overflow: hidden;
        border: 1px solid #30363d; box-shadow: 0 2px 10px rgba(0,0,0,0.15);
    }
    .comparison-table th {
        background: #0d1117; padding: 10px 16px; text-align: left;
        font-weight: 600; font-size: 0.7rem; color: #8b949e !important;
        text-transform: uppercase; letter-spacing: 0.4px;
        border-bottom: 2px solid #30363d;
    }
    .comparison-table td {
        padding: 10px 16px; border-bottom: 1px solid #21262d;
        color: #e6edf3 !important;
    }
    .comparison-table tr:hover td { background: rgba(88,166,255,0.04); }
    .comparison-table .best-row { background: rgba(35,134,54,0.12) !important; }
    .comparison-table .best-row:hover td { background: rgba(35,134,54,0.18) !important; }
    
    .score-good { color: #3fb950 !important; font-weight: 600; }
    .score-medium { color: #d29922 !important; font-weight: 600; }
    .score-poor { color: #f85149 !important; font-weight: 600; }
    
    .stRadio > div {
        display: flex; gap: 10px; background: #161b22;
        padding: 8px 12px; border-radius: 10px; border: 1px solid #30363d;
    }
    .stRadio label {
        color: #e6edf3 !important; font-size: 0.85rem !important;
        font-weight: 500 !important; padding: 7px 16px !important;
        border-radius: 8px !important; transition: all 0.15s ease;
    }
    .stRadio label[data-checked="true"] {
        background: linear-gradient(135deg, #238636, #2ea043) !important;
        color: #ffffff !important; box-shadow: 0 2px 6px rgba(35,134,54,0.3);
    }
    
    .footer {
        text-align: center; padding: 22px; color: #484f58 !important;
        font-size: 0.75rem; border-top: 1px solid #21262d; margin-top: 36px;
    }
    
    hr { border: none; border-top: 1px solid #21262d; margin: 18px 0; }
    
    .section-title {
        font-size: 11px; font-weight: 600; color: #8b949e;
        text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 10px;
    }
    
    .image-upload-container {
        border: 2px dashed rgba(88,166,255,0.25); border-radius: 12px;
        padding: 22px; text-align: center; background: #0d1117;
        transition: all 0.2s ease;
    }
    .image-upload-container:hover {
        border-color: #58a6ff; background: rgba(88,166,255,0.06);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%) !important;
        box-shadow: 0 2px 8px rgba(31,111,235,0.3) !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #388bfd 0%, #58a6ff 100%) !important;
        box-shadow: 0 4px 14px rgba(31,111,235,0.4) !important;
    }
    
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #484f58; }
    
    .stMultiSelect [data-baseweb="tag"] {
        background: rgba(88,166,255,0.15) !important;
        border-color: rgba(88,166,255,0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 20px; padding-bottom: 12px; border-bottom: 1px solid #21262d;">
        <div style="font-size: 22px; font-weight: 700; color: #f0f6fc; letter-spacing: -0.6px;">
             Article<span style="color: #58a6ff;">Forge</span>
        </div>
        <div style="font-size: 11px; color: #484f58; margin-top: 4px;">v2.0 · AI Article Studio</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="font-size: 11px; font-weight: 600; color: #8b949e; text-transform: uppercase; letter-spacing: 0.6px; margin-bottom: 8px;">
        AI Models
    </div>
    <div style="font-size: 12px; color: #484f58; margin-bottom: 10px;">
        Select models to generate & compare
    </div>
    """, unsafe_allow_html=True)
    
    selected_models = st.multiselect(
        "AI Models",
        ["OpenRouter", "Groq", "Cohere", "Tavily", "Google Gemini"],
        default=["Groq", "OpenRouter", "Google Gemini"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    tone = st.selectbox(
        "Writing Tone",
        ["Professional", "Conversational", "Academic", "Persuasive", "Storytelling"],
        index=0
    )
    
    st.markdown("---")
    
    st.markdown("""
    <div style="background: rgba(88,166,255,0.08); border: 1px solid rgba(88,166,255,0.2); border-radius: 10px; padding: 12px 14px; margin-top: 8px;">
        <div style="font-size: 12px; color: #58a6ff; font-weight: 600; margin-bottom: 4px;">💡 Pro Tip</div>
        <div style="font-size: 12px; color: #8b949e; line-height: 1.5;">Use specific long-tail keywords for better SEO rankings and more targeted content.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #21262d;">
        <div style="font-size: 11px; color: #484f58; line-height: 1.6;">
            <strong style="color: #8b949e;">Recommended:</strong><br>
            Groq (fast & free) + Gemini
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------- MAIN HEADER ----------
st.markdown("""
<div style="margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #21262d;">
    <h1 style="font-size: 1.85rem; font-weight: 700; color: #f0f6fc; margin-bottom: 4px; letter-spacing: -0.4px;">
        Article Generator
    </h1>
    <p style="color: #8b949e; font-size: 0.92rem; margin: 0;">
        Generate · Compare · Humanize · Export — multi-model AI article studio
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- OPTION SELECTION ----------
st.markdown("---")
st.markdown('<div class="section-title">Input Method</div>', unsafe_allow_html=True)

option = st.radio(
    "Input Method",
    [
        "Auto-Generate with AI (Enter keywords & headings)",
        "Paste Your Own Article (Audit & Humanize only)"
    ],
    index=0,
    horizontal=False,
    label_visibility="collapsed"
)

st.markdown("---")

# ============================================================
# OPTION 1: AUTO-GENERATE
# ============================================================
if option == "Auto-Generate with AI (Enter keywords & headings)":
    
    with st.container():
        st.markdown('<div class="section-title">Content Details</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2.2, 1])
        
        with col1:
            title = st.text_input(
                "Article Title",
                placeholder="Enter your article title...",
                label_visibility="collapsed"
            )
        
        with col2:
            word_count = st.slider(
                "Word Count",
                min_value=300,
                max_value=2500,
                value=800,
                step=100
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="font-size: 11px; font-weight: 600; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
                Short-tail Keywords
            </div>
            <div style="font-size: 12px; color: #484f58; margin-bottom: 6px;">
                Broad, 1-2 word keywords
            </div>
            """, unsafe_allow_html=True)
            
            short_tail = st.text_area(
                "Short-tail Keywords",
                placeholder="technology, AI, writing",
                height=50,
                label_visibility="collapsed"
            )
            short_tail_list = [k.strip() for k in short_tail.split(",") if k.strip()]
            
            if short_tail_list:
                chips = "".join([f'<span class="chip chip-short">{k}</span>' for k in short_tail_list])
                st.markdown(f"<div style='margin-top: 4px;'>{chips}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="font-size: 11px; font-weight: 600; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
                Long-tail Keywords
            </div>
            <div style="font-size: 12px; color: #484f58; margin-bottom: 6px;">
                Specific, 3+ word phrases
            </div>
            """, unsafe_allow_html=True)
            
            long_tail = st.text_area(
                "Long-tail Keywords",
                placeholder="best AI writing tools for bloggers",
                height=50,
                label_visibility="collapsed"
            )
            long_tail_list = [k.strip() for k in long_tail.split(",") if k.strip()]
            
            if long_tail_list:
                chips = "".join([f'<span class="chip chip-long">{k}</span>' for k in long_tail_list])
                st.markdown(f"<div style='margin-top: 4px;'>{chips}</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("""
        <div style="font-size: 11px; font-weight: 600; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
            Headings Structure
        </div>
        <div style="font-size: 12px; color: #484f58; margin-bottom: 8px;">
            Define the main sections of your article
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            h1_headings = st.text_area(
                "H1 — Main Title",
                placeholder="Your primary heading",
                height=44,
                label_visibility="collapsed"
            )
        with col2:
            h2_headings = st.text_area(
                "H2 — Sections",
                placeholder="Section 1, Section 2, Section 3",
                height=44,
                label_visibility="collapsed"
            )
        with col3:
            h3_headings = st.text_area(
                "H3 — Sub-sections",
                placeholder="Sub-topic A, Sub-topic B",
                height=44,
                label_visibility="collapsed"
            )
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            target_audience = st.text_input(
                "Target Audience",
                placeholder="Content writers, Students, Business owners"
            )
        
        with col2:
            include_images = st.checkbox("Include Images", value=True)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([2, 1.2, 2])
        with col2:
            generate_btn = st.button("Generate Articles", width='stretch')
    
    # ---------- GENERATION LOGIC ----------
    if 'generate_btn' in locals() and generate_btn:
        if not title:
            st.error("Please enter an article title.")
        elif not short_tail_list and not long_tail_list:
            st.error("Please enter at least one keyword.")
        elif not selected_models:
            st.error("Please select at least one AI model.")
        else:
            # Warn about known problematic models
            problematic = [m for m in selected_models if m in ["DeepSeek"]]
            if problematic:
                st.warning(f"⚠️ Note: {', '.join(problematic)} may fail (known issues)")
            
            if "Groq" not in selected_models:
                st.info("💡 Tip: Groq is most reliable and free!")
            
            headings = {
                "h1": [h1_headings] if h1_headings else [],
                "h2": [h.strip() for h in h2_headings.split(",") if h.strip()] if h2_headings else [],
                "h3": [h.strip() for h in h3_headings.split(",") if h.strip()] if h3_headings else []
            }
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            model_map = {
                "OpenRouter": "openrouter",
                "Groq": "groq",
                "Cohere": "cohere",
                "DeepSeek": "deepseek",
                "Tavily": "tavily",
                "Google Gemini": "gemini"
            }
            
            model_names = [model_map.get(m) for m in selected_models if m in model_map]
            
            status_text.info(f"Generating articles from {len(model_names)} models...")
            progress_bar.progress(5)
            
            # ✅ Store each model's result separately
            generated_articles = {}
            total_models = len(model_names)

            for i, model in enumerate(model_names):
                status_text.info(f"Generating with {model.title()}... ({i+1}/{total_models})")
                progress_bar.progress(10 + (i * 10))
                
                try:
                    all_keywords = short_tail_list + long_tail_list
                    article = generate_article(
                        title=title,
                        keywords=all_keywords,
                        word_count=word_count,
                        tone=tone,
                        audience=target_audience if target_audience else None,
                        headings=headings,
                        model=model
                    )
                    
                    # ✅ Check result
                    if article and not article.startswith("❌") and not article.startswith("Error") and len(article) > 100:
                        ai_score = detect_ai(article)
                        plag_score = check_plagiarism(article)
                        generated_articles[model.title()] = {
                            "content": article,
                            "ai_score": ai_score,
                            "plagiarism": plag_score,
                            "word_count": len(article.split()),
                            "status": "success"
                        }
                        print(f"✅ {model} success! Length: {len(article.split())} words")
                    else:
                        generated_articles[model.title()] = {
                            "content": f"Failed: {article if article else 'No response'}",
                            "ai_score": 100,
                            "plagiarism": 100,
                            "word_count": 0,
                            "status": "failed"
                        }
                        print(f"❌ {model} failed: {article[:100] if article else 'No response'}")
                
                except Exception as e:
                    generated_articles[model.title()] = {
                        "content": f"Error: {str(e)[:200]}",
                        "ai_score": 100,
                        "plagiarism": 100,
                        "word_count": 0,
                        "status": "failed"
                    }
                    print(f"❌ {model} exception: {str(e)}")
            
            progress_bar.progress(60)
            
            # ---------- COMPARISON TABLE ----------
            st.markdown("---")
            st.markdown('<div class="section-title">Model Comparison</div>', unsafe_allow_html=True)

            # ✅ Check if generated_articles exists and has data
            if 'generated_articles' in locals() and generated_articles:
                best_model = None
                best_score = 999

                for name, data in generated_articles.items():
                    if data["status"] == "success" and data["ai_score"] < best_score:
                        best_score = data["ai_score"]
                        best_model = name

                # ============================================================
                # ✅ DATA FRAME TABLE (Clean & Professional)
                # ============================================================

                import pandas as pd

                # Prepare data for dataframe
                table_data = []
                for name, data in generated_articles.items():
                    if data["status"] == "success":
                        # Quality label
                        if data["ai_score"] < 25:
                            quality = "High Quality"
                        elif data["ai_score"] < 45:
                            quality = "Needs Review"
                        else:
                            quality = "AI-Generated"
                        
                        # Source type
                        is_fallback = "Generated using" in data["content"] or "generated using" in data["content"]
                        source = "Fallback" if is_fallback else "AI Model"
                        
                        # Add to table
                        table_data.append({
                            "Model": name,
                            "AI Score": f"{data['ai_score']}%",
                            "Plagiarism": f"{data['plagiarism']}%",
                            "Words": data['word_count'],
                            "Quality": quality,
                            "Source": source,
                            "_score": data['ai_score']  # For sorting/highlighting
                        })
                    else:
                        table_data.append({
                            "Model": name,
                            "AI Score": "N/A",
                            "Plagiarism": "N/A",
                            "Words": 0,
                            "Quality": "Failed",
                            "Source": "Error",
                            "_score": 999
                        })

                # Create DataFrame
                df = pd.DataFrame(table_data)

                # Drop the internal column
                df = df.drop(columns=['_score'])

                # ============================================================
                # ✅ DISPLAY DATAFRAME WITH STYLING
                # ============================================================

                # Style function
                def highlight_quality(val):
                    """
                    Color-code Quality column
                    """
                    if val == "High Quality":
                        return 'background-color: #0d3520; color: #3fb950; font-weight: bold'
                    elif val == "Needs Review":
                        return 'background-color: #3d2e00; color: #d29922; font-weight: bold'
                    elif val == "AI-Generated":
                        return 'background-color: #2d0a0a; color: #f85149; font-weight: bold'
                    elif val == "Failed":
                        return 'background-color: #2d0a0a; color: #f85149;'
                    return ''

                def highlight_best_row(row):
                    """
                    Highlight the best model (lowest AI Score)
                    """
                    if row.name == df.index[df['Quality'] == 'High Quality'].min():
                        return ['background-color: #0d3520; border-left: 3px solid #3fb950'] * len(row)
                    return [''] * len(row)

                # Apply styling
                styled_df = df.style.map(highlight_quality, subset=['Quality'])

                # Display
                st.markdown("###  Model Comparison")
                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Model": st.column_config.TextColumn("Model", width="small"),
                        "AI Score": st.column_config.TextColumn("AI Score", width="small"),
                        "Plagiarism": st.column_config.TextColumn("Plagiarism", width="small"),
                        "Words": st.column_config.NumberColumn("Words", width="small"),
                        "Quality": st.column_config.TextColumn("Quality", width="medium"),
                        "Source": st.column_config.TextColumn("Source", width="small"),
                    }
                )

                # ============================================================
                # ✅ SHOW BEST MODEL INFO
                # ============================================================

                if not df.empty:
                    best_model = df[df['Quality'] == 'High Quality']
                    if not best_model.empty:
                        best = best_model.iloc[0]
                        st.success(f" Best Model: **{best['Model']}** with AI Score {best['AI Score']}")
                    else:
                        # If no High Quality, show lowest score
                        df_sorted = df.sort_values('AI Score')
                        best = df_sorted.iloc[0]
                        st.info(f"Best available: **{best['Model']}** with AI Score {best['AI Score']}")

                # ---------- TABS WITH MODEL-SPECIFIC ARTICLES ----------
                st.markdown("---")
                st.markdown('<div class="section-title">Generated Articles From All Models</div>', unsafe_allow_html=True)

                tab_names = [name for name in generated_articles.keys()]
                tabs = st.tabs(tab_names)

                for tab, (model_name, data) in zip(tabs, generated_articles.items()):
                    with tab:
                        if data["status"] == "success":
                            col1, col2, col3 = st.columns(3)
                            col1.metric("AI Score", f"{data['ai_score']}%")
                            col2.metric("Plagiarism", f"{data['plagiarism']}%")
                            col3.metric("Words", data["word_count"])
                            
                            st.markdown(f"###  Generated by: **{model_name}**")
                            
                            st.markdown(f"""
                            <div class="article-container">
                                <h1>{title}</h1>
                                <hr>
                                <div>{data['content'].replace('\n', '<br>')}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.warning(f"❌ {model_name} failed: {data['content']}")
                
                # ---------- MERGE BEST 2 ARTICLES ----------
                st.markdown("---")
                st.markdown('<div class="section-title">Final Refined Article</div>', unsafe_allow_html=True)
                
                status_text.info("Refining and merging best articles...")
                progress_bar.progress(70)
                
                # ✅ Get all successful articles
                successful_models = []
                for name, data in generated_articles.items():
                    if data["status"] == "success" and data["content"]:
                        if data["word_count"] > 50:
                            successful_models.append((name, data))
                
                # Sort by AI score (lowest first = best)
                successful_models.sort(key=lambda x: x[1]["ai_score"])
                
                print(f" Successful articles: {len(successful_models)}")
                for name, data in successful_models:
                    print(f"  - {name}: {data['word_count']} words, AI Score: {data['ai_score']}%")
                
                if len(successful_models) >= 2:
                    name1, data1 = successful_models[0]
                    name2, data2 = successful_models[1]
                    
                    content1 = data1["content"]
                    content2 = data2["content"]
                    
                    paras1 = [p for p in content1.split('\n') if p.strip()]
                    paras2 = [p for p in content2.split('\n') if p.strip()]
                    
                    merged_paras = []
                    
                    intro_count = min(3, len(paras1))
                    merged_paras.extend(paras1[:intro_count])
                    
                    if len(paras2) > 4:
                        body_start = len(paras2) // 4
                        body_end = len(paras2) - len(paras2) // 4
                        merged_paras.extend(paras2[body_start:body_end])
                    else:
                        merged_paras.extend(paras2)
                    
                    if len(paras1) > 2:
                        merged_paras.extend(paras1[-2:])
                    
                    if len(merged_paras) < 4:
                        merged_paras = paras1 + paras2
                    
                    final_article = '\n\n'.join(merged_paras)
                    final_ai_score = (data1["ai_score"] + data2["ai_score"]) // 2
                    final_source = f"Merged from {name1} + {name2}"
                    
                    print(f"✅ Merged {name1} + {name2}: {len(final_article.split())} words")
                    
                elif len(successful_models) == 1:
                    name, data = successful_models[0]
                    final_article = data["content"]
                    final_ai_score = data["ai_score"]
                    final_source = f"Best article from {name}"
                    print(f"✅ Using single article from {name}: {len(final_article.split())} words")
                    
                else:
                    print("⚠️ No successful articles, using fallback...")
                    fallback_content = None
                    for name, data in generated_articles.items():
                        if data["content"] and len(data["content"]) > 50:
                            fallback_content = data["content"]
                            fallback_name = name
                            break
                    
                    if fallback_content:
                        final_article = fallback_content
                        final_ai_score = 50
                        final_source = f"Fallback: {fallback_name}"
                    else:
                        from utils.ai_writer import auto_search_and_generate
                        final_article = auto_search_and_generate(
                            f"Write a detailed article about {title}",
                            word_count
                        )
                        final_ai_score = 50
                        final_source = "Auto-Search Fallback"
                
                # ✅ Ensure final_article is not empty
                if not final_article or len(final_article.split()) < 30:
                    print("⚠️ Final article too short, generating fallback...")
                    from utils.ai_writer import auto_search_and_generate
                    final_article = auto_search_and_generate(
                        f"Write a detailed article about {title}",
                        word_count
                    )
                    final_ai_score = 50
                    final_source = "Auto-Search Fallback"
                
                progress_bar.progress(80)
                
                # ---------- HUMANIZE ----------
                status_text.info("Humanizing content...")
                time.sleep(1)
                
                if final_ai_score > 30:
                    final_article = humanize_text(final_article)
                    final_ai_score = detect_ai(final_article)
                
                # Clean AI signatures
                final_article = re.sub(r'According to.*?\.', '', final_article, flags=re.IGNORECASE)
                final_article = re.sub(r'\(Source:.*?\)', '', final_article, flags=re.IGNORECASE)
                final_article = re.sub(r'Note:.*?\.', '', final_article, flags=re.IGNORECASE)
                
                progress_bar.progress(85)
                
                # ---------- IMAGES ----------
                images = []
                if include_images:
                    try:
                        images = fetch_images(title, per_page=4)
                        if not images:
                            print("⚠️ Image fetch failed, using fallback images...")
                            from utils.images import get_fallback_images
                            images = get_fallback_images()
                        else:
                            print(f"✅ Fetched {len(images)} images")
                    except Exception as e:
                        print(f"⚠️ Image fetch error: {e}")
                        from utils.images import get_fallback_images
                        images = get_fallback_images()

                progress_bar.progress(100)
                status_text.success("All articles generated successfully!")
                time.sleep(0.5)
                status_text.empty()
                
                # ---------- DISPLAY FINAL ARTICLE ----------
                col1, col2, col3, col4 = st.columns(4)
                plag_final = check_plagiarism(final_article)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{final_ai_score}%</div>
                        <div class="metric-label">AI Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{plag_final}%</div>
                        <div class="metric-label">Plagiarism</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{len(final_article.split())}</div>
                        <div class="metric-label">Word Count</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    quality = "Pass" if final_ai_score < 30 and plag_final == 0 else "Review"
                    color = "#3fb950" if final_ai_score < 30 else "#d29922"
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value" style="color:{color} !important;">{quality}</div>
                        <div class="metric-label">Quality</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.caption(f"Source: {final_source}")
                
                st.markdown(f"""
                <div class="article-container">
                    <h1>{title}</h1>
                    <hr>
                    <div>{final_article.replace('\n', '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # ---------- IMAGES ----------
                if images:
                    st.markdown("---")
                    st.markdown('<div class="section-title">Images</div>', unsafe_allow_html=True)
                    
                    cols = st.columns(4)
                    for idx, img in enumerate(images[:4]):
                        with cols[idx]:
                            st.image(img, width='stretch')
                            st.caption(f"Image {idx+1}")
                
                # ---------- EXPORT ----------
                st.markdown("---")
                st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if images:
                        if isinstance(images[0], str):
                            export_images = images
                        else:
                            export_images = [img.getvalue() for img in images if hasattr(img, 'getvalue')]
                    else:
                        export_images = []
                    
                    docx_bytes = export_to_docx(title, final_article, export_images if export_images else [])
                    st.download_button(
                        label="📥 Download DOCX",
                        data=docx_bytes,
                        file_name=f"{title[:40].replace(' ', '_')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        width='stretch'
                    )
                
                with col2:
                    if st.button("🔄 Regenerate", width='stretch'):
                        st.rerun()
            
            else:
                st.info("👈 Select models, fill in the details, and click 'Generate Articles' to see comparison here")

# ============================================================
# OPTION 2: MANUAL PASTE
# ============================================================
else:
    with st.container():
        st.markdown("""
        <div style="font-size: 11px; font-weight: 600; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
            Paste Your Article
        </div>
        <div style="font-size: 12px; color: #484f58; margin-bottom: 8px;">
            Paste your existing article below. The system will audit, humanize, and check plagiarism.
        </div>
        """, unsafe_allow_html=True)
        
        manual_article = st.text_area(
            "Article Content",
            placeholder="Paste your article content here...",
            height=200,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            manual_title = st.text_input(
                "Article Title",
                placeholder="Enter the title of your article"
            )
        
        with col2:
            st.markdown("""
            <div style="font-size: 11px; font-weight: 600; color: #8b949e; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                Images
            </div>
            """, unsafe_allow_html=True)
            
            manual_image_option = st.radio(
                "Image Option",
                [
                    "Auto-add",
                    "Upload own",
                    "None"
                ],
                index=0,
                horizontal=True,
                label_visibility="collapsed"
            )
            
            manual_user_images = []
            
            if manual_image_option == "Upload own":
                st.markdown("""
                <div class="image-upload-container">
                    <div style="color: #8b949e; font-size: 0.9rem;">Upload up to 4 images (JPG, PNG)</div>
                </div>
                """, unsafe_allow_html=True)
                
                uploaded_files = st.file_uploader(
                    "Upload Images",
                    type=["jpg", "jpeg", "png", "webp"],
                    accept_multiple_files=True,
                    label_visibility="collapsed"
                )
                if uploaded_files:
                    manual_user_images = uploaded_files[:4]
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([2, 1.2, 2])
        with col2:
            audit_btn = st.button("Audit & Humanize", width='stretch')
    
    # ---------- AUDIT LOGIC ----------
    if 'audit_btn' in locals() and audit_btn:
        if not manual_article:
            st.error("Please paste your article content.")
        else:
            article = manual_article
            title = manual_title if manual_title else "Untitled Article"
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.info("Running AI detection...")
            progress_bar.progress(25)
            time.sleep(0.8)
            
            ai_score = detect_ai(article)
            progress_bar.progress(45)
            
            status_text.info("Checking plagiarism...")
            plagiarism_score = check_plagiarism(article)
            progress_bar.progress(60)
            
            if ai_score > 30:
                status_text.info("Humanizing content...")
                article = humanize_text(article)
                time.sleep(0.8)
                ai_score = detect_ai(article)
            
            progress_bar.progress(80)
            
            # ---------- IMAGES ----------
            images = []
            
            if manual_image_option == "Auto-add":
                status_text.info("Fetching images...")
                image_keyword = title.split()[0] if title else "article"
                try:
                    images = fetch_images(image_keyword, per_page=4)
                    if not images:
                        images = get_fallback_images()
                except:
                    images = get_fallback_images()
            elif manual_image_option == "Upload own":
                if manual_user_images:
                    status_text.info("Processing uploaded images...")
                    images = manual_user_images
            
            progress_bar.progress(100)
            status_text.success("Audit complete!")
            time.sleep(0.3)
            status_text.empty()
            
            # ---------- DISPLAY ----------
            st.markdown("---")
            st.markdown('<div class="section-title">Audited Article</div>', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{ai_score}%</div>
                    <div class="metric-label">AI Score</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{plagiarism_score}%</div>
                    <div class="metric-label">Plagiarism</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(article.split())}</div>
                    <div class="metric-label">Word Count</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                quality = "Pass" if ai_score < 30 and plagiarism_score == 0 else "Review"
                color = "#3fb950" if ai_score < 30 else "#d29922"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value" style="color:{color} !important;">{quality}</div>
                    <div class="metric-label">Quality</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            st.markdown(f"""
            <div class="article-container">
                <h1>{title}</h1>
                <hr>
                <div>{article.replace('\n', '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if images:
                st.markdown("---")
                st.markdown('<div class="section-title">Images</div>', unsafe_allow_html=True)
                
                if isinstance(images[0], str):
                    cols = st.columns(4)
                    for idx, img_url in enumerate(images[:4]):
                        with cols[idx]:
                            st.image(img_url, width='stretch')
                else:
                    cols = st.columns(4)
                    for idx, img_file in enumerate(images[:4]):
                        with cols[idx]:
                            try:
                                img = Image.open(img_file)
                                st.image(img, width='stretch')
                                st.caption(f"Uploaded {idx+1}")
                            except:
                                pass
            
            # ---------- EXPORT ----------
            st.markdown("---")
            st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if images:
                    if isinstance(images[0], str):
                        export_images = images
                    else:
                        export_images = [img.getvalue() for img in images if hasattr(img, 'getvalue')]
                else:
                    export_images = []
                
                docx_bytes = export_to_docx(title, article, export_images if export_images else [])
                st.download_button(
                    label="📥 Download DOCX",
                    data=docx_bytes,
                    file_name=f"{title[:40].replace(' ', '_')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    width='stretch'
                )
            
            with col2:
                if st.button("🔄 Start Over", width='stretch'):
                    st.rerun() 

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    ArticleForge v2.0 &middot; Built with Streamlit &middot; Free &amp; Open Source
</div>
""", unsafe_allow_html=True)