from pathlib import Path
from typing import Optional

import typer

from .pdf_tool import PdfTool
from .pdf_compressor import CompressionLevel

app = typer.Typer(help="PDF Tool - Merge and compress PDF files")


def get_compression_level(level: str) -> CompressionLevel:
    mapping = {
        "low": CompressionLevel.LOW,
        "medium": CompressionLevel.MEDIUM,
        "high": CompressionLevel.HIGH,
        "extreme": CompressionLevel.EXTREME,
    }
    return mapping.get(level.lower(), CompressionLevel.MEDIUM)


@app.command()
def merge(
    files: list[Path] = typer.Argument(..., help="PDF files to merge (at least 2)"),
    output: Path = typer.Option("merged.pdf", "-o", "--output", help="Output file path"),
):
    """Merge multiple PDF files into one."""
    tool = PdfTool()
    try:
        result = tool.merge(files, output)
        typer.echo(f"✓ Merged {len(files)} files into: {result}")
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def compress(
    file: Path = typer.Argument(..., help="PDF file to compress"),
    output: Optional[Path] = typer.Option(None, "-o", "--output", help="Output file path"),
    level: str = typer.Option("medium", "-l", "--level", help="Compression level: low, medium, high, extreme"),
):
    """Compress a PDF file to reduce its size."""
    tool = PdfTool()
    compression = get_compression_level(level)
    
    try:
        input_size = file.stat().st_size
        result = tool.compress(file, output, compression)
        output_size = result.stat().st_size
        reduction = (1 - output_size / input_size) * 100
        
        typer.echo(f"✓ Compressed: {result}")
        typer.echo(f"  Size: {input_size / 1024:.1f}KB → {output_size / 1024:.1f}KB ({reduction:.1f}% reduction)")
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def merge_compress(
    files: list[Path] = typer.Argument(..., help="PDF files to merge and compress"),
    output: Path = typer.Option("merged.pdf", "-o", "--output", help="Output file path"),
    level: str = typer.Option("medium", "-l", "--level", help="Compression level: low, medium, high, extreme"),
):
    """Merge multiple PDF files and compress the result."""
    tool = PdfTool()
    compression = get_compression_level(level)
    
    try:
        result = tool.merge_and_compress(files, output, compression)
        typer.echo(f"✓ Merged and compressed {len(files)} files into: {result}")
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
        raise typer.Exit(1)


def main():
    app()


if __name__ == "__main__":
    main()
