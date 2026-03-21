import requests
import re

HEADERS = {
    "User-Agent": "internet-weather-station"
}


def clean_text(text):
    # remove links
    text = re.sub(r'http\S+', '', text)
    return text


def is_bot_comment(text):
    text = text.lower()

    bot_phrases = [
        "i am a bot",
        "this action was performed automatically",
        "moderators of this subreddit",
        "do not celebrate violence",
        "contact the moderators"
    ]

    return any(phrase in text for phrase in bot_phrases)


def get_comments(permalink):
    url = f"https://www.reddit.com{permalink}.json?limit=5"

    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        data = response.json()

        comments = []

        for c in data[1]["data"]["children"]:
            body = c["data"].get("body", "")

            if not body:
                continue

            if is_bot_comment(body):
                continue

            body = clean_text(body)

            comments.append(body)

            # limit to 3 good comments
            if len(comments) >= 3:
                break

        return " ".join(comments)

    except:
        return ""


def get_reddit_posts():
    url = "https://www.reddit.com/r/all/hot.json?limit=50"

    response = requests.get(url, headers=HEADERS, timeout=5)
    data = response.json()

    posts = []

    for i, post in enumerate(data["data"]["children"]):
        p = post["data"]

        title = p.get("title", "")
        body = p.get("selftext", "")
        permalink = p.get("permalink", "")

        title = clean_text(title)
        body = clean_text(body)

        # only fetch comments for first 10 posts (speed boost)
        if i < 10:
            comments_text = get_comments(permalink)
        else:
            comments_text = ""

        full_text = f"{title} {body} {comments_text}"

        posts.append({
            "text": full_text,
            "likes": p.get("score", 0),
            "comments": p.get("num_comments", 0)
        })

    return posts