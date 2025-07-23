"""
Tests for YouTube Analyzer Module
Comprehensive testing of YouTube video analysis functionality
"""

import pytest
import asyncio
import os
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# Import modules to test
from brain.modules.youtube_analyzer import YouTubeAnalyzer, VideoMetadata, VideoAnalysis
from brain.modules.youtube_command_handler import YouTubeCommandHandler


class TestYouTubeAnalyzer:
    """Test suite for YouTubeAnalyzer class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = YouTubeAnalyzer()
    
    def test_video_id_extraction_standard_url(self):
        """Test extraction from standard YouTube URLs"""
        test_cases = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "video"),
            ("https://youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "video"),
            ("http://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "video"),
        ]
        
        for url, expected_id, expected_type in test_cases:
            video_id, content_type = self.analyzer.extract_video_id(url)
            assert video_id == expected_id
            assert content_type == expected_type
    
    def test_video_id_extraction_short_url(self):
        """Test extraction from short YouTube URLs"""
        test_cases = [
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ", "video"),
            ("http://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ", "video"),
            ("youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ", "video"),
        ]
        
        for url, expected_id, expected_type in test_cases:
            video_id, content_type = self.analyzer.extract_video_id(url)
            assert video_id == expected_id
            assert content_type == expected_type
    
    def test_video_id_extraction_direct_id(self):
        """Test extraction from direct video ID"""
        direct_id = "dQw4w9WgXcQ"
        video_id, content_type = self.analyzer.extract_video_id(direct_id)
        assert video_id == direct_id
        assert content_type == "video"
    
    def test_playlist_id_extraction(self):
        """Test extraction of playlist IDs"""
        test_cases = [
            ("https://www.youtube.com/playlist?list=PLrAXtmRdnEQy6nuLMt9H1P_ZE2ToZoHU8", 
             "PLrAXtmRdnEQy6nuLMt9H1P_ZE2ToZoHU8", "playlist"),
            ("PLrAXtmRdnEQy6nuLMt9H1P_ZE2ToZoHU8", 
             "PLrAXtmRdnEQy6nuLMt9H1P_ZE2ToZoHU8", "playlist"),
        ]
        
        for url, expected_id, expected_type in test_cases:
            playlist_id, content_type = self.analyzer.extract_video_id(url)
            assert playlist_id == expected_id
            assert content_type == expected_type
    
    def test_invalid_video_id_extraction(self):
        """Test handling of invalid URLs"""
        invalid_urls = [
            "not_a_url",
            "https://example.com",
            "https://youtube.com/invalid",
            "invalid_id_123",
            ""
        ]
        
        for invalid_url in invalid_urls:
            with pytest.raises(ValueError):
                self.analyzer.extract_video_id(invalid_url)
    
    def test_duration_parsing(self):
        """Test YouTube duration format parsing"""
        test_cases = [
            ("PT1H30M45S", "1:30:45"),
            ("PT30M45S", "30:45"),
            ("PT45S", "0:45"),
            ("PT1H", "1:00:00"),
            ("PT2M", "2:00"),
            ("PT", "0:00"),
        ]
        
        for youtube_duration, expected in test_cases:
            result = self.analyzer._parse_duration(youtube_duration)
            assert result == expected
    
    def test_duration_parsing_invalid(self):
        """Test duration parsing with invalid input"""
        invalid_durations = ["invalid", "1:30:45", ""]
        
        for invalid_duration in invalid_durations:
            result = self.analyzer._parse_duration(invalid_duration)
            # Should return original string if parsing fails
            assert result == invalid_duration
    
    @patch('brain.modules.youtube_analyzer.YouTubeTranscriptApi')
    def test_transcript_extraction_success(self, mock_transcript_api):
        """Test successful transcript extraction"""
        # Mock transcript data
        mock_transcript = [
            {"text": "Hello everyone", "start": 0.0},
            {"text": "Welcome to this video", "start": 2.5},
            {"text": "Today we'll learn about", "start": 5.0},
        ]
        mock_transcript_api.get_transcript.return_value = mock_transcript
        
        # Test transcript extraction
        video_id = "test_video_id"
        result = asyncio.run(self.analyzer.get_video_transcript(video_id))
        
        expected_text = "Hello everyone Welcome to this video Today we'll learn about"
        assert result == expected_text
        mock_transcript_api.get_transcript.assert_called_once_with(video_id)
    
    @patch('brain.modules.youtube_analyzer.YouTubeTranscriptApi')
    def test_transcript_extraction_failure(self, mock_transcript_api):
        """Test transcript extraction failure handling"""
        from youtube_transcript_api._errors import TranscriptsDisabled
        
        # Mock transcript API to raise exception
        mock_transcript_api.get_transcript.side_effect = TranscriptsDisabled("test_video_id")
        
        # Test transcript extraction
        video_id = "test_video_id"
        result = asyncio.run(self.analyzer.get_video_transcript(video_id))
        
        assert result is None
    
    def test_create_basic_analysis(self):
        """Test basic analysis creation when AI is unavailable"""
        # Create test metadata
        metadata = VideoMetadata(
            video_id="test_id",
            title="Learn Python Programming",
            description="A comprehensive tutorial",
            channel_name="Tech Channel",
            channel_id="UC123",
            published_at="2023-01-01T00:00:00Z",
            duration="15:30",
            view_count=1000,
            like_count=50,
            comment_count=10,
            tags=["python", "programming", "tutorial"],
            category_id="27",
            default_language="en",
            thumbnail_url="https://example.com/thumbnail.jpg"
        )
        
        # Test basic analysis
        analysis = self.analyzer._create_basic_analysis(metadata, "Sample transcript")
        
        assert "Learn Python Programming" in analysis["summary"]
        assert "Tech Channel" in analysis["summary"]
        assert analysis["technical_content"] == True  # Should detect technical content
        assert analysis["topics"] == ["python", "programming", "tutorial"]
        assert analysis["sentiment"] in ["positive", "neutral"]


class TestYouTubeCommandHandler:
    """Test suite for YouTubeCommandHandler class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.handler = YouTubeCommandHandler()
    
    def create_test_analysis(self, success: bool = True) -> VideoAnalysis:
        """Create test analysis object"""
        if success:
            metadata = VideoMetadata(
                video_id="test_id",
                title="Test Video",
                description="Test description",
                channel_name="Test Channel",
                channel_id="UC123",
                published_at="2023-01-01T00:00:00Z",
                duration="10:30",
                view_count=1000,
                like_count=50,
                comment_count=5,
                tags=["test", "demo"],
                category_id="27",
                default_language="en",
                thumbnail_url="https://example.com/thumbnail.jpg"
            )
            
            return VideoAnalysis(
                metadata=metadata,
                transcript="This is a test transcript with sample content.",
                summary="This is a test video for demonstration purposes.",
                key_points=["Point 1", "Point 2", "Point 3"],
                topics=["test", "demo", "tutorial"],
                sentiment="positive",
                technical_content=True,
                processing_time=2.5,
                success=True,
                error_message=None
            )
        else:
            return VideoAnalysis(
                metadata=None,
                transcript=None,
                summary="Analysis failed",
                key_points=[],
                topics=[],
                sentiment="neutral",
                technical_content=False,
                processing_time=1.0,
                success=False,
                error_message="Test error message"
            )
    
    @patch.object(YouTubeAnalyzer, 'analyze_video')
    def test_detailed_output_formatting(self, mock_analyze):
        """Test detailed output formatting"""
        # Mock successful analysis
        mock_analyze.return_value = self.create_test_analysis(success=True)
        
        # Test command handling
        result = asyncio.run(
            self.handler.handle_youtube_command(
                "https://youtu.be/test_id",
                focus="all",
                format="detailed"
            )
        )
        
        # Verify output contains expected sections
        assert "🎥 **Video Analysis**" in result
        assert "Test Video" in result
        assert "Test Channel" in result
        assert "📊 **METADATA**" in result
        assert "📝 **SUMMARY**" in result
        assert "🔑 **KEY POINTS**" in result
        assert "📈 **ASSESSMENT**" in result
        assert "✅ Success" in result
    
    @patch.object(YouTubeAnalyzer, 'analyze_video')
    def test_technical_focus_formatting(self, mock_analyze):
        """Test technical focus output formatting"""
        # Mock successful analysis with technical content
        mock_analyze.return_value = self.create_test_analysis(success=True)
        
        # Test technical focus
        result = asyncio.run(
            self.handler.handle_youtube_command(
                "https://youtu.be/test_id",
                focus="technical",
                format="detailed"
            )
        )
        
        # Verify technical focus content
        assert "🔧 **Technical Analysis**" in result
        assert "🎯 **TECHNICAL ASSESSMENT**" in result
        assert "✅ High technical content detected" in result
        assert "💡 **KEY TECHNICAL CONCEPTS**" in result
    
    @patch.object(YouTubeAnalyzer, 'analyze_video')
    def test_summary_format(self, mock_analyze):
        """Test summary format output"""
        # Mock successful analysis
        mock_analyze.return_value = self.create_test_analysis(success=True)
        
        # Test summary format
        result = asyncio.run(
            self.handler.handle_youtube_command(
                "https://youtu.be/test_id",
                format="summary"
            )
        )
        
        # Verify summary format is concise
        assert "🎥 **Test Video**" in result
        assert "Test Channel" in result
        assert "This is a test video for demonstration purposes." in result
        assert "🏷️ **Topics**" in result
        assert len(result.split("\n")) < 10  # Should be concise
    
    @patch.object(YouTubeAnalyzer, 'analyze_video')
    def test_json_format(self, mock_analyze):
        """Test JSON format output"""
        # Mock successful analysis
        mock_analyze.return_value = self.create_test_analysis(success=True)
        
        # Test JSON format
        result = asyncio.run(
            self.handler.handle_youtube_command(
                "https://youtu.be/test_id",
                format="json"
            )
        )
        
        # Verify JSON format
        assert "```json" in result
        assert "```" in result
        assert '"success": true' in result
        assert '"video_id": "test_id"' in result
        assert '"title": "Test Video"' in result
    
    @patch.object(YouTubeAnalyzer, 'analyze_video')
    def test_error_handling(self, mock_analyze):
        """Test error handling and troubleshooting"""
        # Mock failed analysis
        mock_analyze.return_value = self.create_test_analysis(success=False)
        
        # Test error handling
        result = asyncio.run(
            self.handler.handle_youtube_command("invalid_url")
        )
        
        # Verify error formatting
        assert "❌ **Analysis Failed**" in result
        assert "Test error message" in result
        assert "**Troubleshooting Tips:**" in result
    
    def test_troubleshooting_help_video_id_error(self):
        """Test troubleshooting help for video ID errors"""
        error_message = "Could not extract video ID"
        help_text = self.handler._get_troubleshooting_help(error_message)
        
        assert "**URL Format**" in help_text
        assert "youtu.be" in help_text
        assert "VIDEO_ID" in help_text
    
    def test_troubleshooting_help_unavailable_error(self):
        """Test troubleshooting help for unavailable video errors"""
        error_message = "Video unavailable"
        help_text = self.handler._get_troubleshooting_help(error_message)
        
        assert "**Video Access**" in help_text
        assert "Public" in help_text
        assert "private" in help_text


