import requests
from urllib.parse import urlparse, parse_qs

def download_thumbnail(video_url):
    try:
        # Extract video ID from the URL
        parsed_url = urlparse(video_url)
        video_id = parse_qs(parsed_url.query).get("v", [None])[0]
        
        if video_id:
            # Build the thumbnail URL
            thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            
            # Download the thumbnail
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                file_name = f"{video_id}_thumbnail.jpg"
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                return file_name
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error downloading thumbnail: {e}")
        return None
