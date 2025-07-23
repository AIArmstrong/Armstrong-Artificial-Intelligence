---
allowed-tools: [Task, Read, Write, Bash, TodoWrite]
description: "AI-powered YouTube video analysis with transcript extraction and content insights"
intelligence-layers: [MEMORY, REASONING, RESEARCH, FOUNDATION]
creative-cortex: [Content_Intelligence, Technical_Analysis, Multi_Format_Output]
---

# 🎥 /youtube - AI-POWERED VIDEO ANALYSIS ENGINE

## 🧠 INTELLIGENCE SYSTEM
**Stage 1**: YouTube video processing with transcript extraction  
**Stage 2**: 4 Intelligence layers (MEMORY + REASONING + RESEARCH + FOUNDATION)  
**Stage 3**: 3 Creative Cortex innovations for supreme video intelligence

## 🎯 SUPREME PURPOSE
Analyze YouTube videos comprehensively using AI-powered content analysis, automatic transcript extraction, and metadata processing. Integrates with AAI brain modules for intelligent insights and learning.

## 🎪 SUPREME EXECUTION WORKFLOW

**MANDATORY FIRST STEP**: Reference `brain/CLAUDE.md → Command Protocol → Smart Module Loading` to activate YouTube analysis intelligence automatically based on context.

### 🧠 SUPREME MODULE ACTIVATION
```python
# Import YouTube analysis modules
from brain.modules.youtube_command_handler import YouTubeCommandHandler
from brain.modules.youtube_analyzer import analyze_youtube_video

# Execute YouTube analysis with full integration
handler = YouTubeCommandHandler()
result = await handler.handle_youtube_command(
    video_url=video_url,
    focus=focus_type,
    format=output_format
)
```

## Usage
```bash
# Analyze a YouTube video from any URL format
/youtube https://youtu.be/VIDEO_ID
/youtube https://www.youtube.com/watch?v=VIDEO_ID  
/youtube VIDEO_ID

# With specific analysis focus
/youtube [URL] --focus technical
/youtube [URL] --focus summary
/youtube [URL] --focus transcript
/youtube [URL] --focus metadata

# Output format options
/youtube [URL] --format detailed
/youtube [URL] --format summary
/youtube [URL] --format json

# Save results
/youtube [URL] --save
```

## Arguments
- `video_url` - YouTube video URL, short URL, or direct video ID
- `--focus` - Analysis focus: `technical`, `summary`, `transcript`, `metadata`
- `--format` - Output format: `detailed`, `summary`, `json`
- `--save` - Save analysis results to file

## Features

### 🎥 Video Processing
- **Multi-format URL support** - Full URLs, short URLs, playlists, direct IDs
- **Comprehensive metadata** - Title, channel, views, duration, tags, statistics
- **Automatic transcripts** - No API keys required for transcript extraction
- **Error resilience** - Graceful handling when transcripts unavailable

### 🧠 AI Analysis
- **Content summarization** - AI-powered video content analysis
- **Key point extraction** - Most important information highlighted
- **Topic identification** - Main themes and subjects covered
- **Technical assessment** - Identifies educational/technical content
- **Sentiment analysis** - Overall tone and sentiment evaluation

### 🔗 AAI Integration
- **OpenRouter AI** - Uses existing AAI AI infrastructure
- **Analytics tracking** - Performance and usage analytics
- **Memory integration** - Results stored in conversation context
- **Error logging** - Comprehensive error tracking and debugging

## Examples

### Basic Video Analysis
```bash
/youtube https://youtu.be/dQw4w9WgXcQ
```
**Output:**
```
🎥 Video Analysis: "Never Gonna Give You Up" by Rick Astley

📊 METADATA:
- Channel: Rick Astley
- Duration: 3:33
- Views: 1.4B views
- Likes: 14M likes
- Published: 2009-10-25

📝 SUMMARY:
Official music video for Rick Astley's classic 1987 hit "Never Gonna Give You Up." 
The video features the iconic dance moves and has become a cultural phenomenon 
known as "Rickrolling" on the internet.

🔑 KEY POINTS:
• Classic 1987 pop song with distinctive bass line and vocals
• Features Rick Astley's signature dance moves and styling
• Became internet meme phenomenon "Rickrolling" 
• One of the most recognizable songs of the 1980s
• Official music video with high production value

🏷️ TOPICS: [Music, 1980s, Pop, Dance, Meme, Internet Culture]

📈 ASSESSMENT:
- Technical Content: No
- Sentiment: Positive
- Target Audience: General/Music fans
- Value: Entertainment/Cultural significance
```

### Technical Content Analysis
```bash
/youtube https://youtu.be/TECH_VIDEO_ID --focus technical
```
**Output:**
```
🎥 Technical Analysis: "Introduction to Machine Learning"

🔧 TECHNICAL ASSESSMENT: ✅ High technical content detected

📚 TECHNICAL CONCEPTS COVERED:
• Supervised vs unsupervised learning
• Neural network architectures
• Training and validation processes
• Common algorithms (regression, classification)
• Real-world implementation examples

💡 COMPLEXITY LEVEL: Intermediate
🎯 TARGET AUDIENCE: Developers, Data Scientists, Students
📖 EDUCATIONAL VALUE: High - Comprehensive tutorial content

📝 IMPLEMENTATION NOTES:
- Includes code examples in Python
- References popular ML libraries (scikit-learn, TensorFlow)
- Provides practical exercises and datasets
- Good for beginners to intermediate learners
```

