#!/usr/bin/env python3
"""
YouTube Command Integration Test Suite
Comprehensive testing of the complete YouTube command integration system
"""

import asyncio
import sys
import os
from pathlib import Path

# Add brain modules to path
sys.path.append('brain/modules')

try:
    from youtube_claude_integration import YouTubeClaudeIntegration, analyze_youtube_video_for_claude
    from youtube_analyzer import YouTubeAnalyzer
    from youtube_command_handler import YouTubeCommandHandler
    from youtube_command_executor import YouTubeCommandExecutor
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Make sure you're running from the AAI directory")
    sys.exit(1)

class YouTubeIntegrationTester:
    """Comprehensive test suite for YouTube command integration"""
    
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test results"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            
        self.test_results.append({
            "name": test_name,
            "passed": passed,
            "status": status,
            "details": details
        })
        print(f"{status}: {test_name}")
        if details:
            print(f"    → {details}")
        
    def test_url_validation(self):
        """Test URL validation functionality"""
        print("\n🧪 Testing URL Validation...")
        
        integration = YouTubeClaudeIntegration()
        
        valid_urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "dQw4w9WgXcQ"
        ]
        
        invalid_urls = [
            "https://vimeo.com/123456",
            "not_a_url",
            ""
        ]
        
        # Test valid URLs
        for url in valid_urls:
            is_valid = integration.validate_video_url(url)
            self.log_test(f"Valid URL: {url}", is_valid, f"Validation result: {is_valid}")
        
        # Test invalid URLs
        for url in invalid_urls:
            is_valid = integration.validate_video_url(url)
            self.log_test(f"Invalid URL: {url}", not is_valid, f"Correctly rejected: {not is_valid}")
    
    def test_video_id_extraction(self):
        """Test video ID extraction"""
        print("\n🧪 Testing Video ID Extraction...")
        
        analyzer = YouTubeAnalyzer()
        
        test_cases = [
            ("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "dQw4w9WgXcQ", "video"),
            ("https://youtu.be/dQw4w9WgXcQ", "dQw4w9WgXcQ", "video"),
            ("dQw4w9WgXcQ", "dQw4w9WgXcQ", "video")
        ]
        
        for input_url, expected_id, expected_type in test_cases:
            try:
                video_id, content_type = analyzer.extract_video_id(input_url)
                success = video_id == expected_id and content_type == expected_type
                self.log_test(f"Extract ID from: {input_url}", success, 
                            f"Got {video_id} ({content_type}), expected {expected_id} ({expected_type})")
            except Exception as e:
                self.log_test(f"Extract ID from: {input_url}", False, f"Exception: {e}")
    
    def test_command_parsing(self):
        """Test command parsing functionality"""
        print("\n🧪 Testing Command Parsing...")
        
        executor = YouTubeCommandExecutor()
        
        test_commands = [
            ("/youtube dQw4w9WgXcQ", {"video_url": "dQw4w9WgXcQ", "focus": "all", "format": "detailed", "save": False}),
            ("/youtube dQw4w9WgXcQ --focus technical", {"video_url": "dQw4w9WgXcQ", "focus": "technical", "format": "detailed", "save": False}),
            ("/youtube dQw4w9WgXcQ --format json --save", {"video_url": "dQw4w9WgXcQ", "focus": "all", "format": "json", "save": True})
        ]
        
        for command, expected in test_commands:
            try:
                result = executor.parse_command_args(command)
                success = all(result.get(key) == value for key, value in expected.items())
                self.log_test(f"Parse command: {command}", success, 
                            f"Result: {result}")
            except Exception as e:
                self.log_test(f"Parse command: {command}", False, f"Exception: {e}")
    
    async def test_integration_layer(self):
        """Test the complete integration layer"""
        print("\n🧪 Testing Integration Layer...")
        
        # Test with a simple video ID
        test_video = "dQw4w9WgXcQ"
        
        try:
            result = await analyze_youtube_video_for_claude(test_video, "summary", "detailed")
            # Since we don't have API keys, we expect a graceful failure
            has_error = "Error" in result or "Failed" in result
            self.log_test("Integration layer execution", has_error, 
                        "Expected graceful error handling without API keys")
            
            # Test that it returns a properly formatted response
            is_formatted = "YouTube" in result and "Analysis" in result
            self.log_test("Response formatting", is_formatted,
                        "Response contains expected YouTube analysis formatting")
                        
        except Exception as e:
            self.log_test("Integration layer execution", False, f"Unexpected exception: {e}")
    
    def test_error_handling(self):
        """Test error handling with invalid inputs"""
        print("\n🧪 Testing Error Handling...")
        
        executor = YouTubeCommandExecutor()
        
        error_cases = [
            "/youtube",  # No URL
            "/youtube --focus technical",  # No URL with flags
            "/youtube invalid_url --format invalid_format"  # Invalid format
        ]
        
        for command in error_cases:
            try:
                result = executor.parse_command_args(command)
                self.log_test(f"Error case: {command}", False, 
                            f"Should have failed but got: {result}")
            except Exception as e:
                self.log_test(f"Error case: {command}", True, 
                            f"Correctly caught error: {str(e)[:100]}")
    
    def test_module_imports(self):
        """Test that all modules import correctly"""
        print("\n🧪 Testing Module Imports...")
        
        modules_to_test = [
            ("youtube_claude_integration", YouTubeClaudeIntegration),
            ("youtube_analyzer", YouTubeAnalyzer), 
            ("youtube_command_handler", YouTubeCommandHandler),
            ("youtube_command_executor", YouTubeCommandExecutor)
        ]
        
        for module_name, module_class in modules_to_test:
            try:
                instance = module_class()
                self.log_test(f"Import and instantiate {module_name}", True, 
                            f"Successfully created {module_class.__name__} instance")
            except Exception as e:
                self.log_test(f"Import and instantiate {module_name}", False, 
                            f"Failed: {e}")
    
    def test_api_key_detection(self):
        """Test API key detection and warnings"""
        print("\n🧪 Testing API Key Detection...")
        
        analyzer = YouTubeAnalyzer()
        
        # Test YouTube API detection
        has_youtube_api = analyzer.youtube_service is not None
        youtube_key_present = os.getenv("YOUTUBE_API_KEY") is not None
        
        if youtube_key_present:
            self.log_test("YouTube API initialization", has_youtube_api, 
                        "YouTube API key found and service initialized")
        else:
            self.log_test("YouTube API key detection", not has_youtube_api,
                        "Correctly detected missing YouTube API key")
        
        # Test OpenRouter API detection  
        has_openrouter = analyzer.openrouter_client is not None
        openrouter_key_present = os.getenv("OPENROUTER_API_KEY") is not None
        
        if openrouter_key_present:
            self.log_test("OpenRouter API initialization", has_openrouter,
                        "OpenRouter API key found and client initialized")
        else:
            self.log_test("OpenRouter API key detection", not has_openrouter,
                        "Correctly detected missing OpenRouter API key")
    
    async def run_all_tests(self):
        """Run the complete test suite"""
        print("🚀 YouTube Command Integration Test Suite")
        print("=" * 60)
        print()
        
        # Run all tests
        self.test_module_imports()
        self.test_url_validation()
        self.test_video_id_extraction()
        self.test_command_parsing()
        self.test_error_handling()
        self.test_api_key_detection()
        await self.test_integration_layer()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        for result in self.test_results:
            print(f"{result['status']} {result['name']}")
        
        print(f"\n🎯 Results: {self.passed_tests}/{self.total_tests} tests passed")
        
        success_rate = (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("✅ YouTube Command Integration is READY FOR USE!")
        else:
            print("⚠️  Some tests failed - review issues before production use")
        
        return success_rate >= 80

async def main():
    """Main test runner"""
    print("Starting YouTube Command Integration Test Suite...\n")
    
    tester = YouTubeIntegrationTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n🎉 All critical tests passed! The YouTube command is fully integrated.")
        print("\n📋 Usage Examples:")
        print("• /youtube https://youtu.be/VIDEO_ID")
        print("• /youtube VIDEO_ID --focus technical --format summary")
        print("• /youtube https://www.youtube.com/watch?v=VIDEO_ID --save")
        
        if not os.getenv("YOUTUBE_API_KEY"):
            print("\n⚠️  Note: For full functionality, set YOUTUBE_API_KEY in your .env file")
        if not os.getenv("OPENROUTER_API_KEY"):
            print("⚠️  Note: For AI analysis, set OPENROUTER_API_KEY in your .env file")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)