"""
Trích xuất từ vựng + nghĩa từ file PDF bằng pypdf
(thay thế PyPDF2 đã deprecated)

Mục tiêu:
- Đọc toàn bộ file PDF
- Tìm các mục từ dạng:
  depression (n)
  /dɪˈpreʃn/
  Trầm cảm
  (A mental state characterized by ...)

- Xuất ra:
  depression: Trầm cảm (A mental state characterized by ...)
"""

from pathlib import Path
import re
from pypdf import PdfReader


# =========================
# CẤU HÌNH
# =========================
PDF_FILE = "20260502101200.pdf"


# =========================
# ĐỌC FILE PDF
# =========================
def extract_text_from_pdf(pdf_path: str) -> str:
    """Đọc toàn bộ text từ PDF."""
    reader = PdfReader(pdf_path)

    pages_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages_text.append(text)

    return "\n".join(pages_text)


# =========================
# LÀM SẠCH TEXT
# =========================
def clean_text(text: str) -> str:
    """Chuẩn hóa text."""
    text = text.replace("￾", "")      # ký tự lỗi ngắt dòng PDF
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


# =========================
# TRÍCH XUẤT TỪ + NGHĨA
# =========================
def extract_vocabulary(text: str):
    """
    Tìm pattern:
    depression (n)
    /dɪˈpreʃn/
    Trầm cảm
    (A mental state ...)
    """

    pattern = re.compile(
        r"""
        (?P<word>[a-zA-Z\- ]+)          # từ vựng
        \s*\([^)]+\)\s*                # loại từ (n), (v), ...
        (?:\[[A-Z0-9]+\])?\s*          # level [B1]
        .*?                            # biến thể từ
        /[^/]+/\s*                     # IPA
        (?P<meaning>[^\n(]+?)\s*       # nghĩa tiếng Việt
        \((?P<definition>.*?)\)        # định nghĩa tiếng Anh
        """,
        re.VERBOSE | re.DOTALL
    )

    results = []

    for match in pattern.finditer(text):
        word = match.group("word").strip()
        meaning = match.group("meaning").strip()
        definition = " ".join(match.group("definition").split())

        results.append(
            f"{word}: {meaning} ({definition})"
        )

    return results


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

    vocab_list = extract_vocabulary(text)

    if not vocab_list:
        print("Không tìm thấy dữ liệu.")
        return

    print("\n===== KẾT QUẢ =====\n")
    for item in vocab_list:
        print(item)


if __name__ == "__main__":
    main()