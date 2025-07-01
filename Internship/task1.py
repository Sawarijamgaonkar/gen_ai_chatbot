
# from dotenv import load_dotenv
# import streamlit as st
# import os
# from PIL import Image
# import google.generativeai as genai
# from collections import Counter
# from streamlit.components.v1 import html


# load_dotenv()

# os.environ["GOOGLE_API_KEY"] = "AIzaSyAWfi-RW03Sq6wUcNhpvuBJ7OO5rcluC5I"
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


# if 'query_count' not in st.session_state:
#     st.session_state.query_count = 0
# if 'search_history' not in st.session_state:
#     st.session_state.search_history = []
# if 'topics' not in st.session_state:
#     st.session_state.topics = []
# if 'ratings' not in st.session_state:
#     st.session_state.ratings = []

# def get_gemini_response(input, image=None):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     if input != "":
#         response = model.generate_content([input, image] if image else [input])
#     else:
#         response = model.generate_content(image)
#     return response.text


# st.set_page_config(page_title="Smart Chatbot Interface", layout="wide")
# st.title("Smart Chatbot Interface")
# st.markdown("### Get insights from your images or ask questions directly!")


# col1, col2 = st.columns([1, 3])
# with col1:
#     st.header("Analytics Dashboard")
#     st.write(f"**Total Queries:** {st.session_state.query_count}")
#     if st.session_state.topics:
#         most_common_topic = Counter(st.session_state.topics).most_common(1)[0]
#         st.write(f"**Most Common Topic:** {most_common_topic[0]} (Count: {most_common_topic[1]})")
#     else:
#         st.write("No topics recorded yet.")

#     if st.session_state.ratings:
#         average_rating = sum(st.session_state.ratings) / len(st.session_state.ratings)
#         st.write(f"**Average User Satisfaction Rating:** {average_rating:.2f}")
#     else:
#         st.write("No ratings recorded yet.")

#     st.markdown("### Search History")
#     if st.session_state.search_history:
#         for query in st.session_state.search_history:
#             st.write(f"- {query}")
#     else:
#         st.write("No search history available.")

# with col2:
#     input_text = st.text_input("Enter your search prompt:")
#     uploaded_image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])
#     image = None
#     if uploaded_image:
#         image = Image.open(uploaded_image)
#         st.image(image, caption="Uploaded Image", use_column_width=True)

#     if st.button("Search Now"):
#         if input_text:
#             st.session_state.query_count += 1
#             st.session_state.topics.append(input_text)  # Track the topic
#             st.session_state.search_history.append(input_text)  # Track search history
#             response = get_gemini_response(input_text, image)
#             st.subheader("The Response is")
#             st.write(response)

#             # User satisfaction rating
#             st.markdown("### Rate Your Satisfaction")
#             rating = st.slider("How satisfied are you with the response? (1-5)", 1, 5, 3)
#             st.session_state.ratings.append(rating)
#         else:
#             st.warning("Please enter a prompt to get a response.")


# from dotenv import load_dotenv
# import streamlit as st
# import os
# from PIL import Image
# import google.generativeai as genai
# from collections import Counter
# import time

# # Set page configuration at the very top
# st.set_page_config(page_title="Nexus AI", layout="wide", page_icon="🤖")

# load_dotenv()

# # Configure API
# os.environ["GOOGLE_API_KEY"] = "AIzaSyAWfi-RW03Sq6wUcNhpvuBJ7OO5rcluC5I"
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# # Initialize session state
# if 'query_count' not in st.session_state:
#     st.session_state.query_count = 0
# if 'search_history' not in st.session_state:
#     st.session_state.search_history = []
# if 'topics' not in st.session_state:
#     st.session_state.topics = []
# if 'ratings' not in st.session_state:
#     st.session_state.ratings = []
# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# def get_gemini_response(input, image=None):
#     model = genai.GenerativeModel("gemini-1.5-flash")
#     if input:
#         response = model.generate_content([input, image] if image else [input])
#     else:
#         response = model.generate_content(image)
#     return response.text

# # Custom CSS for sleek design
# st.markdown("""
# <style>
#     /* Main container */
#     .stApp {
#         background-color: #f8f9fa;
#     }
    
