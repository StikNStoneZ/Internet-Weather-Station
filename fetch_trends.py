import requests
import xml.etree.ElementTree as ET

def get_trending_searches():
    url = "https://trends.google.com/trending/rss?geo=IN"

    try:
        response = requests.get(url, timeout=5)

        # if request fails
        if response.status_code != 200:
            print("Trends HTTP error:", response.status_code)
            return []

        root = ET.fromstring(response.content)

        trends = []

        for item in root.iter("item"):
            title = item.find("title")

            if title is not None:
                trends.append({
                    "text": title.text,
                    "source": "trends"
                })

        return trends[:20]

    except Exception as e:
        print("Trends failed:", e)
        return []