from googleapiclient.discovery import build

API_KEY = "AIzaSyD9FO-TGYGLnbGa8LPd53KapIS06OVZThE"


def get_youtube_posts():
    youtube = build("youtube", "v3", developerKey=API_KEY)

    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        maxResults=50,
        regionCode="IN"
    )

    response = request.execute()

    posts = []

    for item in response["items"]:
        title = item["snippet"]["title"]
        stats = item.get("statistics", {})

        likes = int(stats.get("likeCount", 0))
        comments = int(stats.get("commentCount", 0))
        views = int(stats.get("viewCount", 1))  # avoid division by 0

        hype_score = (likes + comments) / views

        posts.append({
            "text": title,
            "likes": likes,
            "comments": comments,
            "views": views,
            "hype": hype_score
        })

    # 🔥 SORT BY HYPE (NOT popularity)
    posts.sort(key=lambda x: x["hype"], reverse=True)

    # take top 25 hype videos
    return posts[:25]