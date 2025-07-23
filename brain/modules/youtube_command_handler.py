"""
YouTube Command Handler - Integration with Claude Code Command System
Handles /youtube command routing and response formatting
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

from brain.modules.youtube_analyzer import YouTubeAnalyzer, VideoAnalysis


class YouTubeCommandHandler:
    """
    Command handler for /youtube command integration
    
    Provides formatted output, error handling, and integration
    with Claude Code command system
    """
    
    def __init__(self):
        self.analyzer = YouTubeAnalyzer()
    
    async def handle_youtube_command(self, video_url: str, 
                                   focus: str = "all",
                                   format: str = "detailed",
                                   save: bool = False) -> str:
        """
        Handle /youtube command with various options
        
        Args:
            video_url: YouTube video URL or ID
            focus: Analysis focus (all, technical, summary, transcript, metadata)
            format: Output format (detailed, summary, json)
            save: Whether to save analysis results
            
        Returns:
            Formatted analysis results
        """
        
        try:
            # Perform video analysis
            analysis = await self.analyzer.analyze_video(video_url)
            
            if not analysis.success:
                return f"❌ **Analysis Failed**\n\nError: {analysis.error_message}\n\n" + \
                       self._get_troubleshooting_help(analysis.error_message)
            
            # Format output based on requested format
            if format == "json":
                return self._format_json_output(analysis)
            elif format == "summary":
                return self._format_summary_output(analysis)
            else:  # detailed
                return self._format_detailed_output(analysis, focus)
                
        except Exception as e:
            return f"❌ **Command Error**\n\nUnexpected error: {str(e)}\n\n" + \
                   "Please check the video URL format and try again."
    
    def _format_detailed_output(self, analysis: VideoAnalysis, focus: str) -> str:
        """Format detailed analysis output"""
        
        if focus == "metadata":
            return self._format_metadata_focus(analysis)
        elif focus == "transcript":
            return self._format_transcript_focus(analysis)
        elif focus == "technical":
            return self._format_technical_focus(analysis)
        elif focus == "summary":
            return self._format_summary_focus(analysis)
        else:  # focus == "all"
            return self._format_complete_analysis(analysis)
    
    def _format_complete_analysis(self, analysis: VideoAnalysis) -> str:
        """Format complete video analysis"""
        
        metadata = analysis.metadata
        output = []
        
        # Header
        output.append(f"🎥 **Video Analysis**: \"{metadata.title}\"")
        output.append(f"*Channel: {metadata.channel_name}*")
        output.append("")
        
        # Metadata section
        output.append("📊 **METADATA**")
        output.append(f"• **Duration**: {metadata.duration}")
        output.append(f"• **Views**: {metadata.view_count:,}")
        output.append(f"• **Likes**: {metadata.like_count:,}")
        output.append(f"• **Published**: {metadata.published_at[:10]}")
        if metadata.tags:
            tags_display = ", ".join(metadata.tags[:5])
            if len(metadata.tags) > 5:
                tags_display += f" (+{len(metadata.tags) - 5} more)"
            output.append(f"• **Tags**: {tags_display}")
        output.append("")
        
        # Summary section
        if analysis.summary:
            output.append("📝 **SUMMARY**")
            output.append(analysis.summary)
            output.append("")
        
        # Key points section
        if analysis.key_points:
            output.append("🔑 **KEY POINTS**")
            for point in analysis.key_points:
                output.append(f"• {point}")
            output.append("")
        
        # Topics section
        if analysis.topics:
            topics_display = ", ".join(analysis.topics)
            output.append(f"🏷️ **TOPICS**: [{topics_display}]")
            output.append("")
        
        # Assessment section
        output.append("📈 **ASSESSMENT**")
        output.append(f"• **Technical Content**: {'Yes' if analysis.technical_content else 'No'}")
        output.append(f"• **Sentiment**: {analysis.sentiment.title()}")
        output.append(f"• **Transcript Available**: {'Yes' if analysis.transcript else 'No'}")
        output.append("")
        
        # Processing info
        output.append("⚡ **PROCESSING**")
        output.append(f"• **Analysis Time**: {analysis.processing_time:.2f}s")
        output.append(f"• **Status**: ✅ Success")
        
        return "\n".join(output)
    
    def _format_technical_focus(self, analysis: VideoAnalysis) -> str:
        """Format technical content focus"""
        
        metadata = analysis.metadata
        output = []
        
        # Header
        output.append(f"🔧 **Technical Analysis**: \"{metadata.title}\"")
        output.append("")
        
        # Technical assessment
        if analysis.technical_content:
            output.append("🎯 **TECHNICAL ASSESSMENT**: ✅ High technical content detected")
        else:
            output.append("🎯 **TECHNICAL ASSESSMENT**: ⚠️ Limited technical content detected")
        output.append("")
        
        # Technical concepts (from key points)
        if analysis.key_points:
            output.append("💡 **KEY TECHNICAL CONCEPTS**")
            for point in analysis.key_points:
                output.append(f"• {point}")
            output.append("")
        
        # Topics analysis
        if analysis.topics:
            technical_topics = [t for t in analysis.topics if any(
                keyword in t.lower() for keyword in 
                ['programming', 'code', 'development', 'technical', 'engineering', 'software', 'algorithm']
            )]
            if technical_topics:
                output.append(f"🔬 **TECHNICAL TOPICS**: {', '.join(technical_topics)}")
            else:
                output.append(f"🔬 **TOPICS**: {', '.join(analysis.topics)}")
            output.append("")
        
        # Additional technical metadata
        duration_parts = metadata.duration.split(":")
        if len(duration_parts) >= 2:
            try:
                total_minutes = int(duration_parts[0]) * 60 + int(duration_parts[1])
                if len(duration_parts) == 3:
                    total_minutes = int(duration_parts[0]) * 60 + int(duration_parts[1])
                
                if total_minutes > 30:
                    depth_assessment = "In-depth tutorial (30+ minutes)"
                elif total_minutes > 15:
                    depth_assessment = "Comprehensive overview (15-30 minutes)"
                else:
                    depth_assessment = "Quick tutorial/demo (<15 minutes)"
                    
                output.append(f"📊 **CONTENT DEPTH**: {depth_assessment}")
            except:
                pass
        
        # Transcript availability for technical analysis
        if analysis.transcript:
            output.append("📄 **TRANSCRIPT**: Available for detailed technical analysis")
        else:
            output.append("📄 **TRANSCRIPT**: Not available - analysis based on metadata only")
        
        return "\n".join(output)
    
    def _format_transcript_focus(self, analysis: VideoAnalysis) -> str:
        """Format transcript-focused output"""
        
        metadata = analysis.metadata
        output = []
        
        # Header
        output.append(f"📄 **Transcript Analysis**: \"{metadata.title}\"")
        output.append("")
        
        if analysis.transcript:
            # Transcript stats
            word_count = len(analysis.transcript.split())
            char_count = len(analysis.transcript)
            estimated_reading_time = max(1, word_count // 200)  # ~200 WPM reading speed
            
            output.append("📊 **TRANSCRIPT STATISTICS**")
            output.append(f"• **Length**: {char_count:,} characters")
            output.append(f"• **Word Count**: ~{word_count:,} words")
            output.append(f"• **Reading Time**: ~{estimated_reading_time} minutes")
            output.append(f"• **Language**: Auto-detected")
            output.append("")
            
            # Transcript preview
            preview = analysis.transcript[:500]
            if len(analysis.transcript) > 500:
                preview += "..."
            
            output.append("🔍 **TRANSCRIPT PREVIEW**")
            output.append(f"```\n{preview}\n```")
            output.append("")
            
            # Analysis based on transcript
            if analysis.summary:
                output.append("📝 **CONTENT ANALYSIS**")
                output.append(analysis.summary)
        else:
            output.append("❌ **TRANSCRIPT NOT AVAILABLE**")
            output.append("")
            output.append("**Possible reasons:**")
            output.append("• Video has automatic captions disabled")
            output.append("• Content is primarily visual (music, art, etc.)")
            output.append("• Video is too new (transcripts still processing)")
            output.append("• Video language not supported by YouTube's automatic captioning")
            output.append("")
            output.append("📊 **ALTERNATIVE ANALYSIS** (based on metadata)")
            if analysis.summary:
                output.append(analysis.summary)
        
        return "\n".join(output)
    
    def _format_summary_output(self, analysis: VideoAnalysis) -> str:
        """Format concise summary output"""
        
        metadata = analysis.metadata
        output = []
        
        # Compact header
        output.append(f"🎥 **{metadata.title}** ({metadata.duration})")
        output.append(f"*{metadata.channel_name} • {metadata.view_count:,} views*")
        output.append("")
        
        # Summary
        if analysis.summary:
            output.append(analysis.summary)
        else:
            output.append("Summary not available - analysis incomplete.")
        
        # Key topics
        if analysis.topics:
            topics_display = ", ".join(analysis.topics[:3])
            if len(analysis.topics) > 3:
                topics_display += f" (+{len(analysis.topics) - 3} more)"
            output.append(f"\n🏷️ **Topics**: {topics_display}")
        
        return "\n".join(output)
    
    def _format_json_output(self, analysis: VideoAnalysis) -> str:
        """Format JSON output for programmatic use"""
        
        data = {
            "success": analysis.success,
            "processing_time": analysis.processing_time,
            "metadata": {
                "video_id": analysis.metadata.video_id,
                "title": analysis.metadata.title,
                "channel_name": analysis.metadata.channel_name,
                "duration": analysis.metadata.duration,
                "view_count": analysis.metadata.view_count,
                "like_count": analysis.metadata.like_count,
                "published_at": analysis.metadata.published_at,
                "tags": analysis.metadata.tags
            },
            "analysis": {
                "summary": analysis.summary,
                "key_points": analysis.key_points,
                "topics": analysis.topics,
                "technical_content": analysis.technical_content,
                "sentiment": analysis.sentiment,
                "has_transcript": analysis.transcript is not None
            },
            "transcript_length": len(analysis.transcript) if analysis.transcript else 0
        }
        
        return f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```"
    
    def _get_troubleshooting_help(self, error_message: str) -> str:
        """Provide troubleshooting help based on error message"""
        
        help_text = "**Troubleshooting Tips:**\n\n"
        
        if "video ID" in error_message.lower():
            help_text += "• **URL Format**: Try these formats:\n" + \
                        "  - `https://youtu.be/VIDEO_ID`\n" + \
                        "  - `https://www.youtube.com/watch?v=VIDEO_ID`\n" + \
                        "  - `VIDEO_ID` (11 character ID only)\n\n"
        
        if "unavailable" in error_message.lower() or "not found" in error_message.lower():
            help_text += "• **Video Access**: Check if video is:\n" + \
                        "  - Public (not private or unlisted)\n" + \
                        "  - Still available (not deleted)\n" + \
                        "  - Accessible from your region\n\n"
        
        if "api" in error_message.lower():
            help_text += "• **API Issues**: \n" + \
                        "  - Check YOUTUBE_API_KEY in environment\n" + \
                        "  - Verify API key has YouTube Data API v3 enabled\n" + \
                        "  - Check API quota limits\n\n"
        
        help_text += "• **Still having issues?** Try with a different video or contact support."
        
        return help_text
    
    def _format_metadata_focus(self, analysis: VideoAnalysis) -> str:
        """Format metadata-focused output"""
        
        metadata = analysis.metadata
        output = []
        
        # Header
        output.append(f"📊 **Metadata Analysis**: \"{metadata.title}\"")
        output.append("")
        
        # Complete metadata
        output.append("🎯 **VIDEO INFORMATION**")
        output.append(f"• **Video ID**: `{metadata.video_id}`")
        output.append(f"• **Title**: {metadata.title}")
        output.append(f"• **Channel**: {metadata.channel_name}")
        output.append(f"• **Channel ID**: `{metadata.channel_id}`")
        output.append(f"• **Published**: {metadata.published_at}")
        output.append(f"• **Duration**: {metadata.duration}")
        output.append("")
        
        output.append("📈 **STATISTICS**")
        output.append(f"• **Views**: {metadata.view_count:,}")
        output.append(f"• **Likes**: {metadata.like_count:,}")
        output.append(f"• **Comments**: {metadata.comment_count:,}")
        
        # Engagement rate calculation
        if metadata.view_count > 0:
            like_rate = (metadata.like_count / metadata.view_count) * 100
            comment_rate = (metadata.comment_count / metadata.view_count) * 100
            output.append(f"• **Like Rate**: {like_rate:.2f}%")
            output.append(f"• **Comment Rate**: {comment_rate:.2f}%")
        
        output.append("")
        
        # Tags and categorization
        if metadata.tags:
            output.append("🏷️ **TAGS**")
            for i, tag in enumerate(metadata.tags[:10], 1):
                output.append(f"  {i}. {tag}")
            if len(metadata.tags) > 10:
                output.append(f"  ... and {len(metadata.tags) - 10} more tags")
            output.append("")
        
        # Technical metadata
        output.append("🔧 **TECHNICAL DETAILS**")
        output.append(f"• **Category ID**: {metadata.category_id}")
        if metadata.default_language:
            output.append(f"• **Language**: {metadata.default_language}")
        if metadata.thumbnail_url:
            output.append(f"• **Thumbnail**: Available")
        
        return "\n".join(output)
    
    def _format_summary_focus(self, analysis: VideoAnalysis) -> str:
        """Format summary-focused output"""
        
        metadata = analysis.metadata
        output = []
        
        # Header
        output.append(f"📝 **Content Summary**: \"{metadata.title}\"")
        output.append(f"*{metadata.channel_name} • {metadata.duration}*")
        output.append("")
        
        # Main summary
        if analysis.summary:
            output.append("**SUMMARY**")
            output.append(analysis.summary)
            output.append("")
        
        # Key insights
        if analysis.key_points:
            output.append("**KEY INSIGHTS**")
            for i, point in enumerate(analysis.key_points[:5], 1):
                output.append(f"{i}. {point}")
            output.append("")
        
        # Content characteristics
        output.append("**CONTENT CHARACTERISTICS**")
        output.append(f"• **Type**: {'Technical/Educational' if analysis.technical_content else 'General Content'}")
        output.append(f"• **Tone**: {analysis.sentiment.title()}")
        output.append(f"• **Analysis Depth**: {'With transcript' if analysis.transcript else 'Metadata-based'}")
        
        return "\n".join(output)

# Export for easy import
__all__ = ['YouTubeCommandHandler']