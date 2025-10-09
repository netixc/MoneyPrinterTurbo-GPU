# TikTok/Douyin Integration

## 🎉 FREE Douyin Video Search - No Payment Required!

MoneyPrinterTurbo now includes **100% FREE Douyin keyword search** using direct API calls with A-Bogus encryption. No TikHub subscription or payment needed!

## Overview

This integration allows you to search and download videos from Douyin/TikTok platforms for your automated video generation.

**Features:**
- ✅ **FREE keyword search** for Douyin videos (no payment required!)
- ✅ Direct API integration with Douyin's search endpoint
- ✅ A-Bogus encryption built-in
- ✅ Optional TikHub API support for advanced features
- ✅ Video filtering by duration and aspect ratio

## ⚠️ Important Legal Notice

**Using TikTok/Douyin videos in your projects may violate:**
- TikTok/Douyin Terms of Service
- Copyright laws (videos belong to individual creators)
- Commercial use restrictions

**This feature is provided for educational/research purposes only. Use at your own risk.**

## Configuration

Edit your `config.toml` file:

```toml
[app]
# Set video source to "douyin" for free search
video_source = "douyin"

########## TikTok/Douyin Settings
# Option 1: FREE Direct Douyin Search (Recommended - No Payment!)
use_tikhub_api = false
tiktok_platform = "douyin"

# Option 2: TikHub API (Paid Service for Advanced Features)
use_tikhub_api = true
tikhub_api_key = "YOUR_TIKHUB_API_KEY"
tikhub_api_base = "https://api.tikhub.io"
```

## API Options

### 1. FREE Direct Douyin Search (Recommended!) 🆓

**Features:**
- ✅ **100% FREE** - No payment or subscription required!
- ✅ **Full keyword search** functionality
- ✅ Direct Douyin API integration
- ✅ A-Bogus encryption built-in
- ✅ No cookie management needed
- ✅ Video filtering by duration

**Setup:**
1. Set `use_tikhub_api = false` in config
2. Set `video_source = "douyin"`
3. Set `tiktok_platform = "douyin"`
4. **That's it!** Start generating videos immediately!

**How it works:**
- Calls Douyin's official VIDEO_SEARCH API directly
- Generates required A-Bogus encryption parameters
- Returns real video search results with download URLs
- Based on the open-source Douyin_TikTok_Download_API project

**Example:**
```python
from app.services.tiktok_crawler import TikTokCrawler

crawler = TikTokCrawler()
videos = crawler.search_videos_by_keyword("美食", count=10, platform="douyin")
# Returns 10 food-related videos instantly - FREE!
```

### 2. TikHub API (Optional - For Advanced Features)

**Features:**
- ✅ TikTok international support
- ✅ 700+ endpoints
- ✅ 14+ social platforms
- ✅ Enterprise-grade reliability

**Setup:**
1. Register at [https://tikhub.io/](https://tikhub.io/)
2. Get your API key
3. Set `use_tikhub_api = true` in config
4. Add your `tikhub_api_key`

**Pricing:** Pay-as-you-go (check TikHub website for current rates)

## Usage

### Via API

```bash
curl -X POST http://localhost:8080/api/v1/video \
  -H "Content-Type: application/json" \
  -d '{
    "video_subject": "Beautiful sunset",
    "video_source": "tiktok",
    "video_aspect": "9:16"
  }'
```

### Via WebUI

1. Open http://localhost:8501
2. Select "TikTok" or "Douyin" as video source
3. Enter your video subject
4. Generate

## How It Works

1. **Search**: Keywords are sent to TikHub API or douyin.wtf
2. **Filter**: Videos are filtered by duration and aspect ratio
3. **Download**: Videos are downloaded without watermarks
4. **Process**: Videos are combined with your script/audio

## File Structure

```
app/services/
├── tiktok_crawler.py      # TikTok/Douyin API wrapper
└── material.py            # Updated with search_videos_tiktok()

config.example.toml         # Configuration template
```

## Troubleshooting

### "TikHub API error"
- Check your API key is correct
- Verify you have credits in your TikHub account
- Check TikHub service status

### "douyin.wtf API does not support keyword search"
- This is expected with the free API
- Either enable TikHub API or provide specific URLs
- Consider using Pexels/Pixabay for stock footage instead

### "Failed to download video"
- Check your internet connection
- Verify proxy settings if using one
- The video may be region-restricted

## Alternative: Legal Stock Video Sources

For production use, consider these legal alternatives:
- **Pexels** (Free, already integrated)
- **Pixabay** (Free, already integrated)
- **Coverr** (Free, not yet integrated)
- **Videvo** (Free, not yet integrated)

These provide royalty-free content specifically licensed for commercial use.

## Credits

Based on [Douyin_TikTok_Download_API](https://github.com/Evil0ctal/Douyin_TikTok_Download_API) by Evil0ctal.

## References

- TikHub API: https://api.tikhub.io/docs
- Douyin.wtf API: https://douyin.wtf/docs
- Source Project: https://github.com/Evil0ctal/Douyin_TikTok_Download_API