### Transcript Focus
```bash
/youtube [URL] --focus transcript --save
```
**Output:**
```
🎥 Transcript Analysis: Complete transcript extracted and saved

📄 TRANSCRIPT STATS:
- Length: 15,234 characters
- Word count: ~2,500 words
- Estimated reading time: 10 minutes
- Language: English (auto-detected)

💾 SAVED TO: analysis/youtube_transcript_VIDEO_ID.txt

🔍 CONTENT HIGHLIGHTS:
[First 500 characters of transcript with key sections highlighted]

📊 ANALYSIS:
- Speaking pace: Moderate (150 WPM)
- Technical terminology: High
- Audience interaction: Direct address style
- Content structure: Well-organized with clear sections
```

## 🛠️ IMPLEMENTATION DETAILS

**MANDATORY FIRST STEP**: Reference `brain/CLAUDE.md → Command Protocol → Smart Module Loading` to activate YouTube intelligence automatically based on context.

### ⚡ Core Command Execution
```python
# Import main command executor
from brain.modules.youtube_command_executor import YouTubeCommandExecutor

# Execute YouTube analysis command
executor = YouTubeCommandExecutor()
result = await executor.execute("/youtube VIDEO_URL --focus technical")
```

### 🧠 Intelligence Layer Integration
The command leverages AAI's intelligence architecture:

```python
# Intelligence layers automatically activated:
# - MEMORY: Recall previous video analysis patterns
# - REASONING: Deep content analysis with WHY explanations  
# - RESEARCH: Auto-research video topics when beneficial
# - FOUNDATION: Quality validation and error handling

# Creative Cortex modules:
# - Content_Intelligence: Advanced video content understanding
# - Technical_Analysis: Technical content detection and analysis
# - Multi_Format_Output: Optimal output formatting based on content type
```

### 🔧 Core Functionality
The command integrates with multiple YouTube analyzer modules:

```python
# For Claude Code integration
from brain.modules.youtube_claude_integration import analyze_youtube_video_for_claude

# Simple analysis
result = await analyze_youtube_video_for_claude("https://youtu.be/VIDEO_ID")

# Advanced analysis with specific focus
result = await analyze_youtube_video_for_claude(
    video_url="VIDEO_ID", 
    focus="technical", 
    format="summary"
)
```

### 🎯 Direct Module Integration
```python
from brain.modules.youtube_analyzer import YouTubeAnalyzer, VideoAnalysis
from brain.modules.youtube_command_handler import YouTubeCommandHandler

# Advanced usage with full control
handler = YouTubeCommandHandler()
result = await handler.handle_youtube_command(
    video_url="https://youtu.be/VIDEO_ID",
    focus="technical",
    format="json", 
    save=True
)
```

### Error Handling
- **Invalid URLs** - Clear error messages with format examples
- **Private/Unavailable videos** - Graceful handling with alternative suggestions
- **API failures** - Fallback to metadata-only analysis
- **Transcript issues** - Continue analysis without transcript when unavailable

### Performance Optimization
- **Concurrent processing** - Metadata and transcript extraction in parallel
- **Smart caching** - Avoid re-analyzing recently processed videos
- **Rate limiting** - Respect YouTube API and OpenRouter rate limits
- **Timeout handling** - Prevent hanging on slow video processing

## Configuration

### Environment Variables
```bash
# Required for full functionality
YOUTUBE_API_KEY=your_youtube_api_key_here
OPENROUTER_API_KEY=your_openrouter_key_here

# Optional configuration
YOUTUBE_ANALYSIS_CACHE_HOURS=24
YOUTUBE_MAX_TRANSCRIPT_LENGTH=50000
YOUTUBE_ANALYSIS_TIMEOUT=60
```

### Dependencies
```bash
# Install required packages
pip install google-api-python-client youtube-transcript-api

# Verify installation
python -c "from brain.modules.youtube_analyzer import YouTubeAnalyzer; print('✅ Ready')"
```

## Integration Notes

### AAI Brain Integration
- **Memory Storage** - Analysis results stored in conversation memory
- **Analytics Tracking** - Usage patterns and performance metrics logged
- **Learning Loops** - Successful analysis patterns improve future processing
- **Cross-Module** - Results available to other AAI modules and commands

### Command Chaining
```bash
# Analyze video then generate PRP based on content
/youtube [URL] --focus technical && /generate-prp "implement concepts from analyzed video"

# Analyze multiple videos and compare
/youtube [URL1] --save && /youtube [URL2] --save && /compare-analyses
```

### Voice Interface Integration (Future)
When Jarvis voice interface is implemented:
```
"Hey Claude, analyze this video: [URL] and tell me the key technical points"
```

## Success Metrics
- **Analysis Accuracy** - >90% successful video processing
- **Response Time** - <10 seconds for typical videos
- **Transcript Success** - >80% transcript extraction rate
- **User Satisfaction** - High-quality, actionable insights

## Future Enhancements
- **Playlist Analysis** - Process entire playlists automatically
- **Comparative Analysis** - Compare multiple videos on same topic
- **Content Recommendations** - Suggest related videos based on analysis
- **Export Options** - PDF, markdown, structured data formats
- **Batch Processing** - Analyze multiple videos simultaneously

---

*YouTube Analysis Command | AAI Brain Integration | Powered by OpenRouter AI*