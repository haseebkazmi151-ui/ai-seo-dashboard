import streamlit as st
import requests
from bs4 import BeautifulSoup
from google import genai
import pandas as pd

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI SEO Pro Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# PRESENTATION-STYLE GLOWING DARK UI (CSS)
# ==========================================
st.markdown("""
    <!-- Load Google Font & FontAwesome Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <style>
    /* Global Background & Font Overrides */
    .stApp, html, body, [data-testid="stHeader"] {
        font-family: 'Urbanist', sans-serif !important;
        background-color: #020617 !important;
        color: #94a3b8 !important;
    }
    
    /* Sidebar Overrides to match deep charcoal dark theme */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid #1e293b !important;
    }
    
    /* Titles styling with slide-style Lime Left Border */
    .dashboard-title-box {
        border-left: 6px solid #84cc16;
        padding-left: 20px;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .dashboard-title-box h1 {
        color: #f8fafc !important;
        font-size: 52px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        line-height: 1.1 !important;
    }
    .dashboard-title-box span {
        color: #84cc16 !important;
    }
    
    /* Custom CSS Tiles representing the core layout */
    .presentation-tile {
        background-color: #0f172a;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #1e293b;
        margin-bottom: 25px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .presentation-tile:hover {
        transform: translateY(-3px);
        border-color: #84cc16;
    }
    .presentation-tile h3 {
        color: #84cc16 !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        margin-top: 0px;
        margin-bottom: 12px;
    }
    .presentation-tile p {
        color: #94a3b8 !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    .tile-icon {
        font-size: 36px;
        color: #84cc16;
        margin-bottom: 18px;
    }
    
    /* Neon Metric Card styling overrides */
    div[data-testid="stMetric"] {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 16px !important;
        padding: 24px 20px !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #84cc16;
        box-shadow: 0 0 15px rgba(132, 204, 22, 0.15);
    }
    [data-testid="stMetricValue"] {
        color: #84cc16 !important;
        font-size: 42px !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #f8fafc !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    
    /* Elegant Lime Green Button Override */
    div.stButton > button {
        background-color: #84cc16 !important;
        color: #020617 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(132, 204, 22, 0.2) !important;
    }
    div.stButton > button:hover {
        background-color: #a3e635 !important;
        box-shadow: 0 0 20px rgba(132, 204, 22, 0.45) !important;
        transform: translateY(-2px);
    }
    
    /* Input Fields Styling to look premium */
    .stTextInput input {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 15px !important;
    }
    .stTextInput input:focus {
        border-color: #84cc16 !important;
        box-shadow: 0 0 0 2px rgba(132, 204, 22, 0.25) !important;
    }
    
    /* Sidebar Headers */
    .sidebar .sidebar-content h2, .sidebar .sidebar-content h1 {
        color: #f8fafc !important;
    }
    
    /* Styled Markdown Reports */
    .ai-report-container {
        background-color: #0f172a;
        border-radius: 20px;
        padding: 40px;
        border: 1px solid #1e293b;
        color: #e2e8f0;
        margin-top: 25px;
    }
    .ai-report-container h1, .ai-report-container h2 {
        color: #84cc16 !important;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 10px;
    }
    
    /* Bullet points styling */
    .presentation-bullets {
        list-style: none;
        padding-left: 0;
    }
    .presentation-bullets li {
        position: relative;
        padding-left: 35px;
        margin-bottom: 18px;
        font-size: 18px;
        color: #94a3b8;
    }
    .presentation-bullets li::before {
        content: "\\f058";
        font-family: 'Font Awesome 6 Free';
        font-weight: 900;
        position: absolute;
        left: 0;
        color: #84cc16;
        font-size: 20px;
    }
    
    /* HTML Table Overrides */
    table {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        width: 100% !important;
    }
    th {
        background-color: #1e293b !important;
        color: #84cc16 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        padding: 15px !important;
    }
    td {
        color: #f8fafc !important;
        padding: 15px !important;
        font-size: 16px !important;
        border-bottom: 1px solid #1e293b !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# CORE SEO LOGIC (MODULAR)
# ==========================================

def audit_website(url):
    try:
        if not url.startswith('http'):
            url = 'https://' + url
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200: 
            return None, f"Status Code {response.status_code}"
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('title').text.strip() if soup.find('title') else "MISSING"
        desc = soup.find('meta', attrs={'name': 'description'})
        meta_desc = desc.get('content', '').strip() if desc else "MISSING"
        h1 = soup.find('h1').text.strip() if soup.find('h1') else "MISSING"
        links = len(soup.find_all('a', href=True))
        
        return {"url": url, "title": title, "meta_description": meta_desc, "h1": h1, "links": links}, None
    except Exception as e: 
        return None, str(e)

def analyze_competitors(keyword):
    search_url = f"https://www.google.com/search?q={keyword.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        competitors = []
        for g in soup.find_all('div', class_='g')[:3]:  
            link_tag = g.find('a', href=True)
            title_tag = g.find('h3')
            if link_tag and title_tag:
                competitors.append({"Competitor": title_tag.text, "URL": link_tag['href']})
        return competitors
    except: 
        return []

def get_ai_strategy(api_key, audit_data, competitors, keyword):
    try:
        client = genai.Client(api_key=api_key)
        
        my_site_title = audit_data['title'] if audit_data else 'N/A'
        my_site_meta = audit_data['meta_description'] if audit_data else 'N/A'
        my_site_h1 = audit_data['h1'] if audit_data else 'N/A'

        prompt = f"""
        Role: Senior SEO Strategist. Target Keyword: {keyword}
        
        1. AUDIT REPORT for My Site:
        - Title: {my_site_title} | Meta: {my_site_meta} | H1: {my_site_h1}
        
        2. TOP COMPETITORS:
        {competitors}
        
        Generate a professional SEO plan in clear Markdown formatting:
        - FIX: Optimized Title & Meta Description.
        - ANALYSIS: What are competitors doing better?
        - CONTENT: Full SEO Content Outline (H1, H2s) & LSI Keywords.
        """
        response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
        return response.text
    except Exception as e: 
        return f"AI Error: {str(e)}"

# ==========================================
# STREAMLIT UI LAYOUT
# ==========================================

# Styled Title Header (Matches Presentation Title Box)
st.markdown("""
    <div class="dashboard-title-box">
        <h1>AI SEO <span>Pro</span> Dashboard</h1>
        <p style="font-size: 18px; color: #94a3b8; margin-top: 5px;">Transforming raw website data into dominant search rankings with Gemini 2.5 Flash automation.</p>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#f8fafc; font-size: 24px;'>⚙️ Configuration</h2>", unsafe_allow_html=True)
    api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste AI Studio Key")
    st.markdown("<hr style='border-color: #1e293b;'>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='color:#f8fafc; font-size: 18px;'>📍 Target Settings</h3>", unsafe_allow_html=True)
    target_url = st.text_input("Your Website URL", placeholder="example.com")
    keyword = st.text_input("Target Focus Keyword", placeholder="e.g., best running shoes")
    
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("Run SEO Engine")

# --- MAIN PAGE ROUTING ---
if analyze_btn:
    if not api_key or not target_url or not keyword:
        st.error("Please fill in all fields in the sidebar!")
    else:
        with st.status("🔍 Processing SEO Data...", expanded=True) as status:
            st.write("Auditing your website...")
            audit_data, err = audit_website(target_url)
            
            st.write("Analyzing Google SERP...")
            competitors = analyze_competitors(keyword)
            
            st.write("Consulting Gemini AI (gemini-2.5-flash)...")
            report = get_ai_strategy(api_key, audit_data, competitors, keyword)
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        # --- Real-Time Performance Showcase ---
        if audit_data:
            st.markdown("<h2 style='color:#f8fafc; font-size: 28px; border-left:4px solid #84cc16; padding-left:12px; margin-bottom: 20px;'>📊 Site Audit Summary</h2>", unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Title Length", f"{len(audit_data['title'])} chars")
            c2.metric("Meta Desc Status", "Found" if audit_data['meta_description'] != "MISSING" else "Missing")
            c3.metric("H1 Header Status", "Present" if audit_data['h1'] != "MISSING" else "Missing")
            c4.metric("Internal Links Density", f"{audit_data['links']} links")
        elif err:
            st.warning(f"⚠️ Could not fully audit site ({err}), but generating strategy anyway.")

        # --- Competitors Showcase ---
        if competitors:
            st.markdown("<br><h2 style='color:#f8fafc; font-size: 28px; border-left:4px solid #84cc16; padding-left:12px; margin-bottom: 20px;'>🕵️ Competitor Analysis</h2>", unsafe_allow_html=True)
            st.table(pd.DataFrame(competitors))

        # --- AI Strategy Showcase ---
        st.markdown("<br><h2 style='color:#f8fafc; font-size: 28px; border-left:4px solid #84cc16; padding-left:12px; margin-bottom: 10px;'>🤖 AI Strategic Report</h2>", unsafe_allow_html=True)
        st.markdown(f'<div class="ai-report-container">{report}</div>', unsafe_allow_html=True)
        
        # Download Report Styled Segment
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button("Download Report (.txt)", report, file_name="seo_report.txt")

else:
    # --- Landing Page / Mockup Presentation View ---
    st.info("👈 Enter your details in the sidebar and click 'Run SEO Engine' to start your analysis.")
    
    st.markdown("<br><h2 style='color:#f8fafc; font-size: 32px; border-left:4px solid #84cc16; padding-left:15px; margin-bottom: 30px;'>Core AI Modules Overview</h2>", unsafe_allow_html=True)
    
    # Grid of Three Tiles to match presentation style
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="presentation-tile">
                <div class="tile-icon"><i class="fa-solid fa-magnifying-glass-chart"></i></div>
                <h3>Audit Bot</h3>
                <p>Checks technical on-page SEO automatically including: title tags, meta descriptions, H1 headers, and links density.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="presentation-tile">
                <div class="tile-icon"><i class="fa-solid fa-users-viewfinder"></i></div>
                <h3>Spy Engine</h3>
                <p>Identifies top-ranking active competitors from Google SERP and extracts their structured pattern data.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="presentation-tile">
                <div class="tile-icon"><i class="fa-solid fa-brain"></i></div>
                <h3>Strategist</h3>
                <p>Generates keyword-optimized, structured content outlines designed specifically to outrank top players.</p>
            </div>
        """, unsafe_allow_html=True)

    # Smart Features List (Matches Slides "Backend Engine")
    st.markdown("<br><h2 style='color:#f8fafc; font-size: 28px; border-left:4px solid #84cc16; padding-left:15px; margin-bottom: 20px;'>How It Works</h2>", unsafe_allow_html=True)
    st.markdown("""
        <ul class="presentation-bullets">
            <li><strong>Smart Crawler Phase:</strong> Extracts meta-data structure from your on-page source directly.</li>
            <li><strong>SERP Analysis:</strong> Gathers real-time search engine result data for contextual comparison.</li>
            <li><strong>Gemini 2.5 Strategy Synthesis:</strong> Leverages advanced flash model processing to create actionable plans in milliseconds.</li>
        </ul>
    """, unsafe_allow_html=True)