#!/usr/bin/env python3
"""hugo_manager.py — YouTube → Hugo Content Pipeline (MVP)"""

import argparse, os, subprocess, sys, time, yaml, logging
from pathlib import Path
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

try:
    import google.generativeai as genai
except Exception:
    genai = None

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "hugo_content_dir": os.getenv("HUGO_CONTENT_DIR", "content/posts"),
    "gemini_model": os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp"),
}

def run_cmd(cmd, cwd=None, check=True):
    logger.info(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=check, capture_output=True, text=True)
        logger.info(f"Command succeeded: {result.returncode}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        logger.error(f"Stderr: {e.stderr}")
        raise

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
        return generate_dummy_content(title, lang, transcript)
    prompt = f"Generate a structured {lang} Hugo markdown blog post from the following transcript:\n\n{transcript}\n\nTitle: {title}\n\nRequirements:\n- Include YAML front matter with: title, date (use current date), description (compelling 150-160 char description), tags (relevant keywords), categories, draft: false\n- Write engaging, well-structured content in {lang}\n- Use proper markdown formatting with headings, paragraphs, lists\n- Keep the content concise but informative\n- End with a call to action"
    def call_api():
        response = genai.GenerativeModel(model).generate_content(prompt)
        return response.text if hasattr(response, 'text') else str(response)
    return retry_backoff(call_api, max_attempts=5, backoff_base=1.6)

def generate_dummy_content(title, lang, transcript):
    current_date = time.strftime('%Y-%m-%d')
    return f"""---
title: "{title}"
date: {current_date}
publishDate: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}
lastmod: {time.strftime('%Y-%m-%dT%H:%M:%S%z')}
tags: ["YouTube", "Transcript", "AI Generated"]
categories: ["Content"]
description: "AI-generated blog post from YouTube transcript - configure Gemini API for full content generation"
draft: false
---

# {title} ({lang})

This is a placeholder content generated because Gemini API is not configured.

## Transcript Snippet

{transcript[:400]}...

## Next Steps

Please configure the Gemini API to generate proper content. Add your API key to the .env file and install google-generativeai.
"""

def safe_filename(title, lang, vid):
    # Use current date for filename to avoid conflicts
    current_date = time.strftime('%Y-%m-%d')
    slug = "".join(c for c in title.lower().strip() if c.isalnum() or c in (' ', '-')).replace(' ', '-')
    return f"{current_date}-{slug}-{lang}-{vid[:8]}.md"

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

def load_config():
    config_path = Path('config.yaml')
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

def main():
    config = load_config()
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='YouTube video URL')
    parser.add_argument('--title', required=True, help='Post title')
    parser.add_argument('--author', default=os.getenv('GIT_AUTHOR_NAME', 'AutoBot'), help='Author name')
    parser.add_argument('--config', default='config.yaml', help='Config file path')
    args = parser.parse_args()

    # Override config with command line args
    config.update({
        'hugo_content_dir': os.getenv('HUGO_CONTENT_DIR', config.get('hugo_content_dir', 'content/posts')),
        'gemini_model': os.getenv('GEMINI_MODEL', config.get('gemini_model', 'gemini-2.0-flash-exp')),
    })

    try:
        run_pipeline(args.url, args.title, args.author)
        logger.info("Pipeline completed successfully")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