#     /* Chat container */
#     .chat-container {
#         background-color: white;
#         border-radius: 12px;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.05);
#         padding: 1.5rem;
#         height: 70vh;
#         overflow-y: auto;
#     }
    
#     /* User message */
#     .user-message {
#         background-color: #007bff;
#         color: white;
#         border-radius: 18px 18px 0 18px;
#         padding: 10px 16px;
#         margin: 8px 0;
#         max-width: 70%;
#         float: right;
#         clear: both;
#     }
    
#     /* Bot message */
#     .bot-message {
#         background-color: #f1f3f5;
#         color: #212529;
#         border-radius: 18px 18px 18px 0;
#         padding: 10px 16px;
#         margin: 8px 0;
#         max-width: 70%;
#         float: left;
#         clear: both;
#     }
    
#     /* Input area */
#     .stTextInput>div>div>input {
#         border-radius: 20px !important;
#         padding: 10px 15px !important;
#     }
    
#     /* Button */
#     .stButton>button {
#         border-radius: 20px !important;
#         background-color: #007bff !important;
#         color: white !important;
#         border: none !important;
#         padding: 8px 20px !important;
#     }
    
#     /* Analytics card */
#     .analytics-card {
#         background-color: white;
#         border-radius: 12px;
#         box-shadow: 0 4px 12px rgba(0,0,0,0.05);
#         padding: 1rem;
#         margin-bottom: 1rem;
#     }
    
#     /* Typing animation */
#     @keyframes typing {
#         from { width: 0 }
#         to { width: 100% }
#     }
    
#     .typing-indicator {
#         display: inline-block;
#         overflow: hidden;
#         white-space: nowrap;
#         animation: typing 1.5s steps(40, end);
#     }
# </style>
# """, unsafe_allow_html=True)

# # Main layout
# col1, col2 = st.columns([1, 2])

# # Analytics Dashboard
# with col1:
#     st.markdown("""
#     <div style='background-color: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05);'>
#         <h2 style='color: #007bff; border-bottom: 1px solid #eee; padding-bottom: 0.5rem;'>📊 Analytics</h2>
#         <div class='analytics-card'>
#             <h4>Total Queries</h4>
#             <h2 style='color: #007bff;'>{}</h2>
#         </div>
#     """.format(st.session_state.query_count), unsafe_allow_html=True)
    
#     if st.session_state.topics:
#         most_common_topic = Counter(st.session_state.topics).most_common(1)[0]
#         st.markdown(f"""
#         <div class='analytics-card'>
#             <h4>Most Common Topic</h4>
#             <p style='font-size: 1.1rem;'>{most_common_topic[0]}</p>
#             <small>Count: {most_common_topic[1]}</small>
#         </div>
#         """, unsafe_allow_html=True)
    
#     if st.session_state.ratings:
#         average_rating = sum(st.session_state.ratings) / len(st.session_state.ratings)
#         st.markdown(f"""
#         <div class='analytics-card'>
#             <h4>User Satisfaction</h4>
#             <div style='display: flex; align-items: center;'>
#                 <span style='font-size: 1.5rem; color: #ffc107;'>{"★" * int(round(average_rating))}</span>
#                 <span style='margin-left: 0.5rem;'>{average_rating:.1f}/5</span>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("""
#         <div class='analytics-card'>
#             <h4>📝 Recent Queries</h4>
#     """, unsafe_allow_html=True)
    
#     if st.session_state.search_history:
#         for query in st.session_state.search_history[-5:]:
#             st.markdown(f"<p style='margin: 0.5rem 0;'>• {query}</p>", unsafe_allow_html=True)
#     else:
#         st.markdown("<p>No queries yet</p>", unsafe_allow_html=True)
    
#     st.markdown("</div></div>", unsafe_allow_html=True)

# # Chat Interface
# with col2:
#     st.markdown("""
#     <div style='background-color: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 1rem;'>
#         <h2 style='color: #007bff; margin-bottom: 1.5rem;'>💬 Nexus AI Assistant</h2>
#         <div class='chat-container' id='chat-container'>
#     """, unsafe_allow_html=True)
    
#     # Display chat messages
#     for message in st.session_state.messages:
#         if message["role"] == "user":
#             st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
#         else:
#             st.markdown(f"<div class='bot-message'>{message['content']}</div>", unsafe_allow_html=True)
    
#     st.markdown("</div></div>", unsafe_allow_html=True)
    
