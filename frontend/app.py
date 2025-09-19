import streamlit as st
import requests
import time

# Set page config
st.set_page_config(
    page_title="HR Policy Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
}
.chat-message.user {
    background-color: #f0f2f6;
}
.chat-message.assistant {
    background-color: #e6f7ff;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "api_url" not in st.session_state:
    st.session_state.api_url = "http://backend:8000"

# Sidebar for configuration
with st.sidebar:
    st.title("HR Policy Chatbot")
    st.markdown("Ask questions about your HR policies")
    
    st.subheader("Configuration")
    api_url = st.text_input("API URL", st.session_state.api_url)
    if api_url != st.session_state.api_url:
        st.session_state.api_url = api_url
        st.success(f"API URL updated to {api_url}")

# Main chat interface
st.title("HR Policy Chatbot")
st.markdown("Ask me anything about the HR policies!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message and message["sources"]:
            with st.expander("View Sources"):
                for i, source in enumerate(message["sources"]):
                    st.markdown(f"{i+1}. {source}")

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Call backend API
            response = requests.post(
                f"{st.session_state.api_url}/query",
                json={"question": prompt},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data["answer"]
                sources = data["sources"]
                
                # Display answer
                message_placeholder.markdown(answer)
                
                # Display sources if available
                if sources:
                    with st.expander("View Sources"):
                        for i, source in enumerate(sources):
                            st.markdown(f"{i+1}. {source}")
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "sources": sources
                })
            else:
                error_msg = f"Error: {response.status_code} - {response.text}"
                message_placeholder.markdown(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error: {str(e)}"
            message_placeholder.markdown(error_msg)
            st.session_state.messages.append({
                "role": "assistant", 
                "content": error_msg
            })