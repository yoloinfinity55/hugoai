# HugoAI - YouTube to Hugo Content Pipeline

A fully automated system that converts YouTube videos into bilingual Hugo blog posts using AI.

## 🚀 Features

- **YouTube Integration**: Extract transcripts and metadata from YouTube videos
- **AI Content Generation**: Generate high-quality blog posts using Google Gemini AI
- **Bilingual Support**: Create content in English and Chinese simultaneously
- **Hugo Integration**: Seamlessly integrate with Hugo static site generator
- **GitHub Actions**: Automatic deployment to GitHub Pages
- **One-Click Processing**: Convert video to blog post in under 10 minutes
- **Modern Responsive Design**: Beautiful, mobile-first UI with grid layout
- **Robust Error Handling**: Comprehensive logging and retry mechanisms
- **Configurable Pipeline**: YAML-based configuration for easy customization

## 📋 Requirements

- Python 3.10+
- Hugo (latest version)
- Google Gemini API key
- Git

## 🛠️ Installation

### Quick Setup (Recommended)

For a complete setup on macOS (especially Mac Mini M1), run the automated setup script:

```bash
git clone https://github.com/yoloinfinity55/hugoai.git
cd hugoai
./setup.sh
```

This script will:
- Install Homebrew (if needed)
- Install Hugo and required dependencies
- Set up Python environment
- Configure environment variables
- Verify the installation

### Manual Setup

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

## 🌐 View Your Site

After deployment, your site will be available at:
- **Main Site**: https://yoloinfinity55.github.io/hugoai/
- **English Posts**: https://yoloinfinity55.github.io/hugoai/posts/
- **Chinese Posts**: https://yoloinfinity55.github.io/hugoai/zh/posts/

The homepage features:
- **Beautiful grid layout** displaying all blog posts as cards
- **Language filtering** (English/Chinese)
- **Responsive design** that works on all devices
- **Modern styling** with hover effects and smooth transitions
- **Navigation menu** with links to posts, tags, and categories

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
├── .github/workflows/     # GitHub Actions CI/CD
├── layouts/              # Custom Hugo templates
├── static/               # Static assets (CSS, images)
├── assets/               # Source assets (processed by Hugo)
├── archetypes/           # Hugo content templates
├── content/posts/        # Generated blog posts
├── public/              # Built Hugo site (auto-generated)
├── config.yaml          # Hugo configuration
├── hugo_manager.py      # Main automation script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🤖 AI Models

- **Primary**: Google Gemini 2.0 Flash Experimental (fast, cost-effective)
- **Note**: If Gemini API is not configured, the system generates placeholder content

## 🌍 Multilingual Support

Currently supports:
- English (en)
- Chinese (zh)

Easy to extend to other languages by modifying the configuration.

## 📊 Performance

- **Processing Time**: < 10 minutes per video
- **Cost**: Minimal (using Gemini free tier; additional usage may incur costs)
- **Output**: 2 bilingual blog posts per video (English and Chinese)

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

## 📋 Project Specification

### Architecture Overview

HugoAI is a comprehensive content pipeline that transforms YouTube videos into bilingual blog posts using AI. The system consists of several integrated components:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   YouTube API   │───▶│   AI Content    │───▶│   Hugo Site     │
│   (Transcripts) │    │   Generation    │    │   Generator     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   GitHub Pages  │
                       │   Deployment    │
                       └─────────────────┘