#     # Input area
#     input_text = st.text_input("Type your message...", key="input", label_visibility="collapsed")
    
#     col_a, col_b = st.columns([3, 1])
#     with col_a:
#         uploaded_image = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
#     with col_b:
#         if st.button("Send", use_container_width=True):
#             if input_text or uploaded_image:
#                 st.session_state.query_count += 1
                
#                 # Add user message to chat
#                 user_message = input_text if input_text else "Analyze this image"
#                 st.session_state.messages.append({"role": "user", "content": user_message})
#                 st.session_state.search_history.append(user_message)
#                 st.session_state.topics.append(user_message)
                
#                 # Show typing indicator
#                 typing_html = """
#                 <div class='bot-message'>
#                     <span class='typing-indicator'>Nexus AI is typing...</span>
#                 </div>
#                 """
#                 st.markdown(typing_html, unsafe_allow_html=True)
                
#                 # Get response (with simulated delay for better UX)
#                 with st.spinner(""):
#                     time.sleep(1)  # Simulate processing time
#                     image = Image.open(uploaded_image) if uploaded_image else None
#                     response = get_gemini_response(input_text, image)
#                     st.session_state.messages.append({"role": "assistant", "content": response})
                
#                 # Rerun to update the chat display
#                 st.rerun()
#             else:
#                 st.warning("Please enter a message or upload an image")

# # JavaScript to auto-scroll chat to bottom
# st.markdown("""
# <script>
#     window.onload = function() {
#         var chatContainer = document.getElementById('chat-container');
#         chatContainer.scrollTop = chatContainer.scrollHeight;
#     }
# </script>
# """, unsafe_allow_html=True)

from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from collections import Counter
import time

# Set page configuration FIRST
st.set_page_config(page_title="Nexus AI", layout="wide", page_icon="🌸")

load_dotenv()

# Configure API
os.environ["GOOGLE_API_KEY"] = "AIzaSyAWfi-RW03Sq6wUcNhpvuBJ7OO5rcluC5I"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Initialize session state
if 'query_count' not in st.session_state:
    st.session_state.query_count = 0
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'topics' not in st.session_state:
    st.session_state.topics = []
if 'ratings' not in st.session_state:
    st.session_state.ratings = []
if 'messages' not in st.session_state:
    st.session_state.messages = []

def get_gemini_response(input, image=None):
    model = genai.GenerativeModel("gemini-1.5-flash")
    if input:
        response = model.generate_content([input, image] if image else [input])
    else:
        response = model.generate_content(image)
    return response.text

