"""
Command line runner for the Music Recommender Simulation.
Runs all user profiles (standard + adversarial) and prints top-5 recommendations.
"""

from tabulate import tabulate
from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Standard user preference profiles
# ---------------------------------------------------------------------------

HIGH_ENERGY_POP = {
    "label":            "High-Energy Pop",
    "genre":            "pop",
    "mood":             "energetic",
    "energy":           0.92,
    "acousticness":     0.05,
    "instrumentalness": 0.01,
    "valence":          0.88,
    "danceability":     0.85,
    "tempo_bpm":        128.0,
    "liked_song_ids":   [],
}

CHILL_LOFI = {
    "label":            "Chill Lofi",
    "genre":            "lofi",
    "mood":             "chill",
    "energy":           0.25,
    "acousticness":     0.80,
    "instrumentalness": 0.75,
    "valence":          0.45,
    "danceability":     0.40,
    "tempo_bpm":        75.0,
    "liked_song_ids":   [],
}

DEEP_INTENSE_ROCK = {
    "label":            "Deep Intense Rock",
    "genre":            "rock",
    "mood":             "intense",
    "energy":           0.95,
    "acousticness":     0.06,
    "instrumentalness": 0.30,
    "valence":          0.30,
    "danceability":     0.55,
    "tempo_bpm":        145.0,
    "liked_song_ids":   [],
}

# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles — designed to stress-test scoring logic
# ---------------------------------------------------------------------------

# Conflicting: very high energy but sad mood (energy vs. mood mismatch)
CONFLICTED_ENERGY_SAD = {
    "label":            "[Adversarial] High-Energy + Sad Mood",
    "genre":            "pop",
    "mood":             "sad",
    "energy":           0.95,
    "acousticness":     0.10,
    "instrumentalness": 0.02,
    "valence":          0.05,   # very low valence (dark) but energy is high
    "danceability":     0.85,
    "tempo_bpm":        130.0,
    "liked_song_ids":   [],
}

# Extreme minimums: all numeric features set to near-zero
ALL_ZEROS = {
    "label":            "[Adversarial] All-Zero Numeric Features",
    "genre":            "jazz",
    "mood":             "melancholic",
    "energy":           0.0,
    "acousticness":     0.0,
    "instrumentalness": 0.0,
    "valence":          0.0,
    "danceability":     0.0,
    "tempo_bpm":        60.0,   # TEMPO_MIN so normalized value = 0
    "liked_song_ids":   [],
}

# Conflicting genre+mood: angry mood but genre that rarely pairs with it
GENRE_MOOD_MISMATCH = {
    "label":            "[Adversarial] Angry Mood + Lofi Genre",
    "genre":            "lofi",
    "mood":             "angry",
    "energy":           0.90,
    "acousticness":     0.70,   # high acousticness contradicts high energy
    "instrumentalness": 0.80,
    "valence":          0.10,
    "danceability":     0.30,
    "tempo_bpm":        160.0,
    "liked_song_ids":   [],
}

# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

ALL_PROFILES = [
    HIGH_ENERGY_POP,
    CHILL_LOFI,
    DEEP_INTENSE_ROCK,
    CONFLICTED_ENERGY_SAD,
    ALL_ZEROS,
    GENRE_MOOD_MISMATCH,
]


def print_recommendations(label: str, recommendations) -> None:
    print("\n" + "=" * 60)
    print(f"  PROFILE: {label}")
    print("=" * 60)

    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        # wrap reasons onto separate lines for readability
        reasons = explanation.replace(", ", "\n")
        rows.append([rank, song["title"], song["artist"], song["genre"], song["mood"], score, reasons])

    headers = ["#", "Title", "Artist", "Genre", "Mood", "Score", "Reasons"]
    print(tabulate(rows, headers=headers, tablefmt="rounded_outline", colalign=("center",)))
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile in ALL_PROFILES:
        label = profile.pop("label")           # pull label out before scoring
        recommendations = recommend_songs(profile, songs, k=5)
        print_recommendations(label, recommendations)
        profile["label"] = label               # restore so profile stays reusable


if __name__ == "__main__":
    main()