```

### Technical Stack

- **Frontend**: Hugo Static Site Generator
- **Backend**: Python 3.10+ with custom automation scripts
- **AI Engine**: Google Gemini 2.0 Flash Experimental
- **Video Processing**: yt-dlp for YouTube content extraction
- **Transcript API**: YouTube Transcript API
- **Deployment**: GitHub Actions CI/CD
- **Version Control**: Git with GitHub

### Core Components

#### 1. Content Pipeline (`hugo_manager.py`)
- **Language**: Python 3.10+
- **Dependencies**: See `requirements.txt`
- **Key Functions**:
  - `get_video_id()`: Extract YouTube video ID from URL
  - `fetch_transcript()`: Retrieve video transcript in English
  - `generate_with_gemini()`: Create bilingual blog posts using AI
  - `run_pipeline()`: Orchestrate the entire process
  - `git_commit_and_push()`: Version control integration

#### 2. Hugo Site Structure
- **Theme**: Custom responsive theme with grid layout
- **Layouts**:
  - `layouts/index.html`: Homepage with post grid and language filtering
  - `layouts/posts/single.html`: Individual blog post template
  - `layouts/_default/baseof.html`: Base template with header/footer
- **Assets**:
  - `assets/css/style.css`: Modern responsive CSS with mobile-first design
  - Grid system, hover effects, and smooth transitions

#### 3. Configuration Files
- **`config.yaml`**: Hugo site configuration with multilingual support
- **`.env`**: Environment variables for API keys and settings
- **`requirements.txt`**: Python dependencies with version constraints

### API Integrations

#### YouTube Integration
- **Library**: `youtube-transcript-api`
- **Functionality**: Automatic transcript extraction
- **Fallback**: Placeholder content if transcript unavailable
- **Video Support**: Standard videos and YouTube Shorts

#### Google Gemini AI
- **Model**: `gemini-2.0-flash-exp` (primary)
- **Features**:
  - Bilingual content generation (English + Chinese)
  - Structured markdown output with YAML front matter
  - Retry mechanism with exponential backoff
- **Rate Limiting**: Built-in retry logic for API failures
- **Cost**: Free tier available, usage-based pricing beyond limits

### Content Generation Process

1. **Input Validation**: URL format and accessibility check
2. **Transcript Extraction**: Fetch English transcript from YouTube
3. **AI Processing**: Generate content in both English and Chinese
4. **File Creation**: Create markdown files with Hugo front matter
5. **Site Building**: Hugo compilation with minification
6. **Version Control**: Automatic Git commit and push

### Multilingual Implementation

#### Language Support
- **English (en)**: Primary language with full feature support
- **Chinese (zh)**: Complete translation and localization
- **Extensibility**: Easy to add more languages via configuration

#### Content Structure
```
content/posts/
├── 2025-10-22-example-en-abc12345.md
└── 2025-10-22-example-zh-abc12345.md
```

Each post includes:
- YAML front matter with metadata
- Structured content with headings
- SEO-optimized descriptions
- Tag and category classification

### Deployment Architecture

#### GitHub Actions Workflow (`.github/workflows/deploy.yml`)
- **Trigger**: Push to main branch
- **Build Process**:
  1. Checkout repository with submodules
  2. Setup Hugo extended version
  3. Configure GitHub Pages
  4. Build site with minification
  5. Deploy to GitHub Pages
- **Permissions**: Contents read, Pages write, ID token write

#### Hosting
- **Platform**: GitHub Pages
- **Domain**: `https://username.github.io/hugoai/`
- **Performance**: Static hosting with CDN
- **SSL**: Automatic HTTPS via GitHub Pages

### Development Workflow

#### Local Development
1. **Setup**: Run `./setup.sh` for automated installation
2. **Testing**: Use sample YouTube URLs for development
3. **Building**: `hugo server` for local preview
4. **Content Creation**: `python3 hugo_manager.py --url "..." --title "..." --author "..."`

#### Code Quality
- **Linting**: Python code follows PEP 8 standards
- **Error Handling**: Comprehensive logging and user feedback
- **Testing**: Integration tests via Hugo build process

### Performance Metrics

- **Processing Time**: < 10 minutes per video
- **Build Time**: < 30 seconds for site generation
- **Deployment Time**: 2-3 minutes via GitHub Actions
- **Page Load**: Optimized static assets with compression

### Security Considerations

- **API Keys**: Stored in `.env` file (not committed to Git)
- **GitHub Tokens**: GitHub Actions use encrypted secrets
- **Content Validation**: Input sanitization for user-generated content
- **HTTPS**: All communications via secure protocols

### Extensibility

#### Adding New Features
1. **AI Prompts**: Modify `generate_with_gemini()` function
2. **Languages**: Update `config.yaml` and prompt templates
3. **Themes**: Customize Hugo layouts and CSS
4. **Integrations**: Add new APIs in `hugo_manager.py`

#### Configuration Options
- **Models**: Switch AI models via environment variables
- **Output**: Customize content structure and formatting
- **Deployment**: Modify GitHub Actions workflow

## 📋 Standard Operating Procedures (SOP)

### Content Creation Workflow

#### 1. Pre-Processing Checklist
- [ ] Verify YouTube video is public and accessible
- [ ] Check video duration (recommended: 5-30 minutes for optimal content)
- [ ] Ensure video has English transcript available
- [ ] Prepare compelling title and author information
- [ ] Confirm Gemini API key is valid and has quota remaining

#### 2. Content Generation Process
```bash
# Navigate to project directory
cd hugoai

# Run the content pipeline
python3 hugo_manager.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --title "Your Blog Post Title" --author "Author Name"

# Monitor the process
# - Transcript extraction (10-30 seconds)
# - AI content generation (2-5 minutes per language)
# - Hugo site build (30 seconds)
# - Git commit and push (1-2 minutes)
```

#### 3. Post-Processing Verification
- [ ] Check generated markdown files in `content/posts/`
- [ ] Verify YAML front matter is complete
- [ ] Review content quality and accuracy
- [ ] Test site build: `hugo --minify`
- [ ] Push to trigger deployment: `git push origin main`

### Operational Monitoring

#### Daily Operations
- [ ] Monitor GitHub Actions deployment status
- [ ] Check site accessibility at `https://yourusername.github.io/hugoai/`
- [ ] Review Gemini API usage and costs
- [ ] Verify new content appears on the site

