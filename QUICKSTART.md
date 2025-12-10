# 🚀 Quick Start Guide - AI Influencer Automation

## ⚡ 5-Minute Setup

### **Step 1: Get Your FREE Gemini API Key** (2 minutes)

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

### **Step 2: Setup Environment** (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env and paste your Gemini API key
# On Windows: notepad .env
# On Mac/Linux: nano .env
```

Your `.env` should look like:
```
GEMINI_API_KEY=AIzaSy...your_key_here
```

### **Step 3: Install Dependencies** (2 minutes)

```bash
pip install -r requirements.txt
```

### **Step 4: Run Your First Video!** (30 seconds)

```bash
python main.py --video-type short_form
```

That's it! Your first AI influencer video will be generated in `output/videos/`

---

## 🎯 What Just Happened?

The system just:
1. ✅ Analyzed trending topics using Gemini AI
2. ✅ Generated a viral-worthy script
3. ✅ Created professional voiceover
4. ✅ Generated a video (with or without avatar animation)
5. ✅ Optimized everything for SEO

**All using FREE services!**

---

## 📹 Your First Video

Check these files:
- **Video**: `output/videos/simple_short_form_YYYYMMDD_HHMMSS.mp4`
- **Audio**: `output/audio/audio_short_form_YYYYMMDD_HHMMSS.mp3`
- **Metadata**: `output/logs/metadata_short_form_YYYYMMDD_HHMMSS.json`

---

## 🎨 Customize Your Influencer

Edit `config/influencer_config.json`:

```json
{
  "influencer": {
    "name": "Your Name Here",
    "niche": "Your Niche (e.g., Fitness, Cooking, Tech)",
    "content_style": "Your Style (e.g., Funny, Educational)"
  }
}
```

Then run again:
```bash
python main.py
```

---

## 🚀 Next Steps

### **Add Avatar Animation** (Optional but Recommended)

For talking-head videos with facial animation:

1. **Setup SadTalker**:
```bash
# Clone SadTalker
git clone https://github.com/OpenTalker/SadTalker.git tools/SadTalker

# Install dependencies
cd tools/SadTalker
pip install -r requirements.txt

# Download models (this may take a while)
bash scripts/download_models.sh
```

2. **Add your avatar image**:
   - Place your AI influencer image as `test_character.png`
   - Or update the path in `config/influencer_config.json`

3. **Run with avatar**:
```bash
python main.py
```

Now you'll get fully animated talking-head videos! 🎭

---

### **Deploy to Google Colab** (Recommended for Daily Automation)

1. **Upload to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ai_influencer.git
git push -u origin main
```

2. **Open in Colab**:
   - Go to: https://colab.research.google.com/
   - File → Open Notebook → GitHub
   - Enter your repository URL
   - Open `notebooks/colab_setup.ipynb`

3. **Set Secrets in Colab**:
   - Click the key icon (🔑) in left sidebar
   - Add `GEMINI_API_KEY`
   - Run all cells!

4. **Schedule Daily Runs**:
   - Use GitHub Actions (see `.github/workflows/` in gemini-youtube-automation)
   - Or use Colab's scheduling features

---

## 💡 Pro Tips

### **Generate Both Long and Short Videos**
```bash
python main.py --video-type both
```

### **Test Without Publishing**
```bash
python main.py --test
```

### **Use Better Voice Quality** (Optional - Paid)

Add to `.env`:
```bash
ELEVENLABS_API_KEY=your_elevenlabs_key
```

Then the system will use ElevenLabs instead of gTTS for better voice quality.

---

## 🎯 Daily Workflow

Once set up, your daily workflow is:

```bash
# Option 1: Run locally
python main.py

# Option 2: Run on Colab (automated)
# Just let GitHub Actions run daily!
```

That's it! The system handles everything else.

---

## 📊 Expected Output

### **Long-Form Video** (5-10 minutes)
- Educational content
- Multiple sections
- SEO-optimized
- Ready for YouTube

### **Short-Form Video** (30-60 seconds)
- Quick tips
- Viral-worthy hooks
- Optimized for TikTok/Instagram/YouTube Shorts

---

## 🆘 Troubleshooting

### **"GEMINI_API_KEY not found"**
- Make sure you created `.env` file
- Check that your API key is correct
- Try: `export GEMINI_API_KEY=your_key` (Mac/Linux)

### **"SadTalker not available"**
- This is OK! The system will create simple videos without avatar animation
- To enable avatar: Follow "Add Avatar Animation" steps above

### **"MoviePy error"**
- Install ffmpeg: 
  - Windows: `choco install ffmpeg`
  - Mac: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`

### **"Pexels API error"**
- Pexels is optional
- Get free API key: https://www.pexels.com/api/
- Add to `.env`: `PEXELS_API_KEY=your_key`

---

## 📚 Learn More

- **Full Documentation**: See [README_NEW.md](README_NEW.md)
- **Integration Details**: See [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- **Project Analysis**: See [github_projects_analysis.md](github_projects_analysis.md)

---

## 🎉 Success!

You now have a fully automated AI influencer system running on **$0/month**!

**What's Next?**
1. Generate your first 10 videos
2. Analyze what works
3. Optimize your content strategy
4. Scale to daily automation
5. Start growing your audience!

---

**Questions? Issues? Feedback?**

Open an issue on GitHub or check the documentation.

**Happy content creating! 🚀**
