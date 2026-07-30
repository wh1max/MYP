from flask import Flask, request, jsonify, render_template
from googleapiclient.discovery import build
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from flask import jsonify as flask_json
import random
import os



load_dotenv()
app = Flask(__name__)

youtube = build('youtube', 'v3', developerKey=os.environ.get('youtube_api_data_v3'))
ytt = YouTubeTranscriptApi()
languages = [
    "aa", "ab", "af", "am", "ar", "as", "ay", "az", "ba", "be", "bg", "bh", "bi", "bn", "bo", "br", "ca", "co", "cs", 
    "cy", "da", "de", "dz", "el", "en", "eo", "es", "et", "eu", "fa", "fi", "fj", "fo", "fr", "fy", "ga", "gd", "gl", 
    "gn", "gu", "ha", "hi", "he", "hr", "hu", "hy", "ia", "id", "ie", "ik", "in", "is", "it", "iu", "iw", "ja", "ji", 
    "jw", "ka", "kk", "kl", "km", "kn", "ko", "ks", "ku", "ky", "la", "ln", "lo", "lt", "lv", "mg", "mi", "mk", "ml", 
    "mn", "mo", "mr", "ms", "mt", "my", "na", "ne", "nl", "no", "oc", "om", "or", "pa", "pl", "ps", "pt", "qu", "rm", 
    "rn", "ro", "ru", "rw", "sa", "sd", "sg", "sh", "si", "sk", "sl", "sm", "sn", "so", "sq", "sr", "ss", "st", "su", 
    "sv", "sw", "ta", "te", "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "ts", "tt", "tw", "ug", "uk", "ur", "uz", 
    "vi", "vo", "wo", "xh", "yi", "yo", "za", "zh", "zu"
]

@app.route('/YTT', methods=['GET'])
def videoTranscription():
    textInput = request.args.get('t', '')
    transcribe_button = bool(textInput.strip())

    if transcribe_button:
        video_urls = [textInput]

        video_ids = [url.split('v=')[-1] for url in video_urls if 'v=' in url]

        if not video_ids:
            return "Invalid Youtube URL."

        video_id = video_ids[0]

        try:
            trnascribe = ytt.fetch(video_id=video_id, languages=languages)
        except Exception as e:
            return f"Error retrieving transcript: {e}"
    
        formatter = TextFormatter()
        Format_txt = formatter.format_transcript(trnascribe)

        filenumber = random.randint(1, 1000)
        saveNumber = str(filenumber)

        file_path = f'format_{video_id}_{saveNumber}.txt'
        try:
            with open(file_path, 'w', encoding='UTF-8') as text_file:
                text_file.write(Format_txt)
        except Exception as e:
            return f"Error: NO {file_path} Found! {e}"

        try:
            with open('file_tracker.txt', 'a', encoding='UTF-8') as tracker_file:
                tracker_file.write(f'FileNumber: {saveNumber}, VideoId: {video_id}, FileName: format_{video_id}_{saveNumber}.txt')
        except Exception as e:
            return f"Error: NO {file_path} Found! {e}"
                
        try:
            with open(file_path, 'r', encoding='UTF-8') as text_file:
                file_content = text_file.read()

        except Exception as e:
            return f"Error: {e}"

        return flask_json({
            "video_id": video_id,
            "file_number": saveNumber,
            "transcript": file_content
        })
    else:
        return jsonify({"message": "No URL provided. Use ?t=<youtube_url>"}), 400


@app.route('/MYP', methods=['GET'])
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
@app.route('/ytt', methods=['GET'])
def index():
    return render_template('ytt.html')

# TO DO: Manage created files by storing them into DropBox
if __name__ == '__main__':
    app.run(debug=True)



