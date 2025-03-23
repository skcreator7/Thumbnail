import requests

# Function to get the YouTube thumbnail from a video URL
def get_youtube_thumbnail(url: str) -> str:
    video_id = url.split("v=")[-1]  # Extract video ID from URL
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

# Function to download the YouTube thumbnail
def download_thumbnail(url: str) -> str:
    thumbnail_url = get_youtube_thumbnail(url)
    
    # Send back the thumbnail URL or download and save it to a local file
    response = requests.get(thumbnail_url)
    
    if response.status_code == 200:
        # Save the image locally if needed or return the URL to send directly
        file_name = "thumbnail.jpg"
        with open(file_name, "wb") as file:
            file.write(response.content)
        return file_name
    else:
        return None
