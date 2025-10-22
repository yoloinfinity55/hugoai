# HugoAI - YouTube to Hugo Content Pipeline

A fully automated system that converts YouTube videos into bilingual Hugo blog posts using AI.

## 🚀 Features

- **YouTube Integration**: Extract transcripts and metadata from YouTube videos
- **AI Content Generation**: Generate high-quality blog posts using Google Gemini AI
- **Bilingual Support**: Create content in English and Chinese simultaneously
- **Hugo Integration**: Seamlessly integrate with Hugo static site generator
- **GitHub Actions**: Automatic deployment to GitHub Pages
- **One-Click Processing**: Convert video to blog post in under 10 minutes

## 📋 Requirements

- Python 3.10+
- Hugo (latest version)
- Google Gemini API key
- Git

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yoloinfinity55/hugoai.git
   cd hugoai
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```

4. **Configure Hugo:**
   ```bash
   # Hugo should be installed via your package manager
   hugo version
   ```

## ⚙️ Configuration

Edit the `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
HUGO_CONTENT_DIR=content/posts
GIT_AUTHOR_NAME=Your Name
GIT_AUTHOR_EMAIL=your.email@example.com
GIT_REMOTE=origin
GIT_BRANCH=main
```

Edit `config.yaml` for Hugo settings:
```yaml
baseURL: "https://yourusername.github.io/hugoai/"
title: "Your Blog Title"
# ... other Hugo configuration
```

## 🎯 Usage

Process a YouTube video:
```bash
python3 hugo_manager.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --title "Blog Post Title" --author "Your Name"
```

Example:
```bash
python3 hugo_manager.py --url "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --title "Rick Astley - Never Gonna Give You Up" --author "Music Blogger"
```

## 🔄 Workflow

1. **Input**: YouTube URL and title
2. **Extract**: Fetch video transcript and metadata
3. **Generate**: Create English and Chinese blog posts using AI
4. **Build**: Hugo compiles the site
5. **Deploy**: GitHub Actions deploys to GitHub Pages

## 🌐 Deployment

The site automatically deploys to GitHub Pages when you push to the main branch.

To enable GitHub Pages:
1. Go to your repository settings
2. Navigate to "Pages"
3. Under "Source", select "GitHub Actions"
4. The site will be available at: `https://yourusername.github.io/hugoai/`

**Note**: The first deployment may take a few minutes. Check the "Actions" tab in your repository to monitor the deployment status.

## 📁 Project Structure

```
hugoai/
├── .github/workflows/     # GitHub Actions
├── archetypes/           # Hugo content templates
├── content/posts/        # Generated blog posts
├── public/              # Built Hugo site
├── config.yaml          # Hugo configuration
├── hugo_manager.py      # Main automation script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🤖 AI Models

- **Primary**: Google Gemini 2.0 Flash (fast, cost-effective)
- **Fallback**: Google Gemini 1.5 Pro (for complex content)

## 🌍 Multilingual Support

Currently supports:
- English (en)
- Chinese (zh)

Easy to extend to other languages by modifying the configuration.

## 📊 Performance

- **Processing Time**: < 10 minutes per video
- **Cost**: $0 (using Gemini free tier)
- **Output**: 4 pieces of content per video (2 blog posts + 2 social media posts)

## 🔧 Development

To modify the content generation prompts or add features:

1. Edit `hugo_manager.py`
2. Test locally: `python3 hugo_manager.py --url "..." --title "..." --author "..."`
3. Commit and push to trigger deployment

## 📝 License

MIT License - feel free to use and modify.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check the HugoAI specification document for detailed technical details

---

**Built with ❤️ using Hugo, Google Gemini AI, and GitHub Actions**