class TestIntegrationFeatures:
    """Integration tests for YouTube analyzer with AAI components"""
    
    def test_module_imports(self):
        """Test that all modules can be imported successfully"""
        from brain.modules.youtube_analyzer import YouTubeAnalyzer, analyze_youtube_video
        from brain.modules.youtube_command_handler import YouTubeCommandHandler
        
        # Verify classes can be instantiated
        analyzer = YouTubeAnalyzer()
        handler = YouTubeCommandHandler()
        
        assert analyzer is not None
        assert handler is not None
    
    def test_openrouter_integration_mock(self):
        """Test OpenRouter integration (mocked)"""
        with patch('brain.modules.openrouter.router_client.OpenRouterClient') as mock_client:
            analyzer = YouTubeAnalyzer()
            
            # Verify OpenRouter client was attempted to be initialized
            # (May fail if not available, but should handle gracefully)
            assert hasattr(analyzer, 'openrouter_client')
    
    def test_analytics_integration_mock(self):
        """Test analytics integration (mocked)"""
        with patch('brain.modules.unified_analytics.UnifiedAnalyticsClient') as mock_client:
            analyzer = YouTubeAnalyzer()
            
            # Verify analytics client was attempted to be initialized
            assert hasattr(analyzer, 'analytics_client')
    
    def test_environment_variable_handling(self):
        """Test environment variable handling"""
        # Test without API key
        old_key = os.environ.get('YOUTUBE_API_KEY')
        if 'YOUTUBE_API_KEY' in os.environ:
            del os.environ['YOUTUBE_API_KEY']
        
        analyzer = YouTubeAnalyzer()
        assert analyzer.youtube_api_key is None
        assert analyzer.youtube_service is None
        
        # Restore original key if it existed
        if old_key:
            os.environ['YOUTUBE_API_KEY'] = old_key


