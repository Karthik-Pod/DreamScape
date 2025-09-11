import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# ---------------- Backend status check ----------------
def get_backend_status():
    try:
        response = requests.get("http://localhost:5000/api/status", timeout=5)
        return response.json()
    except:
        return {"status": "offline", "message": "Backend not connected"}

# ---------------- Create a story ----------------
def create_story(preferences):
    try:
        response = requests.post(
            "http://localhost:5000/api/story/create",
            json=preferences,
            timeout=10
        )
        return response.json()
    except:
        return {"success": False, "error": "Failed to connect to backend server"}

# ---------------- Analyze a story ----------------
def analyze_story(story_id):
    try:
        response = requests.post(
            "http://localhost:5000/api/story/analyze",
            json={"story_id": story_id},
            timeout=10
        )
        return response.json()
    except:
        return {"success": False, "error": "Failed to connect for analysis"}

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="DreamScape 🎬", layout="centered")
st.title("🎥 DreamScape - AI Story Creator")

# Show backend status
status = get_backend_status()
if status.get("status") == "online":
    st.success("✅ Backend is connected!")
else:
    st.warning("⚠️ Backend is offline. Please start the backend server.")

# --------- User Input Section ---------
st.subheader("✨ Customize Your Story")

title = st.text_input("📌 Story Title", "The Great Adventure")
genre = st.selectbox("🎭 Choose a Genre", ["Action", "Comedy", "Drama", "Horror", "Fantasy", "Sci-Fi"])
mood = st.selectbox("😊 Choose a Mood", ["Exciting", "Romantic", "Mysterious", "Funny"])
idea = st.text_area("💡 Your Story Idea", "A group of explorers discover a hidden world under the ocean...")
username = st.text_input("👤 Username", "guest_user")

# --------- Create Story Button ---------
if st.button("🚀 Create My Story!", type="primary", use_container_width=True):
    preferences = {
        "title": title,
        "genre": genre,
        "mood": mood,
        "idea": idea,
        "username": username
    }

    with st.spinner("🎬 Creating your story..."):
        result = create_story(preferences)

        if result.get("success"):
            story_id = result.get("story_id")
            st.session_state.story_id = story_id
            st.session_state.story_data = result.get("story")
            st.success(f"✨ Story created! ID: {story_id}")
            st.rerun()
        else:
            st.error(f"Failed to create story: {result.get('error', 'Unknown error')}")

# --------- Analyze Story Section ---------
if "story_id" in st.session_state:
    st.subheader("📡 Story Analysis")
    st.write(f"📖 **Title:** {st.session_state.story_data.get('title')}")
    st.write(f"🎭 **Genre:** {st.session_state.story_data.get('genre')}")
    st.write(f"😊 **Mood:** {st.session_state.story_data.get('mood')}")
    st.write(f"👤 **Author:** {st.session_state.story_data.get('username')}")

    if st.button("🧠 Analyze Story with AI Agents", type="primary", use_container_width=True):
        with st.spinner("🤖 AI agents are analyzing your story..."):
            analysis_result = analyze_story(st.session_state.story_id)

            if analysis_result.get("success"):
                st.success("🎉 AI Analysis Complete!")

                analysis = analysis_result.get("analysis", {})

                # ---------------- Character Section ----------------
                st.subheader("👤 Main Character")
                char_dev = analysis["agent_contributions"]["character_development"]["main_character"]
                st.write(f"**Archetype:** {char_dev['archetype']}")
                st.write(f"**Background:** {char_dev['background']}")
                st.write(f"**Character Arc:** {char_dev['character_arc']}")
                st.write(f"**Motivation:** {char_dev['motivation']}")
                st.write(f"**Personality Traits:** {', '.join(char_dev['personality_traits'])}")
                st.write(f"**Strengths:** {', '.join(char_dev['strengths'])}")
                st.write(f"**Weaknesses:** {', '.join(char_dev['weaknesses'])}")

                # ---------------- Dialogue Section ----------------
                st.subheader("💬 Dialogue Style")
                dialogue = analysis["agent_contributions"]["dialogue_style"]
                ds = dialogue["dialogue_style"]
                st.write(f"**Rhythm:** {ds['rhythm']}")
                st.write(f"**Tone:** {ds['tone']}")
                st.write(f"**Vocabulary:** {ds['vocabulary']}")
                st.write("**Guidelines:**")
                for g in dialogue["guidelines"]:
                    st.markdown(f"- {g}")
                st.write(f"**Mood Adjustments:** {dialogue['mood_adjustments']}")

                # ---------------- Plot Section ----------------
                st.subheader("📖 Plot Analysis")
                plot = analysis["agent_contributions"]["plot_analysis"]
                st.write(f"**Analysis:** {plot['analysis']}")
                st.write(f"**Confidence:** {plot['confidence'] * 100:.1f}%")
                st.write(f"**Key Themes:** {', '.join(plot['key_themes'])}")
                st.write(f"**Pacing Notes:** {plot['pacing_notes']}")
                st.write("**Plot Suggestions:**")
                for ps in plot["plot_suggestions"]:
                    st.markdown(f"- {ps}")

                # ---------------- Synthesis Section ----------------
                st.subheader("📝 Synthesis")
                synthesis = analysis["synthesis"]
                st.write("**Integration Notes:**")
                for note in synthesis["integration_notes"]:
                    st.markdown(f"- {note}")

                st.write("**Story Structure:**")
                for step in synthesis["story_structure"]:
                    st.markdown(f"- {step}")

            else:
                st.error(f"Analysis failed: {analysis_result.get('error', 'Unknown error')}")
