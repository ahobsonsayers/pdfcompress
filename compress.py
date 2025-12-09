from pathlib import Path

from pdf2image import convert_from_path

FILES_DIR = Path("./files")
PDF_PATH = FILES_DIR / "input.pdf"

DPI = 200
JPG_QUALITY = 85

pdf_path = Path(PDF_PATH)
if not pdf_path.exists():
    raise FileNotFoundError(f"PDF not found: {pdf_path}")

jpg_dir = FILES_DIR / "jpg"
png_dir = FILES_DIR / "png"

def convert_to_jpg(pdf_path: Path, output_dir_path: Path, dpi: int, quality: int,):
    output_dir_path.mkdir(parents=True, exist_ok=True)

    print(f"Converting PDF to JPG at {DPI} DPI, quality {JPG_QUALITY}...")
    convert_from_path(
        str(pdf_path),
        dpi=dpi,
        fmt="jpeg",
        jpegopt={"quality": quality, "optimize": True,},
        thread_count=4,
        output_folder=output_dir_path,
        output_file="page",
        paths_only=True,
    )
    print("PDF to JPG conversion complete")

    print_dir_size(output_dir_path)
    print()

def convert_to_png(pdf_path: Path, output_dir_path: Path, dpi: int,):
    output_dir_path.mkdir(parents=True, exist_ok=True)

    print(f"Converting PDF to PNG at {DPI} DPI...")
    convert_from_path(
        pdf_path,
        dpi=dpi,
        fmt="png",
        thread_count=4,
        output_folder=output_dir_path,
        output_file="page",
        paths_only=True,
    )
    print("PDF to PNG conversion complete")

    print_dir_size(png_dir)
    print()

def print_dir_size(directory: Path):
    dir_bytes = sum(f.stat().st_size for f in directory.glob("*") if f.is_file())
    dir_mb = dir_bytes / (1024 * 1024)
    print(f"{directory.name} total size: {dir_mb:.2f} MB")

convert_to_jpg(PDF_PATH, jpg_dir, DPI, JPG_QUALITY)
# convert_to_png(PDF_PATH, png_dir, DPI)
