import re
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


def extract_number_and_text(file_name: Path):
    match = re.match(r"(\d+)([A-Za-z]*)", file_name.stem)
    return (int(match.group(1)), match.group(2)) if match else (0, "")


def rename_pdf_files_in_directory(folder: str):
    folder_path = Path(folder)
    if not folder_path.is_dir():
        raise ValueError("Đường dẫn không hợp lệ")

    pdf_files = list(folder_path.glob("[0-9]*.pdf"))
    if not pdf_files:
        raise FileNotFoundError("Không tìm thấy file PDF phù hợp trong thư mục")

    sorted_pdf_files = sorted(pdf_files, key=lambda x: extract_number_and_text(x))

    temp_files = []
    for p in sorted_pdf_files:
        new_name = p.with_name(f"{p.stem}_.pdf")
        temp_files.append(new_name)
        p.rename(new_name)

    for index, p in enumerate(temp_files, start=1):
        new_name = p.with_name(f"{index:02d}.pdf")
        p.rename(new_name)


def browse_directory(entry_widget):
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder_selected)


def on_rename_clicked(entry_widget):
    folder = entry_widget.get()
    try:
        rename_pdf_files_in_directory(folder)
        messagebox.showinfo("Thành công", "Đổi tên file PDF Scan hoàn tất!")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def setup_ui():
    root = tk.Tk()
    root.title("Rename PDF Scan")
    root.iconbitmap(
        r"C:\Users\M10\Documents\MythProjects\Tweaks\__assests\folderredscript_92992.ico"
    )
    root.geometry("390x190")
    root.resizable(False, False)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", font=("Segoe UI", 12))
    style.configure("TButton", font=("Segoe UI", 11), padding=6)
    style.configure("TEntry", font=("Segoe UI", 11))

    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid(row=0, column=0, sticky="nsew")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    label = ttk.Label(main_frame, text="Select folder:")
    label.grid(row=0, column=0, sticky="w", pady=(0, 10))

    entry_dir = ttk.Entry(main_frame, width=50)
    entry_dir.grid(row=1, column=0, pady=5, sticky="ew")

    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=2, column=0, pady=15, sticky="ew")

    browse_btn = ttk.Button(
        button_frame,
        text="🔍 Browser",
        command=lambda: browse_directory(entry_dir),
    )
    browse_btn.grid(row=0, column=0, padx=10)

    rename_btn = ttk.Button(
        button_frame,
        text="📝 Rename",
        command=lambda: on_rename_clicked(entry_dir),
    )
    rename_btn.grid(row=0, column=1, padx=10)

    return root


def main():
    root = setup_ui()
    root.mainloop()


if __name__ == "__main__":
    main()
