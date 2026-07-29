from flask import Flask, request, jsonify, render_template
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

youtube = build('youtube', 'v3', developerKey=os.environ.get('youtube_api_data_v3'))

@app.route('/test', methods=['GET'])
def test():
    user_input = request.args.get('q', '') # User input from the Search Box

    ## YouTube request
    req = youtube.search().list(
        part='snippet',
        q=user_input,
        type='video',
        maxResults=5,
        videoDuration='long',
        safeSearch='none',
        videoEmbeddable='true'
    ) 

    response = req.execute()

    # Transform into a simple list of dicts.
    videos = []
    for item in response.get('items', []):
        videos.append({
            'videoId': item['id']['videoId'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
        })

    # Print for debugging if you want.
    for v in videos:
        print(f"Title: {v['title']}\nVideo ID: {v['videoId']}\n")

    return jsonify(videos)

@app.route('/LoadVd', methods=['GET'])
def Load_video():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)



