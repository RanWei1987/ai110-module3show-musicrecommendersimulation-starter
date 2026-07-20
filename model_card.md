# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
Based on the user profile, it generates a list of top 5 songs that may fit the user's preference. The song's name, score (describing how closely the sone matches the user profile), and explanation on why the sone matches the user

- What assumptions does it make about the user  
It assumes the user only has these favorate genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop.
It assumes the user only has these moods: happy, chill, intense, relaxed, moody, focused
It assumes the user's energy can be described as a float number varying from 0 to 1, while 1 means fully energetic.
- Is this for real users or classroom exploration  
This is just a prototype for clasroom explaration

---

## 3. How the Model Works  

The recommender uses a weighted scoring rule that combines the song metadata already present in the catalog.  

Functions involved in this part of the system:

- `score_song(user_prefs, song)` — computes the numeric score for one song based on the user profile.
- `recommend_songs(user_prefs, songs, k=5)` — applies the scoring function to the catalog and returns a ranked list.
- `Recommender.recommend(user, k=5)` — object-oriented wrapper that ranks the songs stored in the `Recommender` instance.
- `Recommender.explain_recommendation(user, song)` — turns the score into a human-readable explanation.

- The main features used are: `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`.
- The user profile contributes four signals: `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`.
- First, the system checks whether the song matches the preferred genre and mood exactly. If not, it falls back to a small similarity score based on ordered genre and mood patterns.
- Next, it rewards songs whose `energy` is close to the user's target energy.
- Then it uses a simple tempo alignment heuristic: songs with a tempo near the target implied by the energy level are preferred.
- After that, the score incorporates `valence` and `danceability` as softer mood-related bonuses, and finally rewards or penalizes `acousticness` based on whether the user likes acoustic songs.

The scoring is intentionally simple and explainable, so the output can be understood by reading the reasons attached to each recommendation.

In implementation terms, the score is computed as a weighted sum:

```math
\mathrm{score}
=
0.40 \cdot \mathrm{genre\_match}
+ 0.30 \cdot \mathrm{mood\_match}
+ 0.20 \cdot \mathrm{energy\_similarity}
+ 0.10 \cdot \mathrm{tempo\_similarity}
+ 0.05 \cdot \mathrm{valence\_similarity}
+ 0.05 \cdot \mathrm{danceability\_similarity}
+ 0.05 \cdot \mathrm{acoustic\_preference}
```

where the final value is clipped to the range $[0,1]$.  
- `genre_match` and `mood_match` are exact matches when possible, otherwise they fall back to a similarity score.
- `energy_similarity = 1 - |\text{song.energy} - \text{target_energy}|`
- `tempo_similarity` measures closeness to a tempo target inferred from the user’s energy preference.
- `acoustic_preference` rewards high `acousticness` if the user likes acoustic songs, otherwise it rewards low `acousticness`.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog 
There are 10 songs in the catalog
- What genres or moods are represented  
Genres: rock, synthwave, indie pop, pop, jazz, lofi, ambient;  
Moods: intense, happy, focused, moody, chill, relaxed.
- Did you add or remove data  
No
- Are there parts of musical taste missing in the dataset  
There are, but this is just a prototype here. 
---

## 5. Strengths  

The system works well when the user has a clear and stable taste profile, especially for genre and mood preferences.  

It gives intuitive results for profiles such as `pop + happy + high energy`, where the top recommendation clearly aligns with the user’s stated tastes. The scoring is also easy to explain because each result comes with a short reason string, which makes the system more transparent than a black-box ranking.  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

- Features it does not consider  
The system does not consider lyrics, artist popularity, listening history, or broader cultural context. It only uses the metadata in the small catalog and therefore cannot understand deeper reasons why a user might like a song.
- Genres or moods that are underrepresented  
Genres such as synthwave and ambient are underrepresented in the catalog, so the recommender has fewer examples to learn from for those styles. Moods like happy, relaxed, and focused are also less frequently represented, which may make recommendations for those profiles less diverse.
- Cases where the system overfits to one preference  
The model can overfit to one strong preference when the user profile is very narrow. For example, if a user strongly prefers `pop` and `happy`, the system may keep ranking other pop songs highly even when a slightly different genre such as `indie pop` would be a better fit for the user’s overall mood and energy.
- Ways the scoring might unintentionally favor some users  
Because genre and mood are weighted heavily, users with very clear, narrow preferences are likely to get more consistent recommendations than users with mixed or changing tastes. This can unintentionally favor users whose taste profile matches the small catalog well, while making other users appear less satisfied.

---

## 7. Evaluation  

I tested three representative profiles against the dataset:

- `pop / happy / energy=0.8 / likes_acoustic=False`
- `lofi / chill / energy=0.4 / likes_acoustic=True`
- `rock / intense / energy=0.9 / likes_acoustic=False`

For each profile, I checked whether the top-ranked songs matched the intended emotional and sonic profile of the user. The results were sensible: the happy, high-energy pop profile ranked upbeat songs first; the chill acoustic profile pushed toward low-energy, acoustic tracks; and the intense rock profile favored energetic, non-acoustic songs.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

- Additional features or preferences  
A natural next step would be to add more realistic features such as listening history, artist familiarity, or user-defined preferences for tempo, language, and era. This would make the recommender better reflect how real music services model taste over time.
- Better ways to explain recommendations  
The current explanation strings are useful, but they could be improved with clearer, user-facing language such as “This song matches your preferred genre and energy level” instead of the raw scoring reasons. A richer explanation could also mention trade-offs between features when a song is only a partial match.
- Improving diversity among the top results  
The current ranking can become repetitive when the user profile is narrow. A future version could include a diversity penalty so that the top recommendations do not all come from the same genre or mood cluster, which would make the output feel less repetitive and more balanced.
- Handling more complex user tastes  
A more advanced version could support mixed-preference users, such as someone who likes both energetic pop and relaxed jazz. That would require a more flexible profile representation, perhaps with multiple weighted preferences or a balanced “taste vector” rather than a single dominant genre and mood.

---

## 9. Personal Reflection  

A few sentences about your experience.  

- What you learned about recommender systems  
I learned that the core of a recommender system is its scoring function: it takes user features as input, evaluates candidate items in the catalog, and returns the item with the highest matching score. For a developer, one of the most important decisions is choosing which user and item features should be included in that scoring function and how much each one should matter.
- Something unexpected or interesting you discovered  
I found that a simple weighted sum of feature matches is often enough for a prototype recommender. The initial weights are usually chosen heuristically, and then refined based on whether the outputs seem sensible. I had expected a more complicated decision process, but the system became much easier to understand once I saw how the weights and feature choices shaped the ranking.
- How this changed the way you think about music recommendation apps  
I originally expected that many song features would need to be used in the recommendation score. In practice, however, only a small number of strong signals often matter most. That made me realize that music recommendation systems can be both explainable and effective even when they rely on a relatively simple scoring rule.

