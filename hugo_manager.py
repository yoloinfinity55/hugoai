#!/usr/bin/env python3
"""hugo_manager.py — YouTube → Hugo Content Pipeline (MVP)"""

import argparse, os, subprocess, sys, time, yaml
from pathlib import Path
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

try:
    import google.generativeai as genai
except Exception:
    genai = None

load_dotenv()

DEFAULT_CONFIG = {
    "hugo_content_dir": os.getenv("HUGO_CONTENT_DIR", "content/posts"),
    "gemini_model": os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp"),
}

def run_cmd(cmd, cwd=None, check=True):
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=cwd, check=check)

def get_video_id(url: str) -> str:
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    if "/shorts/" in url:
        return url.split("shorts/")[-1].split("?")[0]
    if url.endswith("/"):
        url = url[:-1]
    return url.split("/")[-1]

def fetch_transcript(video_url: str) -> str:
    vid = get_video_id(video_url)
    print(f"Fetching transcript for {vid}")
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(vid)
        transcript = transcript_list.find_transcript(['en'])
        fetched = transcript.fetch()
        text = "\n".join(seg['text'] for seg in fetched)
        return text
    except Exception as e:
        print("Transcript unavailable:", e)
        return "[TRANSCRIPT PLACEHOLDER - manual input required]"

def init_genai(api_key):
    if genai is None:
        print("google-generativeai not installed.")
        return False
    genai.configure(api_key=api_key)
    return True

def retry_backoff(func, *args, max_attempts=4, backoff_base=1.5, **kwargs):
    attempt = 0
    while True:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            attempt += 1
            if attempt >= max_attempts:
                raise
            wait = backoff_base ** attempt
            print(f"Retry {attempt}/{max_attempts} in {wait:.1f}s: {e}")
            time.sleep(wait)

def generate_with_gemini(transcript, title, lang='en', model=None):
    model = model or DEFAULT_CONFIG['gemini_model']
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or genai is None:
        print("Gemini API not configured; returning dummy content")
        return f"# {title} ({lang})\n\nTranscript snippet:\n{transcript[:400]}"
    prompt = f"Generate a structured {lang} Hugo markdown blog post from transcript:\n{transcript}\nTitle: {title}"
    def call_api():
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    return retry_backoff(call_api, max_attempts=5, backoff_base=1.6)

def safe_filename(title, lang, vid):
    slug = "-".join(title.lower().strip().split())
    return f"{time.strftime('%Y-%m-%d')}-{slug}-{lang}-{vid[:8]}.md"

def write_markdown(content, out_dir, filename):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    path = Path(out_dir) / filename
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Wrote {path}")
    return path

def local_hugo_build():
    run_cmd(["hugo", "--minify"])

def git_commit_and_push(message, author, email, remote='origin', branch='main'):
    run_cmd(["git", "add", "-A"])
    run_cmd(["git", "commit", "-m", message, "--author", f"{author} <{email}>"])
    run_cmd(["git", "push", remote, branch])

def run_pipeline(url, title, author):
    vid = get_video_id(url)
    transcript = fetch_transcript(url)
    init_genai(os.getenv('GEMINI_API_KEY'))
    en_md = generate_with_gemini(transcript, title, 'en')
    zh_md = generate_with_gemini(transcript, title, 'zh')
    out_dir = os.getenv('HUGO_CONTENT_DIR', DEFAULT_CONFIG['hugo_content_dir'])
    en_file = safe_filename(title, 'en', vid)
    zh_file = safe_filename(title, 'zh', vid)
    write_markdown(en_md, out_dir, en_file)
    write_markdown(zh_md, out_dir, zh_file)
    local_hugo_build()
    git_commit_and_push(f"Add posts for {vid}", author, os.getenv('GIT_AUTHOR_EMAIL', author))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--author', default=os.getenv('GIT_AUTHOR_NAME', 'AutoBot'))
    args = parser.parse_args()
    run_pipeline(args.url, args.title, args.author)

if __name__ == '__main__':
    main()
