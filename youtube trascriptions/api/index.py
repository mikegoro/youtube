import os
import re
from flask import Flask, request, jsonify, send_from_directory
from youtube_transcript_api import YouTubeTranscriptApi

# 1. ADJUSTED: Tell Flask the HTML is one folder up (in the root)
app = Flask(__name__, static_folder='../')

# YOUR WORKING ID EXTRACTOR (Kept exactly the same)
def extract_video_id(url):
    match = re.search(
        r"(?:youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})",
        url
    )
    return match.group(1) if match else None

@app.route('/')
def serve_frontend():
    # 2. ADJUSTED: Serve from the static_folder (the root)
    return send_from_directory(app.static_folder, 'index.html')

@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/api/transcript', methods=['GET'])
def get_transcript():
    url = request.args.get('url')
    if not url:
        return jsonify({"success": False, "error": "URL is required"}), 400
    
    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"success": False, "error": "Invalid YouTube URL"}), 400

    try:
        # YOUR WORKING INSTANCE LOGIC (Kept exactly the same)
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)

        plain_text = " ".join([item.text for item in transcript])
        
        formatted_list = []
        for item in transcript:
            start = getattr(item, 'start', 0)
            mins, secs = divmod(int(start), 60)
            formatted_list.append(f"[{mins:02d}:{secs:02d}] {item.text}")
            
        formatted_text = "\n".join(formatted_list)
        
        return jsonify({
            "success": True,
            "plain_text": plain_text,
            "formatted_text": formatted_text,
            "video_id": video_id
        })
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": f"YouTube Error: {str(e)}"
        }), 400

# 3. REMOVED: app.run() is deleted because Vercel handles the execution.