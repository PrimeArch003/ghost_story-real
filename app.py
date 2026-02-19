import streamlit as st
import json
from pathlib import Path
import random
from ghost_engine.generator import generate_story, continue_story
from ghost_engine.personality import ghost_reaction

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="BlueGhost Studio", page_icon="👻", layout="wide")

# ----------------------------
# Data / Story Storage
# ----------------------------
DATA_FILE = Path("data/stories.json")
if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
    DATA_FILE.write_text(json.dumps({}))

with open(DATA_FILE, "r") as f:
    stories_db = json.load(f)

# ----------------------------
# Username Input
# ----------------------------
if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.username is None:
    nickname = st.text_input("Enter your nickname (optional):")
    if nickname.strip():
        st.session_state.username = nickname.strip()

username = st.session_state.username or "guest"

# ----------------------------
# Top Tab Navigation with Improved Font & Glow
# ----------------------------
st.markdown("""
<style>
/* Enlarge tab font and make bold */
.css-1ad5bsp .st-b5 {
    font-size: 20px !important;
    font-weight: bold !important;
}

/* Active tab glow effect (blue) */
.css-1ad5bsp .st-b5[aria-selected="true"] {
    color: #00FFFF !important;
    text-shadow: 0 0 8px #00FFFF;
}

/* Inactive tab color (white) */
.css-1ad5bsp .st-b5[aria-selected="false"] {
    color: #FFFFFF !important;
    text-shadow: none;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Top Tabs
# ----------------------------
tab_home, tab_profile, tab_tips, tab_ghost = st.tabs(
    ["Home", "Profile", "Tips", "Ghost Character"]
)

# ----------------------------
# HOME PAGE
# ----------------------------
with tab_home:
    st.title(f"👻 BlueGhost AI — Welcome {username}")
    st.caption("Generate ghostly stories instantly")

    prompt = st.text_input("Enter your story prompt:")
    style = st.selectbox(
        "Choose a story style:",
        ["Horror", "Sci-Fi", "Romance", "Adventure", "Comedy"]
    )

    # Ghost reaction
    if style:
        st.info(ghost_reaction(style))

    if st.button("Generate Story"):
        if not prompt.strip():
            st.warning("Type something first!")
        else:
            story = generate_story(prompt, style)

            # Save story
            user_stories = stories_db.get(username, [])
            user_stories.append({"prompt": prompt, "style": style, "story": story})
            stories_db[username] = user_stories

            with open(DATA_FILE, "w") as f:
                json.dump(stories_db, f, indent=2)

            # ----------------------------
            # Display story with typewriter effect
            # ----------------------------
            import streamlit.components.v1 as components

            def display_story_typewriter(story_text):
                safe_story = story_text.replace('"', '\\"').replace('\n', '\\n')
                typewriter_html = f"""
                <div id="story" style="white-space: pre-wrap; font-size:16px; line-height:1.5;"></div>
                <script>
                    const text = "{safe_story}";
                    const container = document.getElementById("story");
                    let i = 0;
                    function typeWriter() {{
                        if (i < text.length) {{
                            container.innerHTML += text.charAt(i);
                            i++;
                            setTimeout(typeWriter, 20);
                        }}
                    }}
                    typeWriter();
                </script>
                """
                components.html(typewriter_html, height=400)

            display_story_typewriter(story)

            st.info(f"Word count: {len(story.split())}")

            if st.button("Continue Story"):
                new_part = continue_story(story, style)
                display_story_typewriter(new_part)


# ----------------------------
# PROFILE PAGE
# ----------------------------
with tab_profile:
    st.header(f"{username}'s Profile 👻")
    user_stories = stories_db.get(username, [])

    if not user_stories:
        st.info("No stories yet. Go to Home to generate some!")
    else:
        for idx, entry in enumerate(reversed(user_stories), 1):
            st.markdown(f"**{idx}. [{entry['style']}] {entry['prompt']}**")
            st.markdown(entry["story"])
            st.write("---")

# ----------------------------
# TIPS PAGE
# ----------------------------
with tab_tips:
    st.header("Writing Tips & Prompts")
    st.write("- Start with mystery, suspense, or foggy nights…")
    st.write("- Mix genres: 'Romantic Horror', 'Sci-Fi Comedy'")
    st.write("- Focus on atmosphere: describe sights, sounds, feelings")
    st.write("- Give your ghost a personality and backstory")
    st.write("- Try a 100-word micro story challenge")

# ----------------------------
# GHOST CHARACTER PAGE
# ----------------------------
with tab_ghost:
    st.header("Create Your Ghost Character 👻")

    names = ["Etherea", "Lumino", "Whisper", "Shade", "Glimmer", "Phantom"]
    personalities = ["Mysterious", "Cheerful", "Melancholic", "Playful", "Wise", "Shy"]
    quirks = ["floats silently", "glows softly", "makes eerie sounds", "vanishes at will", "loves storytelling"]

    if st.button("Generate Character"):
        st.markdown(f"**Name:** {random.choice(names)}")
        st.markdown(f"**Personality:** {random.choice(personalities)}")
        st.markdown(f"**Special Quirk:** {random.choice(quirks)}")
