"""
YouTube Video Analyzer - AAI Brain Module
Comprehensive YouTube video analysis with transcript extraction and AI-powered insights
Integrated with AAI infrastructure patterns following OpenRouter and analytics systems
"""

import os
import re
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs

# AAI Infrastructure
from brain.modules.openrouter.router_client import OpenRouterClient
try:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from brain.modules.unified_analytics import UnifiedAnalyticsClient
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False
    UnifiedAnalyticsClient = None

# External dependencies for YouTube processing
try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    YOUTUBE_API_AVAILABLE = True
except ImportError:
    YOUTUBE_API_AVAILABLE = False
    
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        TranscriptsDisabled, 
        NoTranscriptFound, 
        VideoUnavailable
    )
    TRANSCRIPT_API_AVAILABLE = True
except ImportError:
    TRANSCRIPT_API_AVAILABLE = False

import requests
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VideoMetadata:
    """Comprehensive video metadata structure"""
    video_id: str
    title: str
    description: str
    channel_name: str
    channel_id: str
    published_at: str
    duration: str
    view_count: int
    like_count: int
    comment_count: int
    tags: List[str]
    category_id: str
    default_language: Optional[str]
    thumbnail_url: str
    
@dataclass
class VideoAnalysis:
    """Complete video analysis result"""
    metadata: VideoMetadata
    transcript: Optional[str]
    summary: str
    key_points: List[str]
    topics: List[str]
    sentiment: str
    technical_content: bool
    processing_time: float
    success: bool
    error_message: Optional[str]