#### Weekly Maintenance
- [ ] Review and update dependencies: `pip list --outdated`
- [ ] Check Hugo version: `hugo version`
- [ ] Test content pipeline with sample video
- [ ] Review site analytics and performance
- [ ] Backup configuration files

#### Monthly Reviews
- [ ] Analyze content engagement metrics
- [ ] Review and optimize AI prompts if needed
- [ ] Update project dependencies
- [ ] Test full deployment pipeline
- [ ] Document any issues or improvements

### Quality Assurance Procedures

#### Content Quality Checks
- [ ] **Accuracy**: Verify facts and information in generated content
- [ ] **Completeness**: Ensure all sections are present and coherent
- [ ] **SEO Optimization**: Check title, description, and tags
- [ ] **Language Quality**: Review both English and Chinese versions
- [ ] **Formatting**: Validate markdown syntax and Hugo front matter

#### Technical Quality Checks
- [ ] **Build Success**: Confirm Hugo builds without errors
- [ ] **Link Validation**: Test all internal and external links
- [ ] **Responsive Design**: Verify mobile compatibility
- [ ] **Performance**: Check page load times and image optimization
- [ ] **Accessibility**: Ensure WCAG compliance

### Troubleshooting Guide

#### Common Issues and Solutions

**1. YouTube Transcript Not Available**
```
Error: Transcript unavailable
Solution:
- Verify video has captions enabled
- Check if video is private or restricted
- Use videos with auto-generated captions
- Manually provide transcript if necessary
```

**2. Gemini API Errors**
```
Error: API quota exceeded or invalid key
Solution:
- Check API key in .env file
- Verify Gemini API quota and billing
- Implement retry logic (already built-in)
- Monitor usage in Google Cloud Console
```

**3. Hugo Build Failures**
```
Error: Build failed
Solution:
- Check markdown syntax in generated files
- Verify YAML front matter format
- Clear Hugo cache: hugo --cleanDestinationDir
- Update Hugo to latest version
```

**4. GitHub Pages Deployment Issues**
```
Error: Deployment failed
Solution:
- Check GitHub Actions logs
- Verify repository settings for Pages
- Confirm branch permissions
- Check DNS and SSL configuration
```

**5. Performance Issues**
```
Problem: Slow content generation
Solution:
- Check internet connection speed
- Monitor API response times
- Consider upgrading API quotas
- Optimize video selection (shorter videos process faster)
```

### Emergency Procedures

#### System Recovery
1. **Backup Current State**: `git add . && git commit -m "Backup before recovery"`
2. **Check Logs**: Review `hugo_manager.py` output and GitHub Actions logs
3. **Test Locally**: Run pipeline with known working video
4. **Restore from Backup**: If needed, revert to previous commit
5. **Contact Support**: Open GitHub issue with detailed error information

#### Data Recovery
- **Generated Content**: Stored in `content/posts/` directory
- **Configuration**: Backup `.env` and `config.yaml` files
- **Site Backup**: Download from GitHub Pages or local build
- **Git History**: Use `git log` to find previous working states

### Best Practices

#### Content Strategy
- **Video Selection**: Choose educational, informative content
- **Title Optimization**: Use descriptive, SEO-friendly titles
- **Author Consistency**: Maintain consistent author information
- **Publishing Schedule**: Regular content updates for better engagement

#### Technical Practices
- **Version Control**: Commit after each content generation
- **Environment Variables**: Never commit API keys to repository
- **Testing**: Always test locally before deploying
- **Monitoring**: Set up alerts for API usage and site availability

#### Security Practices
- **API Key Management**: Rotate keys regularly
- **Access Control**: Limit repository access to trusted users
- **Content Moderation**: Review generated content before publishing
- **Backup Strategy**: Regular backups of configuration and content

### Performance Optimization

#### Content Generation
- **Batch Processing**: Process multiple videos in sequence
- **API Optimization**: Use appropriate Gemini model for content type
- **Caching**: Implement transcript caching for repeated videos
- **Parallel Processing**: Consider concurrent language generation

#### Site Performance
- **Image Optimization**: Compress and resize images
- **CSS/JS Minification**: Use Hugo's built-in minification
- **CDN Integration**: Enable GitHub Pages CDN features
- **Caching Headers**: Configure appropriate cache policies

### Compliance and Legal

#### Content Guidelines
- [ ] Ensure YouTube videos are used in compliance with terms of service
- [ ] Respect copyright and fair use policies
- [ ] Provide proper attribution to original content creators
- [ ] Follow platform-specific content policies

#### Data Privacy
- [ ] No personal data collection or storage
- [ ] API usage complies with service terms
- [ ] Content generation respects intellectual property
- [ ] Transparent data usage in documentation

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check this specification for technical details

---

**Built with ❤️ using Hugo, Google Gemini AI, and GitHub Actions**
