# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Top recommendations:

Sunrise City - Score: 1.00
Because: Matches preferred genre: pop; Matches preferred mood: happy; Energy closeness: 0.98 (song 0.82, target 0.80); Tempo alignment: 0.61 (song 118, target 172); Valence match: 0.99 (song valence 0.84, target 0.85); Danceability match: 0.94 (song danceability 0.79, target 0.85); Prefers less acoustic songs: non-acoustic bonus 0.82

Gym Hero - Score: 1.00
Because: Matches preferred genre: pop; Mood similarity: 0.80 (preferred happy, song intense); Energy closeness: 0.87 (song 0.93, target 0.80); Tempo alignment: 0.71 (song 132, target 172); Valence match: 0.92 (song valence 0.77, target 0.85); Danceability match: 0.97 (song danceability 0.88, target 0.85); Prefers less acoustic songs: non-acoustic bonus 0.95

Rooftop Lights - Score: 1.00
Because: Genre similarity: 0.83 (preferred pop, song indie pop); Matches preferred mood: happy; Energy closeness: 0.96 (song 0.76, target 0.80); Tempo alignment: 0.66 (song 124, target 172); Valence match: 0.96 (song valence 0.81, target 0.85); Danceability match: 0.97 (song danceability 0.82, target 0.85); Prefers less acoustic songs: non-acoustic bonus 0.65

Storm Runner - Score: 0.82
Because: Genre similarity: 0.50 (preferred pop, song rock); Mood similarity: 0.80 (preferred happy, song intense); Energy closeness: 0.89 (song 0.91, target 0.80); Tempo alignment: 0.86 (song 152, target 172); Valence match: 0.63 (song valence 0.48, target 0.85); Danceability match: 0.81 (song danceability 0.66, target 0.85); Prefers less acoustic songs: non-acoustic bonus 0.90

Night Drive Loop - Score: 0.81
Because: Genre similarity: 0.67 (preferred pop, song synthwave); Mood similarity: 0.60 (preferred happy, song moody); Energy closeness: 0.95 (song 0.75, target 0.80); Tempo alignment: 0.56 (song 110, target 172); Valence match: 0.64 (song valence 0.49, target 0.85); Danceability match: 0.88 (song danceability 0.73, target 0.85); Prefers less acoustic songs: non-acoustic bonus 0.78
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

- What happened when you changed the weight on genre from 2.0 to 0.5
  - In the scoring function, the genre term is the coefficient attached to the genre-match signal, and the current implementation uses a baseline value of `0.40`. If the coefficient were changed from `2.0` to `0.5`, the model would become much less dominated by genre and would start to rely more heavily on mood, energy, tempo, and valence. Compared with the current `0.40` setting, the `0.50` version would still be slightly more genre-driven, but it would behave fairly similarly because both values are still moderate and do not completely overwhelm the other features. Using the current `0.40` weight gives the best balance: genre is still important, but songs can still rise in the ranking when they match the user’s mood and energy profile well.

- What happened when you added tempo or valence to the score
  - Tempo and valence were already part of the scoring logic. In the observed sample run, songs that matched the target energy and tempo profile were ranked highly, and valence also helped distinguish songs with a similar mood. This means tempo and valence act as useful secondary signals that refine the ranking after genre and mood. 

