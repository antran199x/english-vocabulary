"""
Tra từ điển từ file PDF bằng pypdf
- Đọc file PDF
- Trích xuất từ + nghĩa
- Lưu vào dictionary
- Dùng while True để tra từ
"""

from pathlib import Path
import re
from pypdf import PdfReader


# =========================
# CẤU HÌNH
# =========================
PDF_FILE = "20260502101200.pdf"


# =========================
# ĐỌC PDF
# =========================
def extract_text_from_pdf(pdf_path: str) -> str:
    """Đọc toàn bộ nội dung PDF."""
    reader = PdfReader(pdf_path)

    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    return "\n".join(pages)


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
def build_dictionary(text: str) -> dict:
    """
    Tạo dictionary:
    {
        "depression": "Trầm cảm (A mental state...)",
        ...
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
        definition = " ".join(match.group("definition").split())

        vocab_dict[word] = f"{meaning} ({definition})"

    return vocab_dict


# =========================
# TRA TỪ
# =========================
def lookup_loop(vocab_dict: dict):
    """Cho phép tra từ liên tục."""
    print("\n===== TỪ ĐIỂN SẴN SÀNG =====")
    print("Gõ từ cần tra.")
    print("Gõ exit để thoát.\n")

    while True:
        word = input("Nhập từ: ").strip().lower()

        if word == "exit":
            print("Đã thoát chương trình.")
            break

        if word in vocab_dict:
            print(f"→ {word}: {vocab_dict[word]}\n")
        else:
            print("Không tìm thấy từ.\n")


# =========================
# MAIN
# =========================
def main():
    pdf_path = Path(PDF_FILE)

    if not pdf_path.exists():
        print("Không tìm thấy file PDF.")
        return

    text = extract_text_from_pdf(pdf_path)
    text = clean_text(text)

    vocab_dict = build_dictionary(text)

    print(f"Đã tải {len(vocab_dict)} từ.")

    lookup_loop(vocab_dict)


if __name__ == "__main__":
    main()