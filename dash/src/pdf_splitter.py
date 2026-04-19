from pathlib import Path

import fitz


class PdfSplitter:
    def split_by_pages(
        self, 
        input_file: Path, 
        output_dir: Path, 
        page_ranges: list[tuple[int, int]]
    ) -> list[Path]:
        """
        Split a PDF into multiple files based on page ranges.
        
        Args:
            input_file: Path to the input PDF file
            output_dir: Directory where split files will be saved
            page_ranges: List of tuples (start_page, end_page), 1-indexed inclusive
            
        Returns:
            List of paths to the created PDF files
        """
        self._validate_file(input_file)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        doc = fitz.open(input_file)
        total_pages = len(doc)
        output_files = []
        
        for idx, (start, end) in enumerate(page_ranges):
            # Convert to 0-indexed
            start_idx = start - 1
            end_idx = end - 1
            
            if start_idx < 0 or end_idx >= total_pages or start_idx > end_idx:
                doc.close()
                raise ValueError(
                    f"Invalid page range ({start}-{end}). "
                    f"Document has {total_pages} pages."
                )
            
            # Create new document with selected pages
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=start_idx, to_page=end_idx)
            
            # Generate output filename
            stem = input_file.stem
            if len(page_ranges) == 1:
                output_name = f"{stem}_pages_{start}-{end}.pdf"
            else:
                output_name = f"{stem}_part{idx + 1}_pages_{start}-{end}.pdf"
            
            output_path = output_dir / output_name
            new_doc.save(output_path)
            new_doc.close()
            output_files.append(output_path)
        
        doc.close()
        return output_files
    
    def split_every_n_pages(
        self, 
        input_file: Path, 
        output_dir: Path, 
        pages_per_split: int
    ) -> list[Path]:
        """
        Split a PDF into multiple files with N pages each.
        
        Args:
            input_file: Path to the input PDF file
            output_dir: Directory where split files will be saved
            pages_per_split: Number of pages per output file
            
        Returns:
            List of paths to the created PDF files
        """
        self._validate_file(input_file)
        
        if pages_per_split < 1:
            raise ValueError("Pages per split must be at least 1")
        
        doc = fitz.open(input_file)
        total_pages = len(doc)
        doc.close()
        
        # Generate page ranges
        page_ranges = []
        for start in range(1, total_pages + 1, pages_per_split):
            end = min(start + pages_per_split - 1, total_pages)
            page_ranges.append((start, end))
        
        return self.split_by_pages(input_file, output_dir, page_ranges)
    
    def extract_pages(
        self, 
        input_file: Path, 
        output_file: Path, 
        pages: list[int]
    ) -> Path:
        """
        Extract specific pages from a PDF into a new file.
        
        Args:
            input_file: Path to the input PDF file
            output_file: Path for the output PDF file
            pages: List of page numbers to extract (1-indexed)
            
        Returns:
            Path to the created PDF file
        """
        self._validate_file(input_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        doc = fitz.open(input_file)
        total_pages = len(doc)
        
        # Validate pages
        for page in pages:
            if page < 1 or page > total_pages:
                doc.close()
                raise ValueError(
                    f"Invalid page number {page}. "
                    f"Document has {total_pages} pages."
                )
        
        new_doc = fitz.open()
        for page in pages:
            new_doc.insert_pdf(doc, from_page=page - 1, to_page=page - 1)
        
        new_doc.save(output_file)
        new_doc.close()
        doc.close()
        
        return output_file
    
    def get_page_count(self, input_file: Path) -> int:
        """Get the number of pages in a PDF file."""
        self._validate_file(input_file)
        doc = fitz.open(input_file)
        count = len(doc)
        doc.close()
        return count

    def _validate_file(self, file: Path) -> None:
        if not file.exists():
            raise FileNotFoundError(f"File not found: {file}")
        if file.suffix.lower() != ".pdf":
            raise ValueError(f"Not a PDF file: {file}")
