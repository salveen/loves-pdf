from pathlib import Path

import fitz


class PdfMerger:
    def merge(self, input_files: list[Path], output_file: Path) -> Path:
        if len(input_files) < 2:
            raise ValueError("At least 2 PDF files are required for merging")

        self._validate_files(input_files)

        result = fitz.open()

        for pdf_path in input_files:
            doc = fitz.open(pdf_path)
            result.insert_pdf(doc)
            doc.close()

        output_file.parent.mkdir(parents=True, exist_ok=True)
        result.save(output_file)
        result.close()

        return output_file

    def _validate_files(self, files: list[Path]) -> None:
        for file in files:
            if not file.exists():
                raise FileNotFoundError(f"File not found: {file}")
            if file.suffix.lower() != ".pdf":
                raise ValueError(f"Not a PDF file: {file}")
