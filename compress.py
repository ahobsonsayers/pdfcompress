from pathlib import Path
import shutil
import img2pdf
from pdf2image import convert_from_path

FILES_DIR = Path("./files")
PDF_PATH = FILES_DIR / "input.pdf"

DPI = 300
JPG_QUALITY = 75

pdf_path = Path(PDF_PATH)
if not pdf_path.exists():
    raise FileNotFoundError(f"PDF not found: {pdf_path}")

jpg_dir = FILES_DIR / "jpg"
png_dir = FILES_DIR / "png"


def pdf_to_jpg_cairo(
    pdf_path: Path,
    output_dir_path: Path,
    dpi: int,
    quality: int,
):
    shutil.rmtree(output_dir_path, ignore_errors=True)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    print(f"Converting PDF to JPG at {DPI} DPI, quality {JPG_QUALITY}...")
    images = convert_from_path(
        str(pdf_path),
        dpi=dpi,
        fmt="jpeg",
        jpegopt={
            "quality": quality,
            "optimize": True,
        },
        thread_count=4,
        output_folder=output_dir_path,
        output_file="page-",
        paths_only=True,
        use_pdftocairo=True,
    )
    print("PDF to JPG conversion complete\n")

    image_paths = []
    for image in images:
        image_path = Path(str(image))

        parts = image_path.name.split("-")
        if len(parts) > 2:
            new_name = "-".join([parts[0], parts[2]])
            image_path = image_path.rename(image_path.with_name(new_name))

        image_paths.append(image_path)

    print_dir_size(output_dir_path)

    return image_paths


def print_dir_size(directory: Path):
    dir_bytes = sum(f.stat().st_size for f in directory.glob("*") if f.is_file())
    dir_mb = dir_bytes / (1024 * 1024)
    print(f"{directory.name} total size: {dir_mb:.2f} MB")


image_paths = pdf_to_jpg_cairo(PDF_PATH, jpg_dir, DPI, JPG_QUALITY)

pdf_bytes = img2pdf.convert([str(path) for path in image_paths])
if pdf_bytes:
    with open(FILES_DIR / "output.pdf", "wb") as output_file:
        output_file.write(pdf_bytes)
