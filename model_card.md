# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

This recommender suggests 5 songs from a small catalog based on a user's mood, genre, and audio preferences. It assumes the user can describe what they want like "I want chill lofi" or "I want intense rock." It is built for classroom exploration, not for real users.

---

## 3. How the Model Works

Every song in the catalog gets a score based on how closely it matches what the user wants. Mood is checked first. if a song matches your mood exactly, it gets a big bonus. Genre is checked next. Then numeric features like energy, acousticness, and danceability are compared, the closer the song's value is to what you want, the more points it earns. The song with the highest total score ranks first. No listening history is used, it only looks at your stated preferences.

---

## 4. Data

The catalog has 20 songs. It covers genres like lofi, pop, rock, metal, jazz, ambient, edm, r&b, country, folk, reggae, synthwave, hip-hop, darkwave, latin, and classical. Moods include chill, happy, intense, energetic, sad, angry, melancholic, focused, relaxed, moody, and nostalgic. No songs were added or removed. Genres like blues, soul, and bossa nova are missing entirely, so users with those tastes are not well served.

---

## 5. Strengths

The system works best when a user has a clear, consistent preference like someone who only wants lofi or only wants intense rock. The top results for those profiles matched what a real listener would expect. The scoring explanation also tells you exactly why each song was recommended, which makes it easy to understand and debug.

---

## 6. Limitations and Bias

The system ignores lyrics and listening context entirely, it only sees numbers. Genres like blues and soul don't exist in the catalog, so those users always get bad recommendations. Mood is weighted so heavily that it overrides everything else, which isn't always fair. Lofi users get better results simply because there are more lofi songs than any other genre in the catalog.

---

## 7. Evaluation

I tested six user profiles: three standard ones (High-Energy Pop, Chill Lofi, Deep Intense Rock) and three adversarial ones designed to confuse the system (conflicting energy+mood, all-zero features, mismatched genre+mood). For each profile I looked at whether the top 5 results matched what a real person with those preferences would actually want to listen to. The Chill Lofi profile felt the most accurate — the top 3 were all genuine lofi songs. What surprised me was that removing mood entirely caused classical music to appear in a lofi playlist, proving mood was the only thing keeping unrelated genres out. I also ran two experiments — doubling energy weight and commenting out mood — and compared the outputs to the original, which confirmed the original weights were already the most sensible version.

---

## 8. Future Work

It would help to add more songs so every genre has at least 3 or 4 options. A conflict penalty would improve results, right now a user asking for high energy and sad mood gets a mixed playlist because the system does not know those two signals disagree. Adding tempo as a stronger signal would also help users who specifically want slow or fast music. Longer term, using listening history instead of stated preferences would make recommendations feel more personal.

---

## 9. Personal Reflection

Building this made me realize how much work goes into something as simple as "here are 5 songs you might like." The hardest part was not the code, it was deciding how much each feature should matter. I was surprised that removing mood completely broke the system and let classical music appear in a lofi playlist. It changed how I think about Spotify and YouTube recommendations, those systems are doing the same basic thing, just with millions of songs and real listening data instead of 20 songs and manual preferences.
