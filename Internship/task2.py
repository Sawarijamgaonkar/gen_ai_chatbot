# from nltk.tokenize import sent_tokenize, word_tokenize
# from collections import Counter
# from nltk.corpus import stopwords

# def generate_summary(text, n):
#     sentences = sent_tokenize(text)
#     stop_words = set(stopwords.words('english'))
#     words = [word.lower() for word in word_tokenize(text) if word.lower() not in stop_words and word.isalnum()]
#     word_freq = Counter(words)
    
#     sentence_scores = {}
#     for sentence in sentences:
#         sentence_words = [word.lower() for word in word_tokenize(sentence) if word.lower() not in stop_words and word.isalnum()]
#         sentence_score = sum([word_freq[word] for word in sentence_words])
#         if len(sentence_words) < 20:
#             sentence_scores[sentence] = sentence_score
    
#     summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n]
#     return ' '.join(summary_sentences)


import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
from heapq import nlargest
from collections import defaultdict

# Download the punkt tokenizer and stopwords
nltk.download('punkt_tab')
nltk.download('stopwords')

def summarize(text, ratio=0.2):
    """
    Extractive summarization using NLTK
    """
    # Tokenize sentences and words
    sents = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    # Remove stopwords and punctuation
    stop_words = set(stopwords.words('english') + list(punctuation))
    words = [word for word in words if word not in stop_words and word.isalnum()]
    
    # Calculate word frequencies
    freq = defaultdict(int)
    for word in words:
        freq[word] += 1
    
    # Normalize frequencies
    max_freq = max(freq.values()) if freq else 1
    for word in freq:
        freq[word] /= max_freq
    
    # Score sentences
    sent_scores = defaultdict(int)
    for i, sent in enumerate(sents):
        for word in word_tokenize(sent.lower()):
            if word in freq:
                sent_scores[i] += freq[word]
    
    # Select top sentences
    select_len = max(1, int(len(sents) * ratio))
    top_sents = nlargest(select_len, sent_scores, key=sent_scores.get)
    summary = ' '.join([sents[i].capitalize() for i in sorted(top_sents)])
    
    return summary

# Streamlit UI
def main():
    st.set_page_config(
        page_title="Text Summarizer",
        page_icon="📝",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        .css-18e3th9 {padding: 2rem 3rem 5rem;}
        .stButton button {
            background: linear-gradient(45deg, #4CAF50, #8BC34A);
            color: white;
            border: none;
            font-weight: bold;
            border-radius: 8px;
            padding: 12px 24px;
            transition: all 0.3s;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .stTextArea textarea {
            min-height: 250px;
            border-radius: 8px;
        }
        .css-1q8dd3e {
            border-radius: 8px;
        }
        .summary-box {
            background-color: #f5f7fa;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("🔍 Summarizer")
        st.markdown("""
        **How it works:**
        - Analyzes text with natural language processing
        - Scores sentences by importance
        - Extracts key sentences to create a summary
        """)
        
        ratio = st.slider(
            "Summary length (%)",
            min_value=10, max_value=50, value=20,
            help="Percentage of original text to include in summary"
        )
        
        st.markdown("---")
        st.markdown("**Tips for best results:**")
        st.markdown("""
        - Input at least 5-6 sentences
        - Clear, well-structured text works best
        - Adjust length as needed
        """)

    # Main content
    st.title("📄 Extractive Text Summarizer")
    st.markdown("Quickly condense long documents into key points")
    
    # Input section
    text = st.text_area(
        "Paste your text below:",
        height=300,
        placeholder="Enter text to summarize (minimum 5 sentences)...",
        help="The more text you provide, the better the results will be."
    )
    
    if st.button("Generate Summary 🚀"):
        if not text or len(sent_tokenize(text)) < 3:
            st.warning("Please enter at least 3 sentences for summarization")
        else:
            with st.spinner("Analyzing content..."):
                result = summarize(text, ratio/100)
                
                st.success("Summary generated!")
                with st.expander("⏬ View Summary", expanded=True):
                    st.markdown(f'<div class="summary-box">{result}</div>', 
                               unsafe_allow_html=True)
                    
                    # Show stats
                    orig_len = len(sent_tokenize(text))
                    summ_len = len(sent_tokenize(result))
                    st.caption(f"Reduced from {orig_len} to {summ_len} sentences ({ratio}%)")
                
                # Download button
                st.download_button(
                    "📥 Download Summary",
                    data=result,
                    file_name="summary.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
