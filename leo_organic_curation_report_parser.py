import requests
import json
import time
import logging
import re
from collections import defaultdict
#Script created to parse curation reports provided by inleo. This case just to provide some reports
#From their organic curation
#by @gwajnberg


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to fetch posts
def get_posts(session):
    posts_list = []
    url = "https://api.hive.blog"  # Replace with the actual API endpoint for fetching posts

    # Define the request payload
    payload = {
        "jsonrpc": "2.0",
        "method": "condenser_api.get_discussions_by_blog",
        "params": {"tag": "leo-curation", "limit": 100},
        "id": 1,
    }

    try:
        response = session.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        posts = data["result"]

        for post in posts:
            author = post["author"]
            permlink = post["permlink"]
            if author == "leo-curation" and permlink.startswith("organic-curation-report"):
                post_body = post.get("body", "")
                posts_list.append(post_body)
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error processing JSON or missing key: {e}")

    return posts_list

# Function to extract stats from post bodies
def extract_stats(posts):
    stats = defaultdict(lambda: defaultdict(int))  # {curated_user: {curator: count}}

    for post_body in posts:
        # Regex to extract curated user and curator
        matches = re.findall(r"@(\w+)\s+\|.*\|\s+(\w+)", post_body)
        for curated_user, curator in matches:
            stats[curated_user][curator] += 1

    return stats

# Function to print stats ordered by the most curated users
def print_stats(stats):
    # Create a list of tuples with total curation count and user stats
    sorted_stats = sorted(
        stats.items(),
        key=lambda item: sum(item[1].values()),  # Total curations
        reverse=True
    )

    for curated_user, curators in sorted_stats:
        total_curations = sum(curators.values())
        curators_str = ", ".join(
            f"{count} by {curator}" for curator, count in curators.items()
        )
        print(f"{curated_user} {total_curations} ({curators_str})")

def main():
    start = time.time()

    try:
        with requests.Session() as session:
            posts = get_posts(session)
            stats = extract_stats(posts)
            print_stats(stats)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    elapsed_time = time.time() - start
    print(f"Work completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
