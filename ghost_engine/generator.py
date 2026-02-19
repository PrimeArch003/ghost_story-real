from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def generate_story(prompt, style):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"You are a creative writer. Write in a {style} style.\n\n{prompt}",
        max_output_tokens=400,
        temperature=0.8
    )

    return response.output[0].content[0].text


def continue_story(previous_story, style):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Continue this story in {style} style:\n\n{previous_story}",
        max_output_tokens=400,
        temperature=0.85
    )

    return response.output[0].content[0].text
