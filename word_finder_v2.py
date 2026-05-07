"""
Tra từ điển từ file PDF bằng pypdf
- Quét folder chứa PDF
- Đọc toàn bộ PDF
- Trích xuất từ + nghĩa
- Lưu vào dictionary
- Cho phép tra từ liên tục
"""

from pathlib import Path
import re
import logging
from pypdf import PdfReader


# ================= LOGGING =================
logging.basicConfig(level=logging.INFO, format="%(message)s")


# =========================
# NHẬP THƯ MỤC
# =========================
def get_folder_path() -> Path:
    """Yêu cầu người dùng nhập thư mục chứa file PDF."""
    while True:
        folder = Path(input("Nhập đường dẫn thư mục chứa PDF: ").strip())

        if not folder.exists():
            print("❌ Đường dẫn không tồn tại.")
        elif not folder.is_dir():
            print("❌ Đây không phải thư mục.")
        else:
            return folder


# =========================
# QUÉT FILE PDF
# =========================
def get_pdf_files(folder_path: Path) -> list[Path]:
    """Lấy danh sách file PDF trong thư mục."""
    pdf_files = [
        file_path
        for file_path in folder_path.iterdir()
        if file_path.is_file() and file_path.suffix.lower() == ".pdf"
    ]

    return pdf_files


# =========================
# ĐỌC PDF
# =========================
def extract_text_from_pdf(pdf_path: Path) -> str:
    """Đọc toàn bộ nội dung từ một file PDF."""
    try:
        reader = PdfReader(pdf_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    except Exception as error:
        logging.error(f"❌ Lỗi khi đọc {pdf_path.name}: {error}")
        return ""


# =========================
# LÀM SẠCH TEXT
# =========================
def clean_text(text: str) -> str:
    """Chuẩn hóa văn bản."""
    text = text.replace("￾", "")
    text = text.replace("\xa0", " ")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


# =========================
# TẠO DICTIONARY
# =========================
def build_dictionary(text: str) -> dict[str, str]:
    """
    Tạo dictionary dạng:
    {
        "depression": "Trầm cảm (A mental state...)"
    }
    """

    pattern = re.compile(
        r"""
        (?P<word>[a-zA-Z\- ]+)
        \s*\([^)]+\)\s*
        (?:\[[A-Z0-9]+\])?\s*
        .*?
        /[^/]+/\s*
        (?P<meaning>[^\n(]+?)\s*
        \((?P<definition>.*?)\)
        """,
        re.VERBOSE | re.DOTALL
    )

    vocab_dict = {}

    for match in pattern.finditer(text):
        word = match.group("word").strip().lower()

        meaning = match.group("meaning").strip()

        definition = " ".join(
            match.group("definition").split()
        )

        vocab_dict[word] = (
            f"{meaning} ({definition})"
        )

    return vocab_dict


# =========================
# LOAD TOÀN BỘ PDF
# =========================
def load_dictionary_from_pdfs(pdf_files: list[Path]) -> dict[str, str]:
    """Đọc toàn bộ PDF và tạo từ điển."""

    full_text = []

    for pdf_file in pdf_files:
        logging.info(f"📖 Đang đọc: {pdf_file.name}")

        text = extract_text_from_pdf(pdf_file)

        if text:
            cleaned_text = clean_text(text)
            full_text.append(cleaned_text)

    merged_text = "\n".join(full_text)

    return build_dictionary(merged_text)


# =========================
# TRA TỪ
# =========================
def lookup_loop(vocab_dict: dict[str, str]) -> None:
    """Cho phép tra từ liên tục."""

    print("\n===== TỪ ĐIỂN ĐÃ SẴN SÀNG =====")
    print("Gõ từ cần tra.")
    print("Gõ 'exit' để thoát.\n")

    while True:
        word = input("Nhập từ: ").strip().lower()

        if word == "exit":
            print("👋 Đã thoát chương trình.")
            break

        meaning = vocab_dict.get(word)

        if meaning:
            print(f"\n→ {word}:")
            print(meaning)
            print()

        else:
            print("❌ Không tìm thấy từ.\n")


# =========================
# MAIN
# =========================
def main() -> None:
    """Hàm chính."""

    folder_path = get_folder_path()

    logging.info("\n🔍 Đang tìm file PDF...\n")

    pdf_files = get_pdf_files(folder_path)

    if not pdf_files:
        print("❌ Không tìm thấy file PDF.")
        return

    print(f"✅ Tìm thấy {len(pdf_files)} file PDF.\n")

    vocab_dict = load_dictionary_from_pdfs(pdf_files)

    print(f"\n✅ Đã tải {len(vocab_dict)} từ vựng.\n")

    lookup_loop(vocab_dict)


if __name__ == "__main__":
    main()