import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv
load_dotenv()

## langsmith tracking

os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_PROJECT'] = 'chatbot'

# promt template

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","hey you are a helful assistence. please response the user query with very very politely"),
        ("user","question:{question}")
    ]
)

def generate_response(question,llm,tempreture,max_tokens):
    llm = ChatGroq(model=llm,max_tokens=max_tokens)
    output = StrOutputParser()
    chain = prompt|llm|output
    answer = chain.stream({"question":question})
    return answer

##title

st.title("Q&A CHATBOT")
st.sidebar.title("SETTINGS")

## dropdown 
model_dict = {
    "OpenAI GPT-OSS 120B": "openai/gpt-oss-120b",
    "OpenAI GPT-OSS 20B": "openai/gpt-oss-20b",
    "Llama 3.3 70B": "llama-3.3-70b-versatile",
}

selected = st.sidebar.selectbox("select an model",list(model_dict.keys()))
llm = model_dict[selected]
tempreture = st.sidebar.slider("Tempreture",min_value=0.0,max_value=1.0,value=0.7)
max_tokens =  st.sidebar.slider("Max Tokens",min_value=500,max_value=2000,value=800)

#main interface

st.write("Ask any Question")

user_input = st.text_input("you:")
if user_input:
    with st.spinner():
        response = generate_response(user_input,llm,tempreture,max_tokens)
        st.write(response)
else:
    st.write("Please provide the Questuion")
