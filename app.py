from flask import Flask, render_template
import time
from fetch_reddit import get_reddit_posts
from fetch_youtube import get_youtube_posts
from fetch_trends import get_trending_searches

from analyze import analyze_posts
from weather import calculate_weather, process_trends

cache = {}
last_fetch = 0

app = Flask(__name__)

# ================= TOOLTIP INFO =================

def get_mood_info(mood):
    mapping = {
        "Calm": "Internet is peaceful. Nothing major happening.",
        "Mild Nonsense": "Light humor, memes, and casual chatter dominate.",
        "Slightly Heated": "Some debates and arguments are emerging.",
        "Chaotic": "Confusion, drama everywhere.",
        "Meltdown": "Internet is exploding with outrage or major events."
    }
    return mapping.get(mood, "Unknown mood.")


def get_heat_info(temp):
    if temp < 25:
        return "Low engagement. Content is not spreading much."
    elif temp < 30:
        return "Moderate activity. People interacting steadily."
    elif temp < 35:
        return "High engagement. Topics gaining traction."
    else:
        return "Viral explosion. Internet is on fire."


def get_momentum_info(momentum):
    mapping = {
        "Still Air": "Trends are stagnant.",
        "Light Drift": "Slow movement of topics.",
        "Moderate Spread": "Steady growth in trends.",
        "Strong Currents": "Fast-moving viral content.",
        "Storm Surge": "Explosive spread across platforms."
    }
    return mapping.get(momentum, "Unknown momentum.")


def get_tension_info(tension):
    mapping = {
        "Stable": "No major conflicts.",
        "Unstable": "Some disagreements rising.",
        "High": "Heavy arguments and controversy.",
        "Critical": "Internet-wide conflict."
    }
    return mapping.get(tension, "Unknown tension.")


def get_clarity_info(clarity):
    mapping = {
        "Clear": "Content is easy to understand.",
        "Foggy": "Mixed signals and confusion.",
        "Low Visibility": "Chaos or misinformation dominates."
    }
    return mapping.get(clarity, "Unknown clarity.")


# ================= MAIN ROUTE =================

@app.route("/")
def home():
    global cache, last_fetch

    # Refresh data every 30 seconds
    if time.time() - last_fetch > 30:

        try:
            # Reddit
            try:
                reddit_posts = get_reddit_posts()
            except Exception as e:
                print("Reddit failed:", e)
                reddit_posts = []

            # YouTube
            try:
                youtube_posts = get_youtube_posts()
            except Exception as e:
                print("YouTube failed:", e)
                youtube_posts = []

            # Combine
            all_posts = reddit_posts + youtube_posts

            # Analyze
            sentiments = analyze_posts(all_posts)

            # Weather
            weather = calculate_weather(sentiments, all_posts)

            # Save to cache
            cache = {
                "mood": weather.get("condition", "Unknown"),
                "temp": weather.get("temperature", 0),
                "momentum": weather.get("wind", "N/A"),
                "tension": weather.get("pressure", "N/A"),
                "clarity": weather.get("visibility", "N/A"),
            }

            last_fetch = time.time()

        except Exception as e:
            print("Main fetch failed:", e)
            # Keep old cache (important)

    # First run fallback
    if not cache:
        cache = {
            "mood": "Loading...",
            "temp": 0,
            "momentum": "N/A",
            "tension": "N/A",
            "clarity": "N/A",
        }

    return render_template("index.html", **cache)


# ================= DETAILS PAGE =================

@app.route("/details")
def details():
    reddit_posts = get_reddit_posts()
    youtube_posts = get_youtube_posts()

    reddit_sentiments = analyze_posts(reddit_posts)
    youtube_sentiments = analyze_posts(youtube_posts)

    reddit_weather = calculate_weather(reddit_sentiments, reddit_posts)
    youtube_weather = calculate_weather(youtube_sentiments, youtube_posts)

    # 🔥 Extract reddit values
    r_mood = reddit_weather["condition"]
    r_temp = reddit_weather["temperature"]
    r_momentum = reddit_weather["wind"]
    r_tension = reddit_weather["pressure"]
    r_clarity = reddit_weather["visibility"]

    # 🔥 Extract youtube values
    y_mood = youtube_weather["condition"]
    y_temp = youtube_weather["temperature"]
    y_momentum = youtube_weather["wind"]
    y_tension = youtube_weather["pressure"]
    y_clarity = youtube_weather["visibility"]

    return render_template(
        "details.html",

        # Reddit
        r_mood=r_mood,
        r_temp=r_temp,
        r_momentum=r_momentum,
        r_tension=r_tension,
        r_clarity=r_clarity,

        r_mood_info=get_mood_info(r_mood),
        r_heat_info=get_heat_info(r_temp),
        r_momentum_info=get_momentum_info(r_momentum),
        r_tension_info=get_tension_info(r_tension),
        r_clarity_info=get_clarity_info(r_clarity),

        # YouTube
        y_mood=y_mood,
        y_temp=y_temp,
        y_momentum=y_momentum,
        y_tension=y_tension,
        y_clarity=y_clarity,

        y_mood_info=get_mood_info(y_mood),
        y_heat_info=get_heat_info(y_temp),
        y_momentum_info=get_momentum_info(y_momentum),
        y_tension_info=get_tension_info(y_tension),
        y_clarity_info=get_clarity_info(y_clarity)
    )


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)