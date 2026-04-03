from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """Represents a song and its audio attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    liveness: float
    instrumentalness: float
    speechiness: float

@dataclass
class UserProfile:
    """Stores a user's derived taste preferences built from their liked songs."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_danceability: float
    target_acousticness: float
    target_tempo_bpm: float
    target_instrumentalness: float
    target_liveness: float
    target_speechiness: float
    liked_song_ids: list

class Recommender:
    """OOP wrapper around the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"


def load_songs(csv_path: str) -> List[Dict]:
    """Reads songs.csv and returns a list of song dicts with numeric fields cast to float/int."""
    import csv

    numeric_fields = {
        "id": int,
        "energy": float,
        "tempo_bpm": float,
        "valence": float,
        "danceability": float,
        "acousticness": float,
        "liveness": float,
        "instrumentalness": float,
        "speechiness": float,
    }

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field, cast in numeric_fields.items():
                row[field] = cast(row[field])
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    return songs


MOOD_ADJACENCY = {
    "chill":       ["relaxed", "focused"],
    "relaxed":     ["chill", "happy"],
    "focused":     ["chill", "melancholic"],
    "happy":       ["relaxed", "energetic"],
    "intense":     ["angry", "energetic"],
    "angry":       ["intense"],
    "moody":       ["melancholic", "sad"],
    "melancholic": ["moody", "sad"],
    "sad":         ["melancholic", "moody"],
    "energetic":   ["intense", "happy"],
    "nostalgic":   ["melancholic", "relaxed"],
}


def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """Scores a single song against user preferences and returns (total_score, reasons_string)."""
    score = 0.0
    reasons = []

    # --- Mood (max 3.0) ---
    song_mood = song["mood"]
    user_mood = user_prefs.get("mood", "")
    if song_mood == user_mood:
        score += 3.0
        reasons.append("mood match (+3.0)")
    elif song_mood in MOOD_ADJACENCY.get(user_mood, []):
        score += 1.5
        reasons.append("close mood match (+1.5)")

    # --- Genre (max 2.0) ---
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # --- Numeric features: points = max_points * (1 - abs(song_value - user_value)) ---
    numeric_features = [
        ("energy",           "energy",           2.5),
        ("acousticness",     "acousticness",     2.0),
        ("instrumentalness", "instrumentalness", 1.0),
        ("valence",          "valence",          0.8),
        ("danceability",     "danceability",     0.4),
        ("tempo_bpm",        "tempo_bpm",        0.3),
    ]

    TEMPO_MIN, TEMPO_MAX = 60.0, 168.0

    for song_key, pref_key, max_pts in numeric_features:
        if pref_key in user_prefs:
            song_val = song[song_key]
            user_val = user_prefs[pref_key]
            if song_key == "tempo_bpm":
                song_val = (song_val - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
                user_val = (user_val - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)
            pts = max_pts * (1 - abs(song_val - user_val))
            score += pts
            reasons.append(f"{song_key} match (+{pts:.2f})")

    return round(score, 2), ", ".join(reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every unheard song, sorts by score descending, and returns the top-k results."""
    liked_ids = user_prefs.get("liked_song_ids", [])

    scored = [
        (song, *score_song(song, user_prefs))
        for song in songs
        if song["id"] not in liked_ids
    ]

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
