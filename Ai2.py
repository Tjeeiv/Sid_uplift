import os 
import streamlit as st
import tiktoken 
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv() 
apikey = os.getenv("Puter_API_KEY")

st.set_page_config(page_title="Pro Text Completer")
st.title("Text Completer")

with st.sidebar:
    st.header("Config")

    model_choice = st.selectbox (
        " Select Model", ["gpt-4o","gpt-4o-mini"],
        index=0,
        help = "gpy-4o is smartest; gpt-4o-mini is fastest/cheapest."
    )

    persona_type = st.selectbox(
        "Assistant Persona" ,
        ["GA" , "CW"],
        index = 0
    )

    personas = {
        "GA": "You are ahelpful, concise assistant.",
        "CW":"You are highly imaginative novelist. Use descriptive language and vivid metaphors."
    }

    system_prompt = personas[persona_type]

    temp = st.slider("Temperature(Creativity)", 0.0, 1.5,0.7,0.1)

    st.divider()
    st.info("new app")


def countTokens(text,model_name):
        try:
            encoding = tiktoken.encoding_for_model("gpt-4o")
            return len(encoding.encode(text))
        except:
            return 0

if not apikey:
     st.error("No Key")
     st.stop()

client = OpenAI(base_url= "https://api.puter.com/puterai/openai/v1/" , api_key=apikey)

UserInput = st.text_area("What should I do",placeholder="Tell me",height = 150)

if st.button("Generate Completion"):
    if UserInput.strip()=="":
        st.warning("Type something")
    else:
        token_in=countTokens(UserInput , model_choice)
        st.caption(f"Input: {token_in} Tokens")

        st.subheader("Output: ")
        responsePlaceholder = st.empty()
        FullResponse = ""

        try:
            stream = client.chat.completions.create(model=model_choice, 
                                                    messages=[{"role": "system", "content":system_prompt} ,
                                                               {"role": "user", "content":UserInput}]
                                                                 ,temperature= temp, stream = True)
            
            for chunk in stream:
                 if chunk.choices[0].delta.content is not None:
                      FullResponse += chunk.choices[0].delta.content

                      responsePlaceholder.markdown(FullResponse)
            
            responsePlaceholder.markdown(FullResponse)

            token_out = countTokens(FullResponse,model_choice)
            st.success(f"Generation Complete | Total : {token_in+token_out} tokens")
            
                 
                 
        except Exception as e:
             st.error(f"error: {e}")