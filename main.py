from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Filly AI Motor V6 (YouTube & TikTok Fix) Online! 🚀"

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('link')
    
    if not video_url:
        return jsonify({"error": "Sem link"}), 400

    try:
        # Configurações Especiais de Camuflagem
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'cachedir': False,
            # Força IPv4 (Essencial para o Render não ser bloqueado)
            'source_address': '0.0.0.0',
            
            # Truques para enganar o YouTube e TikTok
            'extractor_args': {
                'youtube': {
                    # Fingimos ser um Android e um iPhone para passar sem login
                    'player_client': ['android', 'ios'],
                    'skip': ['dash', 'hls']
                },
                'tiktok': {
                    # Forçamos a versão da API móvel
                    'app_version': ['v1.0.0']
                }
            },
            
            # Cabeçalhos falsos de navegador
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            return jsonify({
                "status": "success",
                "title": info.get('title', 'Video'),
                "thumbnail": info.get('thumbnail', ''),
                "download_url": info.get('url'),
                "platform": info.get('extractor_key')
            })

    except Exception as e:
        error_msg = str(e)
        print(f"Erro: {error_msg}")
        
        if "Sign in" in error_msg:
            return jsonify({
                "error": "O YouTube está muito rigoroso hoje. Tenta outro vídeo ou usa TikTok/Insta!",
                "status": "failed"
            }), 500
        elif "TikTok" in error_msg:
             return jsonify({
                "error": "Erro no TikTok. Tenta novamente em 10 segundos.",
                "status": "failed"
            }), 500
            
        return jsonify({"error": "Link inválido ou privado.", "status": "failed"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
