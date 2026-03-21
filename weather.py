def calculate_weather(sentiments, posts):
    # --- Safety ---
    if not sentiments or not posts:
        return {
            "temperature": 0,
            "pressure": "Stable",
            "condition": "No Data",
            "wind": "Calm",
            "visibility": "Clear"
        }

    total_posts = len(sentiments)

    # --- 🌡 Temperature ---
    avg_sentiment = sum(sentiments) / total_posts
    temperature = (1 - avg_sentiment) * 30

    # --- 🌡 Pressure ---
    total_likes = sum(p["likes"] for p in posts)
    total_comments = sum(p["comments"] for p in posts)

    pressure_value = total_comments / (total_likes + 1)

    if pressure_value > 0.5:
        pressure = "High"
    elif pressure_value > 0.2:
        pressure = "Rising"
    else:
        pressure = "Stable"

    # --- 🌬 Wind ---
    avg_engagement = sum((p["likes"] + p["comments"]) for p in posts) / total_posts

    if avg_engagement > 10000:
        wind = "Strong Currents"
    elif avg_engagement > 3000:
        wind = "Moderate Spread"
    else:
        wind = "Slow Spread"

    # --- 🌫 Visibility ---
    confusion_keywords = [
        "what is happening",
        "is this real",
        "can someone explain",
        "wtf",
        "why is this"
    ]

    confusion_count = 0

    for p in posts:
        text = p["text"].lower()
        if any(k in text for k in confusion_keywords):
            confusion_count += 1

    if confusion_count > 10:
        visibility = "Poor"
    elif confusion_count > 5:
        visibility = "Hazy"
    else:
        visibility = "Clear"

    # --- 🔥 Drama ---
    extreme_count = sum(1 for s in sentiments if s > 0.6 or s < -0.6)
    drama_ratio = extreme_count / total_posts

    # --- ⚔️ Conflict ---
    positive = sum(1 for s in sentiments if s > 0.3)
    negative = sum(1 for s in sentiments if s < -0.3)
    conflict_ratio = min(positive, negative) / total_posts

    # --- 🌦 FINAL CONDITION ---
    if conflict_ratio > 0.35:
        condition = "Polarized Storm"
    elif drama_ratio > 0.4:
        condition = "Thunderstorms"
    elif drama_ratio > 0.25:
        condition = "Slightly Heated"
    elif avg_sentiment < -0.2:
        condition = "Scattered Arguments"
    elif avg_sentiment > 0.4:
        condition = "Clear Skies"
    else:
        condition = "Mild Nonsense"

    return {
        "temperature": round(temperature, 2),
        "pressure": pressure,
        "condition": condition,
        "wind": wind,
        "visibility": visibility
    }


def process_trends(trends):
    alert_keywords = [
        "earthquake", "war", "crash", "death",
        "attack", "flood", "fire", "breaking"
    ]

    hype_keywords = [
        "match", "final", "live", "release",
        "trailer", "vs", "results"
    ]

    alert = None
    hype_count = 0

    for t in trends:
        text = t["text"].lower()

        # detect major events
        if any(word in text for word in alert_keywords):
            alert = "⚠ Major Event Detected"

        # detect hype activity
        if any(word in text for word in hype_keywords):
            hype_count += 1

    # forecast logic
    if hype_count > 8:
        forecast = "High activity expected"
    elif hype_count > 4:
        forecast = "Moderate activity"
    else:
        forecast = "Stable"

    return alert, forecast