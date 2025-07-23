# YouTube Integration Setup Guide

## Overview
This guide will help you set up the YouTube video analysis integration in your AAI system. The integration provides comprehensive YouTube video analysis with transcript extraction, AI-powered insights, and seamless command integration.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Install required packages
pip install google-api-python-client youtube-transcript-api

# Or install from requirements file
pip install -r requirements_youtube.txt

# Verify installation
python -c "from brain.modules.youtube_analyzer import YouTubeAnalyzer; print('✅ YouTube integration ready')"
```

### 2. Get YouTube API Key (Optional but Recommended)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing project
3. Enable **YouTube Data API v3**
4. Create credentials → API Key
5. Copy the API key for next step

### 3. Configure Environment Variables
```bash
# Add to your .env file
echo "YOUTUBE_API_KEY=your_youtube_api_key_here" >> .env

# Optional configuration
echo "YOUTUBE_ANALYSIS_CACHE_HOURS=24" >> .env
echo "YOUTUBE_MAX_TRANSCRIPT_LENGTH=50000" >> .env
```

### 4. Test the Integration
```bash
# Test with a simple video
python -c "
import asyncio
from brain.modules.youtube_analyzer import analyze_youtube_video

async def test():
    result = await analyze_youtube_video('https://youtu.be/dQw4w9WgXcQ')
    print('✅ Success!' if result.success else f'❌ Failed: {result.error_message}')

asyncio.run(test())
"
```

## 📋 Detailed Setup

### Dependencies Explanation

| Package | Purpose | Required |
|---------|---------|----------|
| `google-api-python-client` | YouTube Data API access | Recommended |
| `youtube-transcript-api` | Transcript extraction | Yes |
| `python-dateutil` | Date parsing utilities | Auto-installed |
| `isodate` | ISO 8601 duration parsing | Auto-installed |

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `YOUTUBE_API_KEY` | YouTube Data API v3 key | None | No* |
| `OPENROUTER_API_KEY` | AI analysis (existing) | None | Recommended |
| `YOUTUBE_ANALYSIS_CACHE_HOURS` | Cache duration | 24 | No |
| `YOUTUBE_MAX_TRANSCRIPT_LENGTH` | Transcript limit | 50000 | No |

**Note**: YouTube API key is not required for transcript extraction, but enables richer metadata analysis.

### File Structure After Setup
```
AAI/
├── brain/modules/
│   ├── youtube_analyzer.py          # ✅ Core analyzer
│   └── youtube_command_handler.py   # ✅ Command integration
├── .claude/commands/
│   └── youtube.md                   # ✅ Command documentation
├── tests/
│   └── test_youtube_analyzer.py     # ✅ Test suite
├── requirements_youtube.txt         # ✅ Dependencies
└── setup_youtube_integration.md     # ✅ This guide
```

## 🧪 Testing Your Setup

### Basic Functionality Test
```python
import asyncio
from brain.modules.youtube_analyzer import YouTubeAnalyzer

async def test_basic():
    analyzer = YouTubeAnalyzer()
    
    # Test video ID extraction
    video_id, content_type = analyzer.extract_video_id("https://youtu.be/dQw4w9WgXcQ")
    print(f"✅ URL parsing: {video_id} ({content_type})")
    
    # Test full analysis (will use mock data if APIs unavailable)
    analysis = await analyzer.analyze_video("https://youtu.be/dQw4w9WgXcQ")
    print(f"✅ Analysis: {'Success' if analysis.success else 'Failed'}")
    
    return analysis

# Run test
result = asyncio.run(test_basic())
print(f"Summary: {result.summary}")
```

### Command Handler Test
```python
import asyncio
from brain.modules.youtube_command_handler import YouTubeCommandHandler

