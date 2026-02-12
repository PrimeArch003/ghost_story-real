import streamlit as st
import os
from openai import OpenAI

# Create OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Ghost Mode AI Story Generator 👻")

# Story prompt input
prompt = st.text_input("Enter your story prompt:", key="story_prompt")

# Story style selector
style = st.selectbox(
    "Choose a story style:",
    ["Horror", "Sci-Fi", "Romance", "Adventure", "Comedy"],
    key="story_style"
)

# Generate story button
if st.button("Generate Story"):
    if prompt.strip() == "":
        st.warning("Type something first!")
    else:
        with st.spinner("Creating story..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a creative writer. Write in a {style} style."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )

            story = response.choices[0].message.content
            st.success("Here’s your story:")
            st.write(story)
            word_count = len(story.split())
            st.info(f"Word count: {word_count}")
            st.download_button(
    label="Download Story as .txt",
    data=story,
    file_name="ghost_story.txt",
    mime="text/plain"
)




