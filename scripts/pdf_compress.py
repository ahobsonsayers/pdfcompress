from pathlib import Path
import tempfile
import img2pdf
import pypdfium2 as pdfium
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


def pdf_to_jpg_to_pdf(
    input_pdf_path: Path,
    output_pdf_path: Path,
    dpi: int,
    quality: int,
):
    scale = dpi / 72.0

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)

        pdf = pdfium.PdfDocument(input_pdf_path)

        image_paths: list[Path] = []
        n_pages = len(pdf)
        for i in range(n_pages):
            page = pdf[i]
            bitmap = page.render(scale=scale, rotation=0)
            image = bitmap.to_pil()

            image_path = temp_dir_path / f"page-{i + 1:04d}.jpg"

            image.save(
                image_path,
                "JPEG",
                quality=quality,
                optimize=True,
            )

            image_paths.append(image_path)

        pdf.close()

        # Convert JPG images back to PDF
        pdf_bytes = img2pdf.convert([str(path) for path in image_paths])
        if pdf_bytes:
            with open(output_pdf_path, "wb") as output_file:
                output_file.write(pdf_bytes)


def print_file_sizes(original_path: Path, compressed_path: Path):
    original_mb = original_path.stat().st_size / (1024 * 1024)
    compressed_mb = compressed_path.stat().st_size / (1024 * 1024)
    reduction = ((original_mb - compressed_mb) / original_mb) * 100

    print(f"Original PDF size: {original_mb:.2f} MB")
    print(f"Compressed PDF size: {compressed_mb:.2f} MB")
    print(f"Size reduction: {reduction:.1f}%")


pdf_to_jpg_to_pdf(
    input_pdf_path,
    output_pdf_path,
    dpi,
    jpg_quality,
)
print_file_sizes(input_pdf_path, output_pdf_path)
