from pathlib import Path
import pymupdf
import sys

if len(sys.argv) != 5:
    print(f"Usage: {sys.argv[0]} <input-pdf> <output-pdf> <dpi> <jpg-quality>")
    sys.exit(1)

input_pdf_path = Path(sys.argv[1])
output_pdf_path = Path(sys.argv[2])
dpi = int(sys.argv[3])
jpg_quality = int(sys.argv[4])

if not input_pdf_path.exists():
    raise FileNotFoundError(f"pdf not found: {input_pdf_path}")


def compress_pdf_images(
    input_pdf_path: Path,
    output_pdf_path: Path,
    dpi: int,
    quality: int,
):
    doc = pymupdf.open(input_pdf_path)

    # Compress images using PyMuPDF's built-in method
    doc.rewrite_images(
        dpi_threshold=dpi + 1,
        dpi_target=dpi,
        quality=quality,
        lossy=True,
        lossless=True,
        bitonal=True,
        color=True,
        gray=True,
        set_to_gray=False,
    )

    doc.save(
        output_pdf_path,
        garbage=4,
        clean=True,
        deflate=True,
        deflate_images=True,
        deflate_fonts=True,
        use_objstms=True,
    )

    doc.close()


def print_file_sizes(original_path: Path, compressed_path: Path):
    original_mb = original_path.stat().st_size / (1024 * 1024)
    compressed_mb = compressed_path.stat().st_size / (1024 * 1024)
    reduction = ((original_mb - compressed_mb) / original_mb) * 100

    print(f"Original PDF size: {original_mb:.2f} MB")
    print(f"Compressed PDF size: {compressed_mb:.2f} MB")
    print(f"Size reduction: {reduction:.1f}%")


compress_pdf_images(
    input_pdf_path,
    output_pdf_path,
    dpi,
    jpg_quality,
)
print_file_sizes(input_pdf_path, output_pdf_path)