async def test_command():
    handler = YouTubeCommandHandler()
    
    # Test different output formats
    detailed = await handler.handle_youtube_command(
        "https://youtu.be/dQw4w9WgXcQ", 
        format="detailed"
    )
    
    summary = await handler.handle_youtube_command(
        "https://youtu.be/dQw4w9WgXcQ", 
        format="summary"
    )
    
    print("✅ Detailed format:", len(detailed), "characters")
    print("✅ Summary format:", len(summary), "characters")

asyncio.run(test_command())
```

### Run Full Test Suite
```bash
# Run all tests
pytest tests/test_youtube_analyzer.py -v

# Run specific test categories
pytest tests/test_youtube_analyzer.py::TestYouTubeAnalyzer -v
pytest tests/test_youtube_analyzer.py::TestYouTubeCommandHandler -v
```

## 🎯 Usage Examples

### Basic Video Analysis
```python
from brain.modules.youtube_analyzer import analyze_youtube_video

# Analyze any YouTube video
result = await analyze_youtube_video("https://youtu.be/VIDEO_ID")

print(f"Title: {result.metadata.title}")
print(f"Summary: {result.summary}")
print(f"Key Points: {result.key_points}")
print(f"Technical Content: {result.technical_content}")
```

### Command Integration Usage
Once set up, you can use the `/youtube` command:

```bash
# Basic analysis
/youtube https://youtu.be/VIDEO_ID

# Focused analysis
/youtube VIDEO_ID --focus technical
/youtube VIDEO_ID --focus summary  
/youtube VIDEO_ID --focus transcript

# Different output formats
/youtube VIDEO_ID --format json
/youtube VIDEO_ID --format summary
```

### Programmatic Integration
```python
from brain.modules.youtube_command_handler import YouTubeCommandHandler

handler = YouTubeCommandHandler()

# Get formatted analysis
analysis = await handler.handle_youtube_command(
    video_url="https://youtu.be/VIDEO_ID",
    focus="technical",
    format="detailed"
)

print(analysis)  # Formatted output ready for display
```

## 🔧 Configuration Options

### Performance Tuning
```python
# In youtube_analyzer.py, adjust these settings:
class YouTubeAnalyzer:
    def __init__(self):
        self.max_transcript_length = 50000  # Reduce for faster processing
        self.cache_duration = timedelta(hours=24)  # Adjust caching
```

### Error Handling Configuration
```python
# Custom error handling
analyzer = YouTubeAnalyzer()
analyzer.enable_verbose_logging = True  # More detailed logs
analyzer.retry_attempts = 3  # API retry attempts
```

### API Rate Limiting
```python
# Built-in rate limiting (automatically configured)
# - YouTube API: 10,000 requests/day default quota
# - Transcript API: No rate limits (unofficial API)
# - OpenRouter: Uses existing AAI rate limiting
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Missing Dependencies
**Error**: `ModuleNotFoundError: No module named 'googleapiclient'`

**Solution**:
```bash
pip install google-api-python-client youtube-transcript-api
```

#### 2. YouTube API Quota Exceeded
**Error**: `HttpError 403: The request cannot be completed because you have exceeded your quota.`

