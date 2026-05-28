from transformers import pipeline
import streamlit as st

pipe = pipeline("text-generation", model="microsoft/DialoGPT-medium")

st.title("My Chatbot")

userinput = st.text_input("You", placeholder = "Ask Anything.." )

if st.button("Send"):
  if userinput.strip() == "":
    st.warning("Please Type something")
  else:
    with st.spinner("Thinking..."):
      messages = [{"role": "system", "content": "You are a helpful chatbot."},    {"role": "user", "content": userinput} ]

      result = pipe(messages)
      bot =result[0]["generated_text"][2]["content"]
      
    st.text_area("Bot:", value=bot, height=150)
    st.text_area("Result:", value = result[0]["generated_text"] ,height=150)

#pip install langchain langchain-openai
# pip install langchain langchain-core langchain-openai python-dotenv