# Fixtures for testing
@pytest.fixture
def sample_video_metadata():
    """Sample video metadata for testing"""
    return VideoMetadata(
        video_id="dQw4w9WgXcQ",
        title="Rick Astley - Never Gonna Give You Up",
        description="Official video for Never Gonna Give You Up",
        channel_name="Rick Astley",
        channel_id="UCuAXFkgsw1L7xaCfnd5JJOw",
        published_at="2009-10-25T06:57:33Z",
        duration="3:33",
        view_count=1400000000,
        like_count=14000000,
        comment_count=2000000,
        tags=["rick astley", "never gonna give you up", "music"],
        category_id="10",
        default_language="en",
        thumbnail_url="https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
    )


@pytest.fixture
def sample_video_analysis(sample_video_metadata):
    """Sample video analysis for testing"""
    return VideoAnalysis(
        metadata=sample_video_metadata,
        transcript="Never gonna give you up, never gonna let you down...",
        summary="Classic 1987 pop song that became an internet meme phenomenon.",
        key_points=[
            "Iconic 1980s pop song",
            "Became internet meme 'Rickrolling'",
            "Features distinctive dance moves",
            "Over 1 billion views"
        ],
        topics=["music", "1980s", "pop", "meme", "internet culture"],
        sentiment="positive",
        technical_content=False,
        processing_time=2.3,
        success=True,
        error_message=None
    )


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])