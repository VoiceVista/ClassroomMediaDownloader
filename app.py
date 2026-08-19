import gradio as gr
import yt_dlp
import os
import re

def clean_youtube_url(url):
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
    if video_id_match:
        return f"https://www.youtube.com/watch?v={video_id_match.group(1)}"
    return url

def download_youtube_video(url):
    if not url:
        return None, "Please provide a valid link."
    
    clean_url = clean_youtube_url(url.strip())
    
    # Locate cookie file automatically
    cookie_file = None
    for filename in ['cookies.txt', 'cookies.txt.txt', 'cookies', 'www.youtube.com_cookies.txt']:
        if os.path.exists(filename):
            cookie_file = filename
            break

    ydl_opts = {
        # Fallback format string to catch any available stream (MP4/WebM/Single-file)
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        # Allow multi-client rotation so a stream is always found
        'extractor_args': {
            'youtube': {
                'player_client': ['mweb', 'ios', 'android', 'web']
            }
        }
    }
    
    if cookie_file:
        ydl_opts['cookiefile'] = cookie_file

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(clean_url, download=True)
            file_path = ydl.prepare_filename(info)
            
        return file_path, "Downloaded successfully!"
    except Exception as e:
        return None, f"Error: {str(e)}"

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,300;1,500;1,700&display=swap');

body, .gradio-container {
    background-color: #171010 !important;
    background-image: linear-gradient(180deg, #1f1414 0%, #110c0c 100%) !important;
    font-family: 'Cormorant Garamond', serif !important;
    color: #f3dfcd !important;
    padding-top: 40px !important;
}

.for-teacher-family {
    text-align: center;
    color: #f3dfcd !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 3.5rem !important;
    font-weight: 300 !important;
    font-style: italic !important;
    margin-top: 10px;
    margin-bottom: 30px;
    letter-spacing: -1px;
    line-height: 1.1;
    text-shadow: 0px 2px 4px rgba(0,0,0,0.5);
}

button.primary {
    background: linear-gradient(135deg, #c5a07c 0%, #a07a50 100%) !important;
    color: #171010 !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    font-family: 'Cormorant Garamond', serif !important;
    border: 1px solid #a07a50 !important;
    border-radius: 4px !important;
    padding: 14px 28px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase;
}

button.primary:hover {
    background: linear-gradient(135deg, #e1c09d 0%, #c5a07c 100%) !important;
    box-shadow: 0px 4px 10px rgba(197, 160, 124, 0.3);
}

input[type="text"] {
    background-color: #1f1414 !important;
    border: 1px solid #443535 !important;
    color: #f3dfcd !important;
    border-radius: 4px !important;
    font-size: 1rem !important;
}

.output-file {
    background-color: #1f1414 !important;
    border: 1px solid #a07a50 !important;
    color: #a07a50 !important;
}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Base()) as demo:
    gr.HTML("<div class='for-teacher-family'>For Teacher's Family</div>")
    
    with gr.Row():
        with gr.Column(scale=2):
            url_input = gr.Textbox(
                label="YouTube URL",
                placeholder="Paste link here...",
                interactive=True
            )
            download_btn = gr.Button("Download", variant="primary")
        
        with gr.Column(scale=1):
            file_output = gr.File(label="Download File", elem_classes=["output-file"])
            status_output = gr.Textbox(label="Status", interactive=False)
            
    download_btn.click(
        fn=download_youtube_video,
        inputs=[url_input],
        outputs=[file_output, status_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
