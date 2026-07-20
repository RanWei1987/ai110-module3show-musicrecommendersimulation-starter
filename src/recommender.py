import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

GENRE_ORDER = ["rock", "synthwave", "indie pop", "pop", "jazz", "lofi", "ambient"]
MOOD_ORDER = ["intense", "happy", "focused", "moody", "chill", "relaxed"]
MOOD_VALENCE_PREFERENCE = {
    "happy": 0.85,
    "relaxed": 0.75,
    "chill": 0.65,
    "focused": 0.55,
    "moody": 0.45,
    "intense": 0.40,
}
MOOD_DANCEABILITY_PREFERENCE = {
    "happy": 0.85,
    "intense": 0.80,
    "focused": 0.65,
    "chill": 0.60,
    "relaxed": 0.55,
    "moody": 0.50,
}


def _normalize_user_prefs(user_prefs: Dict) -> Dict:
    return {
        "genre": user_prefs.get("genre") or user_prefs.get("favorite_genre"),
        "mood": user_prefs.get("mood") or user_prefs.get("favorite_mood"),
        "energy": user_prefs.get("energy") or user_prefs.get("target_energy"),
        "likes_acoustic": user_prefs.get("likes_acoustic", False),
    }


def _normalize_song(song: Dict) -> Dict:
    return {
        "id": int(song["id"]),
        "title": song["title"],
        "artist": song["artist"],
        "genre": song["genre"],
        "mood": song["mood"],
        "energy": float(song["energy"]),
        "tempo_bpm": float(song["tempo_bpm"]),
        "valence": float(song["valence"]),
        "danceability": float(song["danceability"]),
        "acousticness": float(song["acousticness"]),
    }


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        ranked = []

        for song in self.songs:
            song_dict = {
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "tempo_bpm": song.tempo_bpm,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            }
            score, reasons = score_song(user_prefs, song_dict)
            ranked.append((song, score, reasons))

        ranked.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _, _ in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }
        _, reasons = score_song(user_prefs, song_dict)
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            song = {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    print(f"Loading songs from {csv_path}...")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    user_prefs = _normalize_user_prefs(user_prefs)
    song = _normalize_song(song)

    reasons: List[str] = []
    total_score = 0.0

    preferred_genre = user_prefs["genre"]
    preferred_mood = user_prefs["mood"]
    target_energy = user_prefs["energy"]
    likes_acoustic = bool(user_prefs["likes_acoustic"])

    if preferred_genre and song["genre"] == preferred_genre:
        total_score += 0.40
        reasons.append(f"Matches preferred genre: {preferred_genre}")
    else:
        if preferred_genre in GENRE_ORDER and song["genre"] in GENRE_ORDER:
            genre_distance = abs(GENRE_ORDER.index(preferred_genre) - GENRE_ORDER.index(song["genre"]))
            genre_similarity = max(0.0, 1.0 - (genre_distance / (len(GENRE_ORDER) - 1)))
            total_score += 0.40 * genre_similarity
            reasons.append(
                f"Genre similarity: {genre_similarity:.2f} "
                f"(preferred {preferred_genre}, song {song['genre']})"
            )

    if preferred_mood and song["mood"] == preferred_mood:
        total_score += 0.30
        reasons.append(f"Matches preferred mood: {preferred_mood}")
    else:
        if preferred_mood in MOOD_ORDER and song["mood"] in MOOD_ORDER:
            mood_distance = abs(MOOD_ORDER.index(preferred_mood) - MOOD_ORDER.index(song["mood"]))
            mood_similarity = 1.0 - (mood_distance / (len(MOOD_ORDER) - 1))
            total_score += 0.30 * mood_similarity
            reasons.append(
                f"Mood similarity: {mood_similarity:.2f} "
                f"(preferred {preferred_mood}, song {song['mood']})"
            )

    if target_energy is not None:
        energy_gap = abs(float(song["energy"]) - float(target_energy))
        energy_similarity = max(0.0, 1.0 - energy_gap)
        total_score += 0.20 * energy_similarity
        reasons.append(
            f"Energy closeness: {energy_similarity:.2f} "
            f"(song {song['energy']:.2f}, target {float(target_energy):.2f})"
        )

        tempo_target = 60.0 + (float(target_energy) * 140.0)
        tempo_gap = abs(float(song["tempo_bpm"]) - tempo_target)
        tempo_similarity = max(0.0, 1.0 - (tempo_gap / 140.0))
        total_score += 0.10 * tempo_similarity
        reasons.append(
            f"Tempo alignment: {tempo_similarity:.2f} "
            f"(song {song['tempo_bpm']:.0f}, target {tempo_target:.0f})"
        )

    valence_target = MOOD_VALENCE_PREFERENCE.get(preferred_mood, 0.6)
    valence_similarity = max(0.0, 1.0 - abs(float(song["valence"]) - valence_target))
    total_score += 0.05 * valence_similarity
    reasons.append(
        f"Valence match: {valence_similarity:.2f} "
        f"(song valence {song['valence']:.2f}, target {valence_target:.2f})"
    )

    danceability_target = MOOD_DANCEABILITY_PREFERENCE.get(preferred_mood, 0.6)
    danceability_similarity = max(0.0, 1.0 - abs(float(song["danceability"]) - danceability_target))
    total_score += 0.05 * danceability_similarity
    reasons.append(
        f"Danceability match: {danceability_similarity:.2f} "
        f"(song danceability {song['danceability']:.2f}, target {danceability_target:.2f})"
    )

    acousticness = float(song["acousticness"])
    if likes_acoustic:
        total_score += 0.05 * acousticness
        reasons.append(f"Likes acoustic songs: acousticness bonus {acousticness:.2f}")
    else:
        total_score += 0.05 * (1.0 - acousticness)
        reasons.append(f"Prefers less acoustic songs: non-acoustic bonus {1.0 - acousticness:.2f}")

    return round(min(total_score, 1.0), 4), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    ranked: List[Tuple[Dict, float, str]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        ranked.append((song, score, explanation))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked[:k]
