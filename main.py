import streamlit as st
from pathlib import Path
import json
import yaml
import pandas as pd
from datetime import datetime
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama
import os

# Configure page
st.set_page_config(
    page_title="AI Web Scraper",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    css_file = Path(__file__).parent / "styles/style.css"
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply styling
load_css()

# Sidebar
with st.sidebar:
    st.markdown("""
        # 📚 Tips & Tricks
        
        ### 🎯 Effective Web Scraping
        1. **Be Specific**: Target precise sections of websites for better results
        2. **Check Content**: Review the scraped content before analysis
        3. **Batch Processing**: Larger pages are automatically split into manageable chunks
        4. **Rate Limiting**: Avoid rapid repeated scraping of the same site
        
        ### 🤖 AI Analysis Tips
        1. **Clear Queries**: Write specific, focused questions
        2. **Context Matters**: Include relevant context in your queries
        3. **Verify Results**: Cross-check important information
        4. **Multiple Passes**: Try different query formulations
        
        ### 💡 Best Practices
        - Start with smaller pages to test
        - Use descriptive queries
        - Download results for important findings
        - Review all batch results
        
        ---
        
        ### ⚠️ Disclaimer
        
        **AI Model Performance**
        - Results may vary depending on the AI model used
        - Accuracy is not guaranteed
        - Always verify critical information
        - Different models may interpret queries differently
        
        **Web Scraping Notice**
        - Respect websites' robots.txt
        - Some sites may block automated access
        - Content may change between scrapes
        
        ---
        
        ### 🔧 Current Settings
        - Model: {os.getenv('LLM_TYPE', 'ollama')} ({os.getenv('LLM_MODEL', 'llama3.1')})
        - Max Chunk Size: 6000 chars
        - Format: Plain Text
    """)

# Main container
with st.container():
    # Header with centered logo
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0;'>
            <h1 class='stTitle'>🌐 AI Web Scraper</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # URL input with styling
    url = st.text_input("Enter Website URL", key="url_input")

    # Step 1: Scrape the Website
    if st.button("🔍 Scrape Website", key="scrape_button"):
        if url:
            with st.spinner():
                st.write("Connecting to Scraping Browser...")
                dom_content = scrape_website(url)
                
                st.write("Processing content...")
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)
                
                st.session_state.dom_content = cleaned_content
                st.success("Website scraped successfully!")

    # Create fixed panels if content exists
    if "dom_content" in st.session_state:
        # Create two equal columns
        left_panel, right_panel = st.columns(2)
        
        # Left Panel - DOM Content
        with left_panel:
            st.write("### 📄 Scraped Content")
            st.text_area(
                label="DOM Content",
                value=st.session_state.dom_content,
                height=600,
                key="dom_viewer",
                label_visibility="collapsed"
            )
        
        # Right Panel - Analysis
        with right_panel:
            st.write("### 🤖 Content Analysis")
            parse_description = st.text_area(
                "What would you like to know about this website?",
                key="query_input",
                height=100
            )

            if st.button("🔍 Analyze Content", key="parse_button"):
                if parse_description:
                    with st.spinner("Analyzing content..."):
                        dom_chunks = split_dom_content(st.session_state.dom_content)
                        parsed_results = []
                        
                        for i, chunk in enumerate(dom_chunks, 1):
                            with st.spinner(f"Processing batch {i} of {len(dom_chunks)}..."):
                                result = parse_with_ollama([chunk], parse_description)
                                parsed_results.append(result)
                        
                        # Store results in session state
                        st.session_state.parsed_results = parsed_results
                        st.session_state.current_query = parse_description
                        st.session_state.analysis_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Display results if they exist in session state
    if 'parsed_results' in st.session_state:
        st.write("### 📊 Analysis Results")
        tabs = st.tabs([f"Batch {i+1}" for i in range(len(st.session_state.parsed_results))])
        
        for i, (tab, result) in enumerate(zip(tabs, st.session_state.parsed_results)):
            with tab:
                st.write(result)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        "📝 Download TXT",
                        result,
                        f"batch_{i+1}_result_{st.session_state.analysis_timestamp}.txt",
                        "text/plain",
                        key=f"download_txt_batch_{i+1}"
                    )
                
                with col2:
                    batch_data = {
                        'batch': i+1,
                        'query': st.session_state.current_query,
                        'result': result
                    }
                    st.download_button(
                        "📊 Download JSON",
                        json.dumps(batch_data, indent=2),
                        f"batch_{i+1}_result_{st.session_state.analysis_timestamp}.json",
                        "application/json",
                        key=f"download_json_batch_{i+1}"
                    )

# Footer
st.write("---")
st.write(
    """
    <div style='text-align: center; color: #7f8c8d;'>
        Built with ❤️ using Streamlit, Ollama, and BrightData
    </div>
    """, 
    unsafe_allow_html=True
)
