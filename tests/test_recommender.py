import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.recommender import Song, UserProfile, Recommender, score_song, recommend_songs

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_score_song_uses_profile_fields_for_rankings():
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    song = {
        "id": 1,
        "title": "Sunrise City",
        "artist": "Neon Echo",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.82,
        "tempo_bpm": 118,
        "valence": 0.84,
        "danceability": 0.79,
        "acousticness": 0.18,
    }

    score, reasons = score_song(user_prefs, song)

    assert isinstance(score, float)
    assert score > 0.5
    assert any("genre" in reason.lower() for reason in reasons)
    assert any("mood" in reason.lower() for reason in reasons)


def test_recommend_songs_returns_ranked_list():
    songs = [
        {
            "id": 1,
            "title": "Sunrise City",
            "artist": "Neon Echo",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.82,
            "tempo_bpm": 118,
            "valence": 0.84,
            "danceability": 0.79,
            "acousticness": 0.18,
        },
        {
            "id": 2,
            "title": "Midnight Coding",
            "artist": "LoRoom",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.42,
            "tempo_bpm": 78,
            "valence": 0.56,
            "danceability": 0.62,
            "acousticness": 0.71,
        },
    ]
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    results = recommend_songs(user_prefs, songs, k=2)

    assert len(results) == 2
    assert results[0][0]["title"] == "Sunrise City"
    assert results[0][1] >= results[1][1]
