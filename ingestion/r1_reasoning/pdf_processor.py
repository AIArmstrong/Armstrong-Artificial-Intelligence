"""
PDF Document Processor for R1 Reasoning Engine

Extracts text and metadata from PDF documents with
quality assessment and AAI confidence scoring.
"""
import os
import logging
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

# PDF processing with fallback
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    try:
        import fitz  # PyMuPDF
        PDF_AVAILABLE = True
        USE_PYMUPDF = True
    except ImportError:
        PDF_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class PDFMetadata:
    """Metadata extracted from PDF"""
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    creator: Optional[str] = None
    producer: Optional[str] = None
    creation_date: Optional[datetime] = None
    modification_date: Optional[datetime] = None
    page_count: int = 0
    file_size_bytes: int = 0
    extraction_confidence: float = 0.70  # AAI minimum


@dataclass
class PDFExtractionResult:
    """Result of PDF text extraction"""
    success: bool
    text_content: str
    metadata: PDFMetadata
    quality_score: float = 0.70  # AAI compliant
    confidence_score: float = 0.70  # AAI compliant
    processing_time_ms: int = 0
    error_message: Optional[str] = None
    pages_processed: int = 0
    extraction_method: str = "unknown"


class PDFProcessor:
    """
    PDF document processor with AAI patterns.
    
    Features:
    - Multi-library PDF processing (PyPDF2, PyMuPDF)
    - Metadata extraction and preservation
    - Quality assessment and confidence scoring
    - Error handling with graceful degradation
    - Page-by-page processing for large documents
    """
    
    def __init__(self, 
                 min_confidence_threshold: float = 0.70,
                 quality_threshold: float = 0.50):
        """Initialize PDF processor"""
        self.min_confidence_threshold = min_confidence_threshold
        self.quality_threshold = quality_threshold
        
        # Check available PDF libraries
        self.available_libraries = self._check_available_libraries()
        
        if not self.available_libraries:
            logger.warning("No PDF processing libraries available. Install PyPDF2 or PyMuPDF.")
    
    def _check_available_libraries(self) -> List[str]:
        """Check which PDF libraries are available"""
        libraries = []
        
        try:
            import PyPDF2
            libraries.append("PyPDF2")
        except ImportError:
            pass
        
        try:
            import fitz
            libraries.append("PyMuPDF")
        except ImportError:
            pass
        
        return libraries
    
    async def extract_from_pdf(self, file_path: str) -> PDFExtractionResult:
        """
        Extract text and metadata from PDF file.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            PDFExtractionResult with extracted content and metadata
        """
        start_time = datetime.now()
        
        if not self.available_libraries:
            return PDFExtractionResult(
                success=False,
                text_content="",
                metadata=PDFMetadata(),
                error_message="No PDF processing libraries available"
            )
        
        # Validate file
        if not self._validate_pdf_file(file_path):
            return PDFExtractionResult(
                success=False,
                text_content="",
                metadata=PDFMetadata(),
                error_message=f"Invalid PDF file: {file_path}"
            )
        
        # Try extraction with available libraries
        for library in self.available_libraries:
            try:
                if library == "PyPDF2":
                    result = await self._extract_with_pypdf2(file_path)
                elif library == "PyMuPDF":
                    result = await self._extract_with_pymupdf(file_path)
                
                if result.success:
                    # Calculate processing time
                    processing_time = (datetime.now() - start_time).total_seconds() * 1000
                    result.processing_time_ms = int(processing_time)
                    result.extraction_method = library
                    
                    # Enhance with quality assessment
                    result = self._assess_extraction_quality(result)
                    
                    return result
                    
            except Exception as e:
                logger.warning(f"PDF extraction failed with {library}: {e}")
                continue
        
        # All extraction methods failed
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        return PDFExtractionResult(
            success=False,
            text_content="",
            metadata=PDFMetadata(),
            processing_time_ms=int(processing_time),
            error_message="All PDF extraction methods failed"
        )
    
    def _validate_pdf_file(self, file_path: str) -> bool:
        """Validate PDF file exists and is readable"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                logger.error(f"PDF file not found: {file_path}")
                return False
            
            if not path.is_file():
                logger.error(f"Path is not a file: {file_path}")
                return False
            
            if path.suffix.lower() != '.pdf':
                logger.warning(f"File extension is not .pdf: {file_path}")
            
            if path.stat().st_size == 0:
                logger.error(f"PDF file is empty: {file_path}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"PDF file validation failed: {e}")
            return False
    
    async def _extract_with_pypdf2(self, file_path: str) -> PDFExtractionResult:
        """Extract PDF content using PyPDF2"""
        try:
            import PyPDF2
            
            text_content = ""
            metadata = PDFMetadata()
            pages_processed = 0
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract metadata
                if pdf_reader.metadata:
                    metadata.title = pdf_reader.metadata.get('/Title')
                    metadata.author = pdf_reader.metadata.get('/Author')
                    metadata.subject = pdf_reader.metadata.get('/Subject')
                    metadata.creator = pdf_reader.metadata.get('/Creator')
                    metadata.producer = pdf_reader.metadata.get('/Producer')
                    
                    # Handle dates
                    creation_date = pdf_reader.metadata.get('/CreationDate')
                    if creation_date:
                        try:
                            metadata.creation_date = datetime.strptime(creation_date, "D:%Y%m%d%H%M%S%z")
                        except (ValueError, TypeError) as e:
                            logging.debug(f"Could not parse PDF creation date {creation_date}: {e}")
                            pass
                
                metadata.page_count = len(pdf_reader.pages)
                metadata.file_size_bytes = Path(file_path).stat().st_size
                
                # Extract text from all pages
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text_content += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                            pages_processed += 1
                    except Exception as e:
                        logger.warning(f"Failed to extract text from page {page_num + 1}: {e}")
                        continue
            
            # Calculate confidence based on extraction success
            confidence_score = self._calculate_extraction_confidence(
                pages_processed, metadata.page_count, len(text_content)
            )
            metadata.extraction_confidence = confidence_score
            
            return PDFExtractionResult(
                success=bool(text_content.strip()),
                text_content=text_content.strip(),
                metadata=metadata,
                confidence_score=confidence_score,
                pages_processed=pages_processed
            )
            
        except Exception as e:
            logger.error(f"PyPDF2 extraction failed: {e}")
            return PDFExtractionResult(
                success=False,
                text_content="",
                metadata=PDFMetadata(),
                error_message=str(e)
            )
    
    async def _extract_with_pymupdf(self, file_path: str) -> PDFExtractionResult:
        """Extract PDF content using PyMuPDF (fitz)"""
        try:
            import fitz
            
            text_content = ""
            metadata = PDFMetadata()
            pages_processed = 0
            
            # Open PDF document
            pdf_document = fitz.open(file_path)
            
            # Extract metadata
            pdf_metadata = pdf_document.metadata
            if pdf_metadata:
                metadata.title = pdf_metadata.get('title')
                metadata.author = pdf_metadata.get('author')
                metadata.subject = pdf_metadata.get('subject')
                metadata.creator = pdf_metadata.get('creator')
                metadata.producer = pdf_metadata.get('producer')
                
                # Handle dates
                creation_date = pdf_metadata.get('creationDate')
                if creation_date:
                    try:
                        metadata.creation_date = datetime.fromisoformat(creation_date.replace('Z', '+00:00'))
                    except (ValueError, TypeError, AttributeError) as e:
                        logging.debug(f"Could not parse ISO format creation date {creation_date}: {e}")
                        pass
            
            metadata.page_count = pdf_document.page_count
            metadata.file_size_bytes = Path(file_path).stat().st_size
            
            # Extract text from all pages
            for page_num in range(pdf_document.page_count):
                try:
                    page = pdf_document[page_num]
                    page_text = page.get_text()
                    
                    if page_text:
                        text_content += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                        pages_processed += 1
                        
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {page_num + 1}: {e}")
                    continue
            
            pdf_document.close()
            
            # Calculate confidence based on extraction success
            confidence_score = self._calculate_extraction_confidence(
                pages_processed, metadata.page_count, len(text_content)
            )
            metadata.extraction_confidence = confidence_score
            
            return PDFExtractionResult(
                success=bool(text_content.strip()),
                text_content=text_content.strip(),
                metadata=metadata,
                confidence_score=confidence_score,
                pages_processed=pages_processed
            )
            
        except Exception as e:
            logger.error(f"PyMuPDF extraction failed: {e}")
            return PDFExtractionResult(
                success=False,
                text_content="",
                metadata=PDFMetadata(),
                error_message=str(e)
            )
    
    def _calculate_extraction_confidence(self,
                                       pages_processed: int,
                                       total_pages: int,
                                       text_length: int) -> float:
        """Calculate AAI-compliant confidence score for extraction"""
        
        base_confidence = 0.70  # AAI minimum
        
        # Page processing success rate
        if total_pages > 0:
            page_success_rate = pages_processed / total_pages
            base_confidence += page_success_rate * 0.15
        
        # Text content length (more text generally means better extraction)
        if text_length > 1000:
            base_confidence += 0.05
        if text_length > 5000:
            base_confidence += 0.03
        if text_length > 10000:
            base_confidence += 0.02
        
        # Ensure within AAI range
        return max(0.70, min(0.95, base_confidence))
    
    def _assess_extraction_quality(self, result: PDFExtractionResult) -> PDFExtractionResult:
        """Assess and enhance extraction quality metrics"""
        
        if not result.success:
            result.quality_score = 0.0
            return result
        
        quality_score = 0.50  # Base quality
        
        # Text content quality indicators
        text = result.text_content.lower()
        
        # Check for structure indicators
        structure_indicators = [
            'chapter', 'section', 'introduction', 'conclusion',
            'abstract', 'summary', 'table', 'figure'
        ]
        
        structure_count = sum(1 for indicator in structure_indicators if indicator in text)
        quality_score += min(0.2, structure_count * 0.02)
        
        # Check for technical content indicators
        technical_indicators = [
            'analysis', 'research', 'study', 'method', 'result',
            'data', 'algorithm', 'system', 'implementation'
        ]
        
        technical_count = sum(1 for indicator in technical_indicators if indicator in text)
        quality_score += min(0.15, technical_count * 0.015)
        
        # Penalize for common extraction errors
        error_indicators = [
            'â€™', 'â€œ', 'â€', '?????', '□', '■'  # Common encoding issues
        ]
        
        error_count = sum(1 for indicator in error_indicators if indicator in text)
        quality_score -= min(0.2, error_count * 0.05)
        
        # Page coverage factor
        if result.metadata.page_count > 0:
            page_coverage = result.pages_processed / result.metadata.page_count
            quality_score += page_coverage * 0.1
        
        # Text density (characters per page)
        if result.pages_processed > 0:
            text_density = len(result.text_content) / result.pages_processed
            if text_density > 500:  # Good density
                quality_score += 0.05
            elif text_density < 100:  # Poor density
                quality_score -= 0.05
        
        result.quality_score = max(0.0, min(1.0, quality_score))
        
        # Adjust confidence based on quality
        confidence_adjustment = (result.quality_score - 0.5) * 0.1
        result.confidence_score = max(0.70, min(0.95, result.confidence_score + confidence_adjustment))
        
        return result
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported document formats"""
        return ['.pdf'] if self.available_libraries else []
    
    def get_processor_status(self) -> Dict[str, Any]:
        """Get processor status and capabilities"""
        return {
            "available_libraries": self.available_libraries,
            "supported_formats": self.get_supported_formats(),
            "min_confidence_threshold": self.min_confidence_threshold,
            "quality_threshold": self.quality_threshold,
            "ready": bool(self.available_libraries)
        }


async def test_pdf_processor():
    """Test PDF processor functionality"""
    import tempfile
    
    processor = PDFProcessor()
    
    print("🧪 Testing PDF Processor")
    print("=" * 30)
    
    # Check processor status
    status = processor.get_processor_status()
    print(f"Available libraries: {status['available_libraries']}")
    print(f"Supported formats: {status['supported_formats']}")
    print(f"Ready: {status['ready']}")
    
    if not status['ready']:
        print("❌ PDF processor not ready - no libraries available")
        print("Install PyPDF2 or PyMuPDF to enable PDF processing")
        return
    
    # Create a simple test PDF (would need actual PDF for real test)
    print("\n📄 For full testing, provide a PDF file path")
    print("Example usage:")
    print("  result = await processor.extract_from_pdf('/path/to/document.pdf')")
    print("  print(f'Success: {result.success}')")
    print("  print(f'Pages: {result.pages_processed}')")
    print("  print(f'Confidence: {result.confidence_score:.2%}')")
    print("  print(f'Quality: {result.quality_score:.2%}')")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_pdf_processor())