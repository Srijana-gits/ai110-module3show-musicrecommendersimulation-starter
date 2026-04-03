import sys
import streamlit as st

sys.path.insert(0, "src")
from recommender import load_songs, recommend_songs

songs = load_songs("data/songs.csv")

all_genres = sorted(set(s["genre"] for s in songs))
all_moods  = sorted(set(s["mood"]  for s in songs))
all_titles = {s["id"]: f"{s['title']} — {s['artist']}" for s in songs}

st.title("🎵 Music Recommender")
st.caption("Content-based recommendations powered by your taste profile.")

st.sidebar.header("Your Preferences")

genre = st.sidebar.selectbox("Favorite Genre", all_genres)
mood  = st.sidebar.selectbox("Favorite Mood",  all_moods)

energy           = st.sidebar.slider("Energy",           0.0, 1.0, 0.38, 0.01)
acousticness     = st.sidebar.slider("Acousticness",     0.0, 1.0, 0.82, 0.01)
instrumentalness = st.sidebar.slider("Instrumentalness", 0.0, 1.0, 0.79, 0.01)
valence          = st.sidebar.slider("Valence",          0.0, 1.0, 0.60, 0.01)
danceability     = st.sidebar.slider("Danceability",     0.0, 1.0, 0.55, 0.01)
tempo_bpm        = st.sidebar.slider("Tempo (BPM)",      60.0, 168.0, 72.5, 0.5)

liked = st.sidebar.multiselect(
    "Songs you've already heard (exclude from results)",
    options=list(all_titles.keys()),
    format_func=lambda i: all_titles[i],
    default=[2, 4, 9, 6],
)

k = st.sidebar.slider("Number of recommendations", 1, 10, 5)

user_prefs = {
    "genre":            genre,
    "mood":             mood,
    "energy":           energy,
    "acousticness":     acousticness,
    "instrumentalness": instrumentalness,
    "valence":          valence,
    "danceability":     danceability,
    "tempo_bpm":        tempo_bpm,
    "liked_song_ids":   liked,
}

results = recommend_songs(user_prefs, songs, k=k)

st.subheader("Top Recommendations")

if not results:
    st.warning("No recommendations found. Try adjusting your preferences.")
else:
    for rank, (song, score, explanation) in enumerate(results, start=1):
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**#{rank} {song['title']}** — {song['artist']}")
                st.caption(f"Genre: {song['genre']}  |  Mood: {song['mood']}")
                st.caption(f"Why: {explanation}")
            with col2:
                st.metric("Score", score)
            st.divider()
