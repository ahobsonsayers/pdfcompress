from pathlib import Path
import shutil
import img2pdf
import pypdfium2 as pdfium

FILES_DIR = Path("./files")
PDF_PATH = FILES_DIR / "input.pdf"

DPI = 300
JPG_QUALITY = 68

pdf_path = Path(PDF_PATH)
if not pdf_path.exists():
    raise FileNotFoundError(f"PDF not found: {pdf_path}")

jpg_dir = FILES_DIR / "jpg"
png_dir = FILES_DIR / "png"


def pdf_to_jpg(
    pdf_path: Path,
    output_dir_path: Path,
    dpi: int,
    quality: int,
):
    shutil.rmtree(output_dir_path, ignore_errors=True)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    print(f"Converting PDF to JPG at {dpi} DPI, quality {quality}...")

    scale = dpi / 72.0

    pdf = pdfium.PdfDocument(pdf_path)

    image_paths: list[Path] = []
    n_pages = len(pdf)
    for i in range(n_pages):
        page = pdf[i]
        bitmap = page.render(scale=scale, rotation=0)
        image = bitmap.to_pil()

        image_path = output_dir_path / f"page-{i + 1:02d}.jpg"

        image.save(
            image_path,
            "JPEG",
            quality=quality,
            optimize=True,
        )

        image_paths.append(image_path)

    print("PDF to JPG conversion complete")

    print_dir_size(output_dir_path)

    return image_paths


def print_dir_size(directory: Path):
    dir_bytes = sum(f.stat().st_size for f in directory.glob("*") if f.is_file())
    dir_mb = dir_bytes / (1024 * 1024)
    print(f"{directory.name} total size: {dir_mb:.2f} MB")


image_paths = pdf_to_jpg(PDF_PATH, jpg_dir, DPI, JPG_QUALITY)

pdf_bytes = img2pdf.convert([str(path) for path in image_paths])
if pdf_bytes:
    with open(FILES_DIR / "output.pdf", "wb") as output_file:
        output_file.write(pdf_bytes)
