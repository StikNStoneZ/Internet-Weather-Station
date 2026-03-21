from fetch_reddit import get_reddit_posts
from fetch_youtube import get_youtube_posts
from fetch_trends import get_trending_searches

from analyze import analyze_posts
from weather import calculate_weather, process_trends


def display(title, weather):
    print(f"\n{title}")
    print("-" * len(title))
    print(f"Condition: {weather['condition']}")
    print(f"Temperature: {weather['temperature']}°C")
    print(f"Wind: {weather['wind']}")
    print(f"Pressure: {weather['pressure']}")
    print(f"Visibility: {weather['visibility']}")


def run():
    print("Fetching Reddit...")
    reddit_posts = get_reddit_posts()

    print("Fetching YouTube...")
    youtube_posts = get_youtube_posts()

    print("Fetching Google Trends...")
    trends = get_trending_searches()

    # --- Reddit Weather ---
    reddit_sentiments = analyze_posts(reddit_posts)
    reddit_weather = calculate_weather(reddit_sentiments, reddit_posts)

    # --- YouTube Weather ---
    youtube_sentiments = analyze_posts(youtube_posts)
    youtube_weather = calculate_weather(youtube_sentiments, youtube_posts)

    # --- Combined Weather ---
    all_posts = reddit_posts + youtube_posts
    all_sentiments = analyze_posts(all_posts)
    combined_weather = calculate_weather(all_sentiments, all_posts)

    # --- Trends Processing ---
    alert, forecast = process_trends(trends)

    print("\n🌐 Internet Weather Station\n")

    display("Reddit", reddit_weather)
    display("YouTube", youtube_weather)

    print("\nOverall Internet")
    print("----------------")
    print(f"Condition: {combined_weather['condition']}")
    print(f"Temperature: {combined_weather['temperature']}°C")
    print(f"Wind: {combined_weather['wind']}")
    print(f"Pressure: {combined_weather['pressure']}")
    print(f"Visibility: {combined_weather['visibility']}")

    # --- Trends Output ---
    if alert:
        print(f"\n⚠ Alert: {alert}")

    print(f"📈 Forecast: {forecast}")


run()