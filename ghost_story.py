import streamlit as st
from openai import OpenAI
import json
from pathlib import Path
import random
from streamlit_lottie import st_lottie
import requests
import streamlit_authenticator as stauth

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="BlueGhost Studio", page_icon="👻", layout="centered")

# ----------------------------
# Story Storage Setup
# ----------------------------
STORIES_FILE = Path("stories.json")

if not STORIES_FILE.exists():
    STORIES_FILE.write_text(json.dumps({}))

with open(STORIES_FILE) as f:
    stories_db = json.load(f)

# ----------------------------
# Streamlit Authenticator Setup
# ----------------------------
authenticator = stauth.Authenticate(
    st.secrets["credentials"],
    st.secrets["cookie"]["name"],
    st.secrets["cookie"]["key"],
    st.secrets["cookie"]["expiry_days"]
)

# ----------------------------
# Login
# ----------------------------
name, authentication_status, username = authenticator.login()

if authentication_status:
    # ----------------------------
    # Logout in sidebar
    # ----------------------------
    authenticator.logout("Logout", "sidebar")

    # ----------------------------
    # Floating ghost background (visual only)
    # ----------------------------
    st.markdown(
        """
        <style>
        body {
            background-color: #0a0a0a;
            background-image: url('https://i.imgur.com/1lKf1wC.png');
            background-size: cover;
            animation: float 30s infinite linear;
        }
        @keyframes float {
            0% { background-position: 0 0; }
            50% { background-position: 50% 50%; }
            100% { background-position: 0 0; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ----------------------------
    # Sidebar Navigation
    # ----------------------------
    page = st.sidebar.radio("Go to", ["Home", "Profile", "Tips", "Ghost Character"])

    # ----------------------------
    # OpenAI Client
    # ----------------------------
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

    # ----------------------------
    # Theme Styles
    # ----------------------------
    theme_styles = {
        "Horror": "background-color:#0d1b2a;color:#a0e7e5;font-family:serif;text-shadow:0 0 8px #a0e7e5;",
        "Sci-Fi": "background-color:#001133;color:#00FFFF;font-family:monospace;text-shadow:0 0 5px #00FFFF;",
        "Romance": "background-color:#FFE4E1;color:#990000;text-shadow:0 0 3px pink;font-family:serif;",
        "Adventure": "background-color:#556B2F;color:#FFFFFF;font-weight:bold;font-family:sans-serif;",
        "Comedy": "background-color:#FFFACD;color:#00008B;font-family:comic-sans-ms;"
    }

    # ----------------------------
    # HOME PAGE
    # ----------------------------
    if page == "Home":
        st.markdown(f"<h1 style='text-align:center;'>👻 BlueGhost AI - Welcome {name}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:gray;'>Generate ghostly stories instantly!</p>", unsafe_allow_html=True)

        prompt = st.text_input("Enter your story prompt:")
        style = st.selectbox("Choose a story style:", ["Horror", "Sci-Fi", "Romance", "Adventure", "Comedy"])

        if st.button("Generate Story"):
            if prompt.strip() == "":
                st.warning("Type something first!")
            else:
                with st.spinner("Generating story..."):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": f"You are a creative writer. Write in a {style} style."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=300,
                        temperature=0.7
                    )
                    story = response.choices[0].message["content"]

                    # Save story in JSON
                    user_stories = stories_db.get(username, [])
                    user_stories.append({"prompt": prompt, "style": style, "story": story})
                    stories_db[username] = user_stories
                    with open(STORIES_FILE, "w") as f:
                        json.dump(stories_db, f)

                    # Display story
                    style_css = theme_styles.get(style, "background-color:#111111;color:white;")
                    st.subheader("📖 Your Generated Story")
                    st.markdown(
                        f"""
                        <div style='{style_css} padding:20px; border-radius:10px; max-height:400px; overflow-y:auto; box-shadow:0 0 15px #00ffff; animation: glow 2s infinite alternate'>
                            {story}
                        </div>
                        <style>
                        @keyframes glow {{
                            from {{ box-shadow:0 0 10px #00ffff; }}
                            to {{ box-shadow:0 0 20px #00ffff; }}
                        }}
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    st.info(f"Word count: {len(story.split())}")
                    st.download_button("Download Story", story, f"{style}_story.txt", "text/plain")

    # ----------------------------
    # PROFILE PAGE
    # ----------------------------
    elif page == "Profile":
        st.header(f"{name}'s Profile 👻")
        st.write("Your previously generated stories:")

        user_stories = stories_db.get(username, [])
        if not user_stories:
            st.info("No stories yet. Go to Home to generate some!")
        else:
            def load_lottieurl(url: str):
                r = requests.get(url)
                if r.status_code != 200:
                    return None
                return r.json()

            lottie_ghost = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jtbfg2nb.json")

            for idx, entry in enumerate(reversed(user_stories), 1):
                st.markdown(f"**{idx}. [{entry['style']}] {entry['prompt']}**")
                st.markdown(
                    f"<div style='background-color:#111111;color:#a0e7e5;padding:10px;border-radius:10px; max-height:200px; overflow-y:auto; box-shadow:0 0 15px #00ffff; animation: glow 2s infinite alternate'>{entry['story']}</div>",
                    unsafe_allow_html=True
                )
                st_lottie(lottie_ghost, height=100)
                st.download_button(
                    "Download Story",
                    entry['story'],
                    f"{entry['style']}_story_{idx}.txt",
                    "text/plain"
                )
                st.write("---")

    # ----------------------------
    # TIPS PAGE
    # ----------------------------
    elif page == "Tips":
        st.header("Writing Tips & Prompts")
        st.write("- Start with **'It was a foggy night...'**")
        st.write("- Mix genres: 'Romantic Horror', 'Sci-Fi Comedy'")
        st.write("- Focus on atmosphere: describe sights, sounds, and feelings")
        st.write("- Try a 100-word micro story challenge")
        st.write("- Give your ghost a personality and backstory!")

    # ----------------------------
    # GHOST CHARACTER PAGE
    # ----------------------------
    elif page == "Ghost Character":
        st.header("Create Your Ghost Character 👻")
        st.write("Generate a fun ghost character for your stories!")

        names = ["Etherea", "Lumino", "Whisper", "Shade", "Glimmer", "Phantom"]
        personalities = ["Mysterious", "Cheerful", "Melancholic", "Playful", "Wise", "Shy"]
        quirks = ["floats silently", "glows softly", "makes eerie sounds", "vanishes at will", "loves storytelling"]

        if st.button("Generate Character"):
            name_char = random.choice(names)
            personality = random.choice(personalities)
            quirk = random.choice(quirks)

            st.markdown(f"**Name:** {name_char}")
            st.markdown(f"**Personality:** {personality}")
            st.markdown(f"**Special Quirk:** {quirk}")

            lottie_char = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jtbfg2nb.json")
            st_lottie(lottie_char, height=150)

# ----------------------------
# Login Failed / None
# ----------------------------
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
