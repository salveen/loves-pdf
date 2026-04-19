from pathlib import Path
from io import BytesIO
from enum import Enum

import fitz
from PIL import Image


class CompressionLevel(Enum):
    LOW = (85, 1.0)
    MEDIUM = (65, 0.85)
    HIGH = (45, 0.7)
    EXTREME = (25, 0.5)

    @property
    def quality(self) -> int:
        return self.value[0]

    @property
    def scale(self) -> float:
        return self.value[1]


class PdfCompressor:
    def __init__(self, compression_level: CompressionLevel = CompressionLevel.MEDIUM):
        self._level = compression_level

    def compress(self, input_file: Path, output_file: Path | None = None) -> Path:
        if not input_file.exists():
            raise FileNotFoundError(f"File not found: {input_file}")

        if output_file is None:
            output_file = input_file.with_stem(f"{input_file.stem}_compressed")

        doc = fitz.open(input_file)

        for page_num in range(len(doc)):
            page = doc[page_num]
            self._compress_page_images(doc, page)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        doc.save(
            output_file,
            garbage=4,
            deflate=True,
            clean=True,
        )
        doc.close()

        return output_file

    def _compress_page_images(self, doc: fitz.Document, page: fitz.Page) -> None:
        image_list = page.get_images(full=True)

        for img_info in image_list:
            xref = img_info[0]
            try:
                self._compress_image(doc, page, xref)
            except Exception:
                pass

    def _compress_image(self, doc: fitz.Document, page: fitz.Page, xref: int) -> None:
        img_data = doc.extract_image(xref)
        if not img_data:
            return

        image_bytes = img_data["image"]
        original_ext = img_data.get("ext", "jpeg")
        
        img = Image.open(BytesIO(image_bytes))
        original_size = len(image_bytes)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        if self._level.scale < 1.0:
            new_size = (int(img.width * self._level.scale), int(img.height * self._level.scale))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=self._level.quality, optimize=True)
        compressed_data = buffer.getvalue()

        if len(compressed_data) >= original_size:
            return

        doc.update_stream(xref, compressed_data, compress=False)
        doc.xref_set_key(xref, "Filter", "/DCTDecode")
        doc.xref_set_key(xref, "ColorSpace", "/DeviceRGB")
        doc.xref_set_key(xref, "Width", str(img.width))
        doc.xref_set_key(xref, "Height", str(img.height))
        doc.xref_set_key(xref, "BitsPerComponent", "8")
        doc.xref_set_key(xref, "Length", str(len(compressed_data)))