import re
from pathlib import Path
import os
import sys


def extract_number_and_text(file_name: Path):
    match = re.match(r"(\d+)([A-Za-z]*)", file_name.stem)  # Tách số và chữ
    return (int(match.group(1)), match.group(2)) if match else (0, "")


def main():
    current_dir = (
        Path(sys.executable).resolve().parent
        if getattr(sys, "frozen", False)
        else Path(__file__).resolve().parent
    )

    # print(current_dir)
    if pdf_files := list(current_dir.glob("[0-9]*.pdf")):
        sorted_pdf_files = sorted(pdf_files, key=lambda x: extract_number_and_text(x))

        temp = []
        for p in sorted_pdf_files:
            new_name = p.with_name(f"{p.stem}_.pdf")
            temp.append(new_name)
            p.rename(new_name)

        for index, p in enumerate(temp, start=1):
            new_name = p.with_name(f"{index:02d}.pdf")
            p.rename(new_name)
    else:
        raise Exception("No PDF Scan File")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[Error] >>  {e}")
        os.system("pause")