- How did your system behave for different types of users

  I ran three distinct profiles against the 15-song catalog. The full top-5 output for each is shown below.

  **Profile 1 — pop / happy / 0.8 (strong exact-match user).** The system returned `Sunrise City` first with a perfect score, and the top slots are dominated by songs that match both genre and mood exactly. Non-pop/non-happy tracks only appear once the exact matches are exhausted.

  ```
  Top recommendations:

  Sunrise City - Score: 1.00
  Because: Matches preferred genre: pop; Matches preferred mood: happy; Energy closeness: 0.98 (song 0.82, target 0.80); Tempo alignment: 0.61 (song 118, target 172); Valence match: 0.99 (song valence 0.84, target 0.85); Danceability match: 0.94 (song danceability 0.79, target 0.85); Prefers less acoustic songs: non-acoustic bonus 0.82

  Gym Hero - Score: 1.00
  Because: Matches preferred genre: pop; Mood similarity: 0.80 (preferred happy, song intense); Energy closeness: 0.87 (song 0.93, target 0.80); Tempo alignment: 0.71 (song 132, target 172); Valence match: 0.92 (song valence 0.77, target 0.85); Danceability match: 0.97 (song danceability 0.88, target 0.85); Prefers less acoustic songs: non-acoustic bonus 0.95

  Rooftop Lights - Score: 1.00
  Because: Genre similarity: 0.83 (preferred pop, song indie pop); Matches preferred mood: happy; Energy closeness: 0.96 (song 0.76, target 0.80); Tempo alignment: 0.66 (song 124, target 172); Valence match: 0.96 (song valence 0.81, target 0.85); Danceability match: 0.97 (song danceability 0.82, target 0.85); Prefers less acoustic songs: non-acoustic bonus 0.65

  Confetti Sky - Score: 1.00
  Because: Matches preferred genre: pop; Matches preferred mood: happy; Energy closeness: 0.98 (song 0.82, target 0.80); Tempo alignment: 0.71 (song 132, target 172); Valence match: 0.92 (song valence 0.77, target 0.85); Danceability match: 0.97 (song danceability 0.88, target 0.85); Prefers less acoustic songs: non-acoustic bonus 0.95

  Storm Runner - Score: 0.82
  Because: Genre similarity: 0.50 (preferred pop, song rock); Mood similarity: 0.80 (preferred happy, song intense); Energy closeness: 0.89 (song 0.91, target 0.80); Tempo alignment: 0.86 (song 152, target 172); Valence match: 0.63 (song valence 0.48, target 0.85); Danceability match: 0.81 (song danceability 0.66, target 0.85); Prefers less acoustic songs: non-acoustic bonus 0.90
  ```

  **Profile 2 — indie pop / chill / 0.4 (softer, low-energy user).** No song in the catalog is an exact indie pop + chill match, so the genre-similarity and mood-similarity fallbacks take over. The top results are jazz, synthwave, and lo-fi tracks that sit close to indie pop on the genre ordering and match the low target energy well — evidence the similarity fallback is doing its job rather than requiring exact matches.

  ```
  Top recommendations:

  Morning Ember - Score: 0.94
  Because: Genre similarity: 0.67 (preferred indie pop, song jazz); Matches preferred mood: chill; Energy closeness: 0.98 (song 0.42, target 0.40); Tempo alignment: 0.73 (song 78, target 116); Valence match: 0.91 (song valence 0.56, target 0.65); Danceability match: 0.98 (song danceability 0.62, target 0.60); Prefers less acoustic songs: non-acoustic bonus 0.29

  Night Drive Loop - Score: 0.92
  Because: Genre similarity: 0.83 (preferred indie pop, song synthwave); Mood similarity: 0.80 (preferred chill, song moody); Energy closeness: 0.65 (song 0.75, target 0.40); Tempo alignment: 0.96 (song 110, target 116); Valence match: 0.84 (song valence 0.49, target 0.65); Danceability match: 0.87 (song danceability 0.73, target 0.60); Prefers less acoustic songs: non-acoustic bonus 0.78

  Velvet Static - Score: 0.92
  Because: Genre similarity: 0.83 (preferred indie pop, song synthwave); Mood similarity: 0.80 (preferred chill, song moody); Energy closeness: 0.64 (song 0.76, target 0.40); Tempo alignment: 0.96 (song 110, target 116); Valence match: 0.84 (song valence 0.49, target 0.65); Danceability match: 0.87 (song danceability 0.73, target 0.60); Prefers less acoustic songs: non-acoustic bonus 0.78

  Coffee Shop Stories - Score: 0.88
  Because: Genre similarity: 0.67 (preferred indie pop, song jazz); Mood similarity: 0.80 (preferred chill, song relaxed); Energy closeness: 0.97 (song 0.37, target 0.40); Tempo alignment: 0.81 (song 90, target 116); Valence match: 0.94 (song valence 0.71, target 0.65); Danceability match: 0.94 (song danceability 0.54, target 0.60); Prefers less acoustic songs: non-acoustic bonus 0.11

  Midnight Coding - Score: 0.88
  Because: Genre similarity: 0.50 (preferred indie pop, song lofi); Matches preferred mood: chill; Energy closeness: 0.98 (song 0.42, target 0.40); Tempo alignment: 0.73 (song 78, target 116); Valence match: 0.91 (song valence 0.56, target 0.65); Danceability match: 0.98 (song danceability 0.62, target 0.60); Prefers less acoustic songs: non-acoustic bonus 0.29
  ```

  **Profile 3 — rock / intense / 0.9 (high-energy user).** The system picked `Storm Runner` first, tied with `Adrenaline Gate`, both perfect exact matches on genre and mood. The remaining slots keep other high-energy, high-danceability tracks nearby, showing the model behaves well when a user prefers stronger, louder music.

  ```
  Top recommendations:

  Storm Runner - Score: 1.00
  Because: Matches preferred genre: rock; Matches preferred mood: intense; Energy closeness: 0.99 (song 0.91, target 0.90); Tempo alignment: 0.76 (song 152, target 186); Valence match: 0.92 (song valence 0.48, target 0.40); Danceability match: 0.86 (song danceability 0.66, target 0.80); Prefers less acoustic songs: non-acoustic bonus 0.90

  Adrenaline Gate - Score: 1.00
  Because: Matches preferred genre: rock; Matches preferred mood: intense; Energy closeness: 0.97 (song 0.93, target 0.90); Tempo alignment: 0.76 (song 152, target 186); Valence match: 0.92 (song valence 0.48, target 0.40); Danceability match: 0.86 (song danceability 0.66, target 0.80); Prefers less acoustic songs: non-acoustic bonus 0.90

  Gym Hero - Score: 0.88
  Because: Genre similarity: 0.50 (preferred rock, song pop); Matches preferred mood: intense; Energy closeness: 0.97 (song 0.93, target 0.90); Tempo alignment: 0.61 (song 132, target 186); Valence match: 0.63 (song valence 0.77, target 0.40); Danceability match: 0.92 (song danceability 0.88, target 0.80); Prefers less acoustic songs: non-acoustic bonus 0.95

  Rooftop Lights - Score: 0.85
  Because: Genre similarity: 0.67 (preferred rock, song indie pop); Mood similarity: 0.80 (preferred intense, song happy); Energy closeness: 0.86 (song 0.76, target 0.90); Tempo alignment: 0.56 (song 124, target 186); Valence match: 0.59 (song valence 0.81, target 0.40); Danceability match: 0.98 (song danceability 0.82, target 0.80); Prefers less acoustic songs: non-acoustic bonus 0.65

  Confetti Sky - Score: 0.81
  Because: Genre similarity: 0.50 (preferred rock, song pop); Mood similarity: 0.80 (preferred intense, song happy); Energy closeness: 0.92 (song 0.82, target 0.90); Tempo alignment: 0.61 (song 132, target 186); Valence match: 0.63 (song valence 0.77, target 0.40); Danceability match: 0.92 (song danceability 0.88, target 0.80); Prefers less acoustic songs: non-acoustic bonus 0.95
  ```

  **Comparing the three:** the exact-match profiles (1 and 3) surface perfect-score songs and cluster tightly around the requested genre/mood, while the softer profile (2) has no perfect matches and instead leans on the similarity fallbacks and the low energy target to rank neighboring genres. This confirms the scorer degrades gracefully from exact matches to "nearby" recommendations rather than returning nothing when no perfect match exists.

---

## Limitations and Risks

Summarize some limitations of your recommender.

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood
- It does not include the list of songs (or artists) that the user would always prefer regardless of the mood or energy.
- The optimal valence, danceability and acousticness based on user's mood, preferred genre and energy are highly arbitrary.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

In this project, I learned that a recommender system is essentially a scoring process that turns structured data into predictions. The system takes a user profile and song metadata, applies a hand-designed rule to each candidate song, and then ranks the songs by how well they match the user’s preferences. This made it clear that recommendation is not simply about collecting data; it is about deciding which features matter most and how they should be combined.

I also saw how bias can appear even in a simple prototype. Because the scoring weights are fixed and the catalog is small, the model can overemphasize a few strong signals, such as genre or mood, which may make recommendations feel repetitive or unfair for users with mixed or changing tastes. This experience helped me understand why real recommendation systems need careful evaluation, more diverse data, and safeguards that reduce overfitting and narrow preference bias.