class YouTubeAnalyzer:
    """
    Advanced YouTube video analyzer with AAI integration
    
    Features:
    - Multi-format URL support (full URLs, short URLs, playlists, direct IDs)
    - Comprehensive metadata extraction via YouTube Data API v3
    - Automatic transcript extraction without API keys
    - AI-powered content analysis and summarization
    - Integration with AAI analytics and memory systems
    - Robust error handling and graceful degradation
    """
    
    def __init__(self):
        """Initialize YouTube analyzer with AAI integrations"""
        
        # API Keys and Configuration
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        self.openrouter_client = None
        self.analytics_client = None
        
        # Initialize AAI integrations
        try:
            self.openrouter_client = OpenRouterClient()
            logger.info("✅ OpenRouter integration initialized")
        except Exception as e:
            logger.warning(f"⚠️  OpenRouter integration failed: {e}")
            
        try:
            if ANALYTICS_AVAILABLE and UnifiedAnalyticsClient:
                self.analytics_client = UnifiedAnalyticsClient()
                logger.info("✅ Analytics integration initialized")
            else:
                self.analytics_client = None
                logger.warning("⚠️  Analytics module not available")
        except Exception as e:
            logger.warning(f"⚠️  Analytics integration failed: {e}")
            self.analytics_client = None
        
        # YouTube API client
        self.youtube_service = None
        if self.youtube_api_key and YOUTUBE_API_AVAILABLE:
            try:
                self.youtube_service = build('youtube', 'v3', developerKey=self.youtube_api_key)
                logger.info("✅ YouTube Data API initialized")
            except Exception as e:
                logger.error(f"❌ YouTube API initialization failed: {e}")
        else:
            if not YOUTUBE_API_AVAILABLE:
                logger.warning("⚠️  Google API client not installed. Run: pip install google-api-python-client")
            if not self.youtube_api_key:
                logger.warning("⚠️  YOUTUBE_API_KEY not found in environment")
        
        # Validation flags
        if not TRANSCRIPT_API_AVAILABLE:
            logger.warning("⚠️  YouTube transcript API not available. Run: pip install youtube-transcript-api")
            
        # Processing configuration
        self.max_transcript_length = 50000  # Limit for AI processing
        self.max_summary_length = 2000
        self.cache_duration = timedelta(hours=24)
        
    def extract_video_id(self, query: str) -> tuple[str, str]:
        """
        Extract video ID from various YouTube URL formats
        
        Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID  
        - https://youtube.com/watch?v=VIDEO_ID
        - https://www.youtube.com/playlist?list=PLAYLIST_ID
        - Direct VIDEO_ID or PLAYLIST_ID
        """
        
        # Clean the query
        query = query.strip()
        
        # Direct video ID (11 characters, alphanumeric and dashes/underscores)
        if re.match(r'^[a-zA-Z0-9_-]{11}$', query):
            return query, "video"
            
        # Direct playlist ID (starts with PL, UC, UU, FL, etc.)
        if re.match(r'^(PL|UC|UU|FL|RD)[a-zA-Z0-9_-]+$', query):
            return query, "playlist"
            
        # Parse URL
        try:
            parsed = urlparse(query)
            
            # Standard YouTube URLs
            if 'youtube.com' in parsed.netloc:
                if '/watch' in parsed.path:
                    # Extract video ID from query params
                    params = parse_qs(parsed.query)
                    if 'v' in params:
                        return params['v'][0], "video"
                elif '/playlist' in parsed.path:
                    # Extract playlist ID
                    params = parse_qs(parsed.query)
                    if 'list' in params:
                        return params['list'][0], "playlist"
                        
            # Short YouTube URLs (youtu.be)
            elif 'youtu.be' in parsed.netloc:
                # Video ID is in the path
                video_id = parsed.path.lstrip('/')
                if video_id:
                    return video_id, "video"
                    
        except Exception as e:
            logger.warning(f"URL parsing failed: {e}")
            
        raise ValueError(f"Could not extract video ID from: {query}")
    
    async def get_video_metadata(self, video_id: str) -> Optional[VideoMetadata]:
        """
        Extract comprehensive video metadata using YouTube Data API
        """
        
        if not self.youtube_service:
            logger.error("YouTube API not available for metadata extraction")
            return None
            
        try:
            # Multi-part API call for comprehensive data
            response = self.youtube_service.videos().list(
                part="statistics,snippet,contentDetails,status",
                id=video_id
            ).execute()
            
            if not response['items']:
                logger.error(f"Video not found: {video_id}")
                return None
                
            video_data = response['items'][0]
            snippet = video_data['snippet']
            statistics = video_data['statistics']
            content_details = video_data['contentDetails']
            
            # Parse duration (PT format to readable)
            duration = content_details.get('duration', 'Unknown')
            duration_readable = self._parse_duration(duration)
            
            # Extract metadata
            metadata = VideoMetadata(
                video_id=video_id,
                title=snippet.get('title', 'Unknown'),
                description=snippet.get('description', ''),
                channel_name=snippet.get('channelTitle', 'Unknown'),
                channel_id=snippet.get('channelId', ''),
                published_at=snippet.get('publishedAt', ''),
                duration=duration_readable,
                view_count=int(statistics.get('viewCount', 0)),
                like_count=int(statistics.get('likeCount', 0)),
                comment_count=int(statistics.get('commentCount', 0)),
                tags=snippet.get('tags', []),
                category_id=snippet.get('categoryId', ''),
                default_language=snippet.get('defaultLanguage'),
                thumbnail_url=snippet.get('thumbnails', {}).get('high', {}).get('url', '')
            )
            
            return metadata
            
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Metadata extraction failed: {e}")
            return None
    
    def _parse_duration(self, duration: str) -> str:
        """Parse YouTube duration format (PT1H30M45S) to readable format"""
        
        if not duration.startswith('PT'):
            return duration
            
        # Remove PT prefix
        duration = duration[2:]
        
        hours = 0
        minutes = 0
        seconds = 0
        
        # Extract hours
        if 'H' in duration:
            hours_match = re.search(r'(\d+)H', duration)
            if hours_match:
                hours = int(hours_match.group(1))
                
        # Extract minutes
        if 'M' in duration:
            minutes_match = re.search(r'(\d+)M', duration)
            if minutes_match:
                minutes = int(minutes_match.group(1))
                
        # Extract seconds
        if 'S' in duration:
            seconds_match = re.search(r'(\d+)S', duration)
            if seconds_match:
                seconds = int(seconds_match.group(1))
        
        # Format readable duration
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    async def get_video_transcript(self, video_id: str) -> Optional[str]:
        """
        Extract video transcript using youtube-transcript-api
        No API key required, supports multiple languages
        """
        
        if not TRANSCRIPT_API_AVAILABLE:
            logger.warning("Transcript API not available")
            return None
            
        try:
            # Get transcript (automatically tries multiple languages)
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Join transcript segments into coherent text
            transcript_text = ' '.join([
                segment['text'].strip() 
                for segment in transcript_list 
                if segment['text'].strip()
            ])
            
            # Limit transcript length for AI processing
            if len(transcript_text) > self.max_transcript_length:
                transcript_text = transcript_text[:self.max_transcript_length] + "..."
                logger.info(f"Transcript truncated to {self.max_transcript_length} characters")
                
            return transcript_text
            
        except (TranscriptsDisabled, NoTranscriptFound):
            logger.info(f"No transcript available for video: {video_id}")
            return None
        except VideoUnavailable:
            logger.error(f"Video unavailable: {video_id}")
            return None
        except Exception as e:
            logger.error(f"Transcript extraction failed: {e}")
            return None
    
    async def analyze_video_content(self, metadata: VideoMetadata, 
                                   transcript: Optional[str]) -> Dict[str, Any]:
        """
        AI-powered video content analysis using OpenRouter
        """
        
        if not self.openrouter_client:
            logger.warning("OpenRouter not available for content analysis")
            return self._create_basic_analysis(metadata, transcript)
            
        try:
            # Construct analysis prompt
            analysis_prompt = self._build_analysis_prompt(metadata, transcript)
            
            # Call OpenRouter for analysis
            response = await self._call_openrouter_analysis(analysis_prompt)
            
            # Parse AI response
            analysis = self._parse_ai_response(response)
            
            return analysis
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return self._create_basic_analysis(metadata, transcript)
    
    def _build_analysis_prompt(self, metadata: VideoMetadata, transcript: Optional[str]) -> str:
        """Build comprehensive analysis prompt for AI"""
        
        prompt = f"""Analyze this YouTube video and provide comprehensive insights.

VIDEO METADATA:
- Title: {metadata.title}
- Channel: {metadata.channel_name}
- Duration: {metadata.duration}
- Views: {metadata.view_count:,}
- Likes: {metadata.like_count:,}
- Published: {metadata.published_at}
- Tags: {', '.join(metadata.tags[:10])}

DESCRIPTION:
{metadata.description[:1000]}

"""
        
        if transcript:
            prompt += f"""
VIDEO TRANSCRIPT:
{transcript}

"""
        else:
            prompt += """
VIDEO TRANSCRIPT: Not available

"""
        
        prompt += """Please provide a comprehensive analysis including:

1. SUMMARY: A concise 2-3 sentence summary of the video's main content
2. KEY_POINTS: 5-7 bullet points of the most important information covered
3. TOPICS: Main topics and themes discussed (as array)
4. TECHNICAL_CONTENT: Whether this contains technical/educational content (true/false)
5. SENTIMENT: Overall tone (positive/negative/neutral)
6. TARGET_AUDIENCE: Who this video is intended for
7. VALUE_ASSESSMENT: Educational, entertainment, or commercial value

Format your response as valid JSON with these exact keys:
{
    "summary": "string",
    "key_points": ["point1", "point2", "point3"],
    "topics": ["topic1", "topic2"],
    "technical_content": boolean,
    "sentiment": "string",
    "target_audience": "string",
    "value_assessment": "string"
}"""
        
        return prompt
    
    async def _call_openrouter_analysis(self, prompt: str) -> str:
        """Call OpenRouter for AI analysis"""
        
        try:
            # Use existing OpenRouter client
            messages = [{"role": "user", "content": prompt}]
            
            response = await self.openrouter_client.generate_response(
                messages=messages,
                model="anthropic/claude-3-haiku",  # Fast and cost-effective
                max_tokens=2000,
                temperature=0.1
            )
            
            return response
            
        except Exception as e:
            logger.error(f"OpenRouter API call failed: {e}")
            raise
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response into structured analysis"""
        
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis_data = json.loads(json_match.group())
                return analysis_data
            else:
                # Fallback parsing
                return self._fallback_parse_response(response)
                
        except json.JSONDecodeError:
            return self._fallback_parse_response(response)
    
    def _fallback_parse_response(self, response: str) -> Dict[str, Any]:
        """Fallback parsing when JSON parsing fails"""
        
        return {
            "summary": response[:500] if response else "Analysis unavailable",
            "key_points": ["Analysis parsing failed - raw response available"],
            "topics": ["General"],
            "technical_content": False,
            "sentiment": "neutral",
            "target_audience": "General audience",
            "value_assessment": "Content analysis incomplete"
        }
    
    def _create_basic_analysis(self, metadata: VideoMetadata, 
                              transcript: Optional[str]) -> Dict[str, Any]:
        """Create basic analysis when AI analysis is unavailable"""
        
        # Basic analysis based on metadata
        technical_indicators = ['tutorial', 'how to', 'programming', 'code', 'technical', 'development']
        is_technical = any(indicator in metadata.title.lower() for indicator in technical_indicators)
        
        # Estimate sentiment based on like/view ratio
        if metadata.view_count > 0:
            like_ratio = metadata.like_count / metadata.view_count
            sentiment = "positive" if like_ratio > 0.01 else "neutral"
        else:
            sentiment = "neutral"
        
        return {
            "summary": f"Video titled '{metadata.title}' by {metadata.channel_name}. " +
                      f"Published {metadata.published_at}, Duration: {metadata.duration}.",
            "key_points": [
                f"Channel: {metadata.channel_name}",
                f"Duration: {metadata.duration}",
                f"Views: {metadata.view_count:,}",
                f"Published: {metadata.published_at}"
            ],
            "topics": metadata.tags[:5] if metadata.tags else ["General"],
            "technical_content": is_technical,
            "sentiment": sentiment,
            "target_audience": "General audience",
            "value_assessment": "Metadata-based analysis (transcript/AI unavailable)"
        }
    
    async def analyze_video(self, video_url: str) -> VideoAnalysis:
        """
        Complete video analysis pipeline
        
        Args:
            video_url: YouTube video URL, short URL, or video ID
            
        Returns:
            VideoAnalysis object with complete analysis results
        """
        
        start_time = datetime.now()
        
        try:
            # Extract video ID
            video_id, content_type = self.extract_video_id(video_url)
            
            if content_type == "playlist":
                # For playlists, analyze the first video
                logger.info("Playlist detected - analyzing first video")
                # Implementation would extract first video from playlist
                # For now, return error
                raise ValueError("Playlist analysis not yet implemented")
            
            logger.info(f"Analyzing video: {video_id}")
            
            # Get video metadata
            metadata = await self.get_video_metadata(video_id)
            if not metadata:
                raise ValueError(f"Could not retrieve metadata for video: {video_id}")
            
            # Get video transcript
            transcript = await self.get_video_transcript(video_id)
            
            # Perform AI analysis
            analysis_data = await self.analyze_video_content(metadata, transcript)
            
            # Calculate processing time
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Create comprehensive analysis result
            analysis = VideoAnalysis(
                metadata=metadata,
                transcript=transcript,
                summary=analysis_data.get("summary", ""),
                key_points=analysis_data.get("key_points", []),
                topics=analysis_data.get("topics", []),
                sentiment=analysis_data.get("sentiment", "neutral"),
                technical_content=analysis_data.get("technical_content", False),
                processing_time=processing_time,
                success=True,
                error_message=None
            )
            
            # Log to analytics if available
            await self._log_analysis_success(analysis)
            
            logger.info(f"✅ Video analysis completed in {processing_time:.2f}s")
            return analysis
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            error_message = str(e)
            
            logger.error(f"❌ Video analysis failed: {error_message}")
            
            # Create error analysis result
            analysis = VideoAnalysis(
                metadata=None,
                transcript=None,
                summary=f"Analysis failed: {error_message}",
                key_points=[],
                topics=[],
                sentiment="neutral",
                technical_content=False,
                processing_time=processing_time,
                success=False,
                error_message=error_message
            )
            
            # Log error to analytics
            await self._log_analysis_error(video_url, error_message)
            
            return analysis
    
    async def _log_analysis_success(self, analysis: VideoAnalysis):
        """Log successful analysis to AAI analytics"""
        
        if not self.analytics_client:
            return
            
        try:
            await self.analytics_client.log_event({
                "event_type": "youtube_analysis_success",
                "video_id": analysis.metadata.video_id,
                "video_title": analysis.metadata.title,
                "channel_name": analysis.metadata.channel_name,
                "processing_time": analysis.processing_time,
                "has_transcript": analysis.transcript is not None,
                "technical_content": analysis.technical_content,
                "sentiment": analysis.sentiment,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            logger.warning(f"Analytics logging failed: {e}")
    
    async def _log_analysis_error(self, video_url: str, error_message: str):
        """Log analysis error to AAI analytics"""
        
        if not self.analytics_client:
            return
            
        try:
            await self.analytics_client.log_event({
                "event_type": "youtube_analysis_error", 
                "video_url": video_url,
                "error_message": error_message,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            logger.warning(f"Error logging failed: {e}")

# Convenience function for easy imports
async def analyze_youtube_video(video_url: str) -> VideoAnalysis:
    """
    Convenience function to analyze a YouTube video
    
    Usage:
        from brain.modules.youtube_analyzer import analyze_youtube_video
        
        result = await analyze_youtube_video("https://youtu.be/VIDEO_ID")
        print(result.summary)
    """
    
    analyzer = YouTubeAnalyzer()
    return await analyzer.analyze_video(video_url)

# Module validation
if __name__ == "__main__":
    # Basic module validation
    analyzer = YouTubeAnalyzer()
    print("✅ YouTube Analyzer module loaded successfully")
    
    # Test video ID extraction
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ", 
        "dQw4w9WgXcQ"
    ]
    
    for url in test_urls:
        try:
            video_id, content_type = analyzer.extract_video_id(url)
            print(f"✅ {url} → {video_id} ({content_type})")
        except Exception as e:
            print(f"❌ {url} → {e}")