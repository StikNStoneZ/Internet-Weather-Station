from googleapiclient.discovery import build
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")

def get_youtube_posts():

    if not API_KEY:
        print("No YouTube API key")
        return []

    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)

        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            maxResults=50,
            regionCode="IN"
        )

        response = request.execute()

        posts = []

        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            stats = item.get("statistics", {})

            title = snippet.get("title", "No title")

            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))
            views = int(stats.get("viewCount", 1))

            hype_score = (likes + comments) / views

            posts.append({
                "text": title,
                "likes": likes,
                "comments": comments,
                "views": views,
                "hype": hype_score
            })

        posts.sort(key=lambda x: x["hype"], reverse=True)

        return posts[:25]

    except Exception as e:
        print("YouTube failed:", e)
        return []