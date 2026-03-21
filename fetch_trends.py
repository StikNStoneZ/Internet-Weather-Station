import requests
import xml.etree.ElementTree as ET


def get_trending_searches():
    url = "https://trends.google.com/trending/rss?geo=IN"

    response = requests.get(url)

    root = ET.fromstring(response.content)

    trends = []

    for item in root.iter("item"):
        title = item.find("title").text

        trends.append({
            "text": title,
            "source": "trends"
        })

    return trends[:20]