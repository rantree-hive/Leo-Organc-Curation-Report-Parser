import requests
import json
import time
import logging
import re
from collections import defaultdict
from datetime import datetime

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
            last_update = post.get("last_update", "")  # Extract last_update timestamp
            if author == "leo-curation" and permlink.startswith("organic-curation-report"):
                post_body = post.get("body", "")
                posts_list.append({"body": post_body, "last_update": last_update})
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error processing JSON or missing key: {e}")

    return posts_list

# Function to extract stats from post bodies
def extract_stats(posts):
    stats = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # {year_month: {curated_user: {curator: count}}}

    for post in posts:
        post_body = post["body"]
        last_update = post["last_update"]

        # Convert last_update to datetime and format as "YYYY-MM"
        try:
            date_obj = datetime.strptime(last_update, "%Y-%m-%dT%H:%M:%S")
            year_month = date_obj.strftime("%Y-%m")
        except ValueError as e:
            logger.error(f"Invalid timestamp format: {last_update}")
            continue

        # Regex to extract curated user and curator
        matches = re.findall(r"@(\w+)\s+\|.*\|\s+(\w+)", post_body)
        for curated_user, curator in matches:
            stats[year_month][curated_user][curator] += 1

    return stats

# Function to print stats ordered by the most curated users, grouped by month and year
def print_stats(stats):
    for year_month, user_stats in sorted(stats.items()):
        print(f"\nStats for {year_month}:")
        
        # Sort by total curations per user
        sorted_user_stats = sorted(
            user_stats.items(),
            key=lambda item: sum(item[1].values()),  # Total curations
            reverse=True
        )

        for curated_user, curators in sorted_user_stats:
            total_curations = sum(curators.values())
            curators_str = ", ".join(
                f"{count} by {curator}" for curator, count in curators.items()
            )
            print(f"  {curated_user} {total_curations} ({curators_str})")

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
    print(f"\nWork completed in {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()
