"""
Command line runner for the Music Recommender Simulation.
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "genre":            "pop",
        "mood":             "happy",
        "energy":           0.8,
        "acousticness":     0.18,
        "instrumentalness": 0.02,
        "valence":          0.84,
        "danceability":     0.79,
        "tempo_bpm":        118.0,
        "liked_song_ids":   [],
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("   TOP RECOMMENDATIONS")
    print("=" * 50)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Score: {score}")
        print(f"    Why:   {explanation}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
