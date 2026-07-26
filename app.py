from flask import Flask, request, jsonify
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

youtube = build('youtube', 'v3', developerKey=os.environ.get('youtube_api_data_v3'))

@app.route('/test', methods=['GET'])
def test():
    req = youtube.search().list(
        part='snippet',
        q='Python programming',
        type='video',
        maxResults=5,
        videoDuration='long',
        safeSearch='none'
    )

    response = req.execute()

    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        print(f'Title: {title}\nDescription: {description}\nVideo ID: {video_id}\n')

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)

# TO DO: Make the json data into a web page.