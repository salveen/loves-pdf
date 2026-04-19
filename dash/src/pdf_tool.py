from pathlib import Path

from .pdf_merger import PdfMerger
from .pdf_compressor import PdfCompressor, CompressionLevel
from .pdf_splitter import PdfSplitter


class PdfTool:
    def __init__(self):
        self._merger = PdfMerger()
        self._splitter = PdfSplitter()

    def merge(self, input_files: list[Path], output_file: Path) -> Path:
        return self._merger.merge(input_files, output_file)
    
    def split_by_ranges(
        self, 
        input_file: Path, 
        output_dir: Path, 
        page_ranges: list[tuple[int, int]]
    ) -> list[Path]:
        """Split PDF by page ranges."""
        return self._splitter.split_by_pages(input_file, output_dir, page_ranges)
    
    def split_every_n_pages(
        self, 
        input_file: Path, 
        output_dir: Path, 
        pages_per_split: int
    ) -> list[Path]:
        """Split PDF into chunks of N pages."""
        return self._splitter.split_every_n_pages(input_file, output_dir, pages_per_split)
    
    def extract_pages(
        self, 
        input_file: Path, 
        output_file: Path, 
        pages: list[int]
    ) -> Path:
        """Extract specific pages from a PDF."""
        return self._splitter.extract_pages(input_file, output_file, pages)
    
    def get_page_count(self, input_file: Path) -> int:
        """Get the number of pages in a PDF."""
        return self._splitter.get_page_count(input_file)

    def compress(
        self,
        input_file: Path,
        output_file: Path | None = None,
        level: CompressionLevel = CompressionLevel.MEDIUM,
    ) -> Path:
        compressor = PdfCompressor(level)
        return compressor.compress(input_file, output_file)