# Custom CSS for white & pastel pink theme
st.markdown("""
<style>
    /* Main container */
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }
    
    /* Chat container */
    .chat-container {
        background-color: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(255, 182, 193, 0.15);
        padding: 1.5rem;
        height: 70vh;
        overflow-y: auto;
        border: 1px solid #ffebee;
    }
    
    /* Chat header */
    .chat-header {
        background-color: #ffebee;
        color: #d81b60;
        padding: 8px 16px;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        display: inline-block;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(255, 182, 193, 0.1);
    }
    
    /* User message */
    .user-message {
        background-color: #ffcdd2;
        color: #c2185b;
        border-radius: 18px 18px 0 18px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 70%;
        float: right;
        clear: both;
        box-shadow: 0 2px 6px rgba(216, 27, 96, 0.1);
    }
    
    /* Bot message */
    .bot-message {
        background-color: #f8bbd0;
        color: #880e4f;
        border-radius: 18px 18px 18px 0;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 70%;
        float: left;
        clear: both;
        box-shadow: 0 2px 6px rgba(216, 27, 96, 0.05);
    }
    
    /* Input area */
    .stTextInput>div>div>input {
        border-radius: 20px !important;
        padding: 12px 16px !important;
        background-color: white !important;
        color: #333 !important;
        border: 1px solid #ffcdd2 !important;
    }
    
    /* Button */
    .stButton>button {
        border-radius: 20px !important;
        background-color: #ff80ab !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 8px rgba(255, 128, 171, 0.3) !important;
        transition: all 0.2s !important;
    }
    
    .stButton>button:hover {
        background-color: #ff4081 !important;
        transform: translateY(-2px) !important;
    }
    
    /* File uploader */
    .stFileUploader>div>div>div>div>div {
        border-radius: 20px !important;
        background-color: white !important;
        border: 1px solid #ffcdd2 !important;
        color: #333 !important;
    }
    
    /* Analytics card */
    .analytics-card {
        background-color: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(255, 182, 193, 0.1);
        padding: 1.25rem;
        margin-bottom: 1rem;
        color: #333;
        border: 1px solid #ffebee;
    }
    
    /* Typing animation */
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    .typing-indicator {
        display: inline-block;
        overflow: hidden;
        white-space: nowrap;
        color: #880e4f;
        animation: typing 1.5s steps(40, end);
    }
    
    /* Remove Streamlit default elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #ffebee;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: #ff80ab;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([1, 2])

# Analytics Dashboard (Left Column)
with col1:
    st.markdown("""
    <div style='background-color: white; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 20px rgba(255, 182, 193, 0.1); border: 1px solid #ffebee;'>
        <h2 style='color: #d81b60; border-bottom: 1px solid #ffcdd2; padding-bottom: 0.5rem;'>📊 Analytics</h2>
        <div class='analytics-card'>
            <h4 style='color: #ff80ab;'>Total Queries</h4>
            <h2 style='color: #d81b60;'>{}</h2>
        </div>
    """.format(st.session_state.query_count), unsafe_allow_html=True)
    
    if st.session_state.topics:
        most_common_topic = Counter(st.session_state.topics).most_common(1)[0]
        st.markdown(f"""
        <div class='analytics-card'>
            <h4 style='color: #ff80ab;'>Most Common Topic</h4>
            <p style='font-size: 1.1rem; color: #333;'>{most_common_topic[0]}</p>
            <small style='color: #888;'>Count: {most_common_topic[1]}</small>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.ratings:
        average_rating = sum(st.session_state.ratings) / len(st.session_state.ratings)
        st.markdown(f"""
        <div class='analytics-card'>
            <h4 style='color: #ff80ab;'>User Satisfaction</h4>
            <div style='display: flex; align-items: center;'>
                <span style='font-size: 1.5rem; color: #ff9800;'>{"★" * int(round(average_rating))}</span>
                <span style='margin-left: 0.5rem; color: #333;'>{average_rating:.1f}/5</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='analytics-card'>
            <h4 style='color: #ff80ab;'>📝 Recent Queries</h4>
    """, unsafe_allow_html=True)
    
    if st.session_state.search_history:
        for query in st.session_state.search_history[-5:]:
            st.markdown(f"<p style='margin: 0.5rem 0; color: #333;'>• {query}</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: #888;'>No queries yet</p>", unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# Chat Interface (Right Column)
with col2:
    st.markdown("""
    <div style='background-color: transparent; padding: 0;'>
        <div class='chat-header'>🌸 Nexus AI</div>
        <div class='chat-container' id='chat-container'>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-message'>{message['content']}</div>", unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Input area with form for clearing on submit
    with st.form(key='chat_form', clear_on_submit=True):
        input_col, button_col = st.columns([4, 1])
        with input_col:
            input_text = st.text_input("Type your message...", key="input", label_visibility="collapsed")
            uploaded_image = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
        with button_col:
            submitted = st.form_submit_button("Send", use_container_width=True)
        
        if submitted:
            if input_text or uploaded_image:
                st.session_state.query_count += 1
                
                # Add user message to chat
                user_message = input_text if input_text else "Analyze this image"
                st.session_state.messages.append({"role": "user", "content": user_message})
                st.session_state.search_history.append(user_message)
                st.session_state.topics.append(user_message)
                
                # Show typing indicator
                typing_html = """
                <div class='bot-message'>
                    <span class='typing-indicator'>Nexus AI is thinking...</span>
                </div>
                """
                st.markdown(typing_html, unsafe_allow_html=True)
                
                # Get response (with simulated delay for better UX)
                with st.spinner(""):
                    time.sleep(1)
                    image = Image.open(uploaded_image) if uploaded_image else None
                    response = get_gemini_response(input_text, image)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
                st.rerun()
            else:
                st.warning("Please enter a message or upload an image")

# JavaScript to auto-scroll chat to bottom
st.markdown("""
<script>
    window.onload = function() {
        var chatContainer = document.getElementById('chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
</script>
""", unsafe_allow_html=True)
