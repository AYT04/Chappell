import os
import requests
import feedparser

def download_podcast_episodes(rss_url, download_dir):
    # Parse the RSS feed
    feed = feedparser.parse(rss_url)

    # Create the download directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Loop through each episode
    for entry in feed.entries:
        # Extract the episode title and media URL
        episode_title = entry.title
        media_url = entry.enclosures[0].href

        # Create a filename based on the episode title
        filename = os.path.join(download_dir, f"{episode_title}.mp3")

        # Download the episode
        print(f"Downloading {episode_title}...")
        response = requests.get(media_url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Downloaded {episode_title}")
        else:
            print(f"Failed to download {episode_title}")

if __name__ == "__main__":
    # Replace with the RSS feed URL of the podcast
    rss_url = "https://ohthatremindsmepod.podbean.com/feed.xml"
    # Replace with the directory where you want to save the episodes
    download_dir = "./oh"
    download_podcast_episodes(rss_url, download_dir)