**Solution**:
- Check [Google Cloud Console](https://console.cloud.google.com/) quota usage
- Request quota increase or wait for reset (daily quotas reset at midnight Pacific Time)
- System will gracefully degrade to transcript-only analysis

#### 3. Transcript Not Available
**Error**: `No transcript available for video: VIDEO_ID`

**Solution**:
- This is normal for many videos (music, visual content, etc.)
- System will analyze using metadata only
- Try a different video with spoken content

#### 4. OpenRouter Integration Issues
**Error**: `OpenRouter integration failed`

**Solution**:
```bash
# Check OpenRouter API key
echo $OPENROUTER_API_KEY

# Verify existing AAI OpenRouter setup
python -c "from brain.modules.openrouter.router_client import OpenRouterClient; print('✅ OK')"
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed logging
from brain.modules.youtube_analyzer import YouTubeAnalyzer
analyzer = YouTubeAnalyzer()
# Now all operations will show detailed logs
```

### Validation Commands
```bash
# Test video ID extraction
python -c "
from brain.modules.youtube_analyzer import YouTubeAnalyzer
a = YouTubeAnalyzer()
print(a.extract_video_id('https://youtu.be/dQw4w9WgXcQ'))
"

# Test transcript extraction
python -c "
import asyncio
from brain.modules.youtube_analyzer import YouTubeAnalyzer
async def test():
    a = YouTubeAnalyzer()
    t = await a.get_video_transcript('dQw4w9WgXcQ')
    print('Transcript length:', len(t) if t else 'None')
asyncio.run(test())
"
```

## 🔗 Integration with AAI Features

### Memory Integration
YouTube analysis results are automatically stored in AAI conversation memory:
```python
# Analysis results are automatically logged to:
# - brain/modules/unified_analytics.py (performance metrics)
# - brain/modules/mem0-memory-enhancement.md (conversation context)
```

### Command System Integration
The YouTube analyzer integrates with the existing command system:
```python
# Commands can chain YouTube analysis:
# /youtube VIDEO_URL && /generate-prp "implement concepts from analyzed video"
```

### Voice Interface Integration (Future)
When the Jarvis voice interface is implemented:
```python
# Voice commands will be supported:
# "Hey Claude, analyze this video: VIDEO_URL"
# "What are the key points from that YouTube video?"
```

## 📈 Performance Expectations

### Typical Performance Metrics
- **URL Processing**: <0.1 seconds
- **Metadata Extraction**: 1-3 seconds (with API)
- **Transcript Extraction**: 2-5 seconds
- **AI Analysis**: 3-8 seconds (depends on content length)
- **Total Processing**: 5-15 seconds typical

### Resource Usage
- **Memory**: ~50-100MB during processing
- **CPU**: Moderate during AI analysis phase
- **Network**: Dependent on video length and metadata complexity

### Optimization Tips
1. **Cache Results**: Analysis results are cached for 24 hours by default
2. **Limit Transcript Length**: Large transcripts are automatically truncated
3. **Parallel Processing**: Metadata and transcript extraction run concurrently
4. **Rate Limiting**: Built-in to prevent API overuse

## 🎉 Success Verification

You'll know the integration is working correctly when:

1. **✅ Module Import**: No errors importing YouTube modules
2. **✅ URL Parsing**: Successfully extracts video IDs from various URL formats  
3. **✅ Metadata Extraction**: Retrieves video title, channel, views, etc.
4. **✅ Transcript Extraction**: Gets transcripts when available
5. **✅ AI Analysis**: Generates summaries and insights
6. **✅ Command Integration**: `/youtube` command works in Claude Code
7. **✅ Error Handling**: Graceful degradation when APIs unavailable

### Final Verification Test
```bash
# Comprehensive integration test
python -c "
import asyncio
from brain.modules.youtube_analyzer import analyze_youtube_video

async def verify():
    # Test with Rick Roll (reliable test video)
    result = await analyze_youtube_video('https://youtu.be/dQw4w9WgXcQ')
    
    checks = [
        ('Success', result.success),
        ('Has metadata', result.metadata is not None),
        ('Has title', bool(result.metadata.title if result.metadata else False)),
        ('Has summary', bool(result.summary)),
        ('Processing time reasonable', result.processing_time < 30)
    ]
    
    print('YouTube Integration Verification:')
    for check, passed in checks:
        print(f'  {check}: {'✅' if passed else '❌'}')
    
    overall = all(passed for _, passed in checks)
    print(f'\nOverall Status: {'✅ READY' if overall else '❌ NEEDS ATTENTION'}')
    
    return overall

success = asyncio.run(verify())
exit(0 if success else 1)
"
```

If this test passes, your YouTube integration is fully functional! 🎉

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review logs for specific error messages
3. Test with a different video URL
4. Verify API keys and environment variables
5. Run the validation commands to isolate issues

The integration is designed to be robust and degrade gracefully when components are unavailable, so basic functionality should work even without all optional dependencies.