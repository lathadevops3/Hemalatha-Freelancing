from pathlib import Path

CATEGORY_EXTENSIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".heic"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".md", ".odt", ".tex"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv", ".webm"],
    "Code": [".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".html", ".css", ".json", ".xml", ".yml", ".yaml", ".sh", ".bat", ".ps1"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "Executables": [".exe", ".msi", ".app", ".deb", ".rpm"],
}

DEFAULT_FOLDERS = set(CATEGORY_EXTENSIONS.keys())


def find_category(file_path: Path) -> str:
    extension = file_path.suffix.lower()
    for category, extensions in CATEGORY_EXTENSIONS.items():
        if extension in extensions:
            return category
    return "Others"


def make_unique_path(target: Path) -> Path:
    if not target.exists():
        return target

    stem = target.stem
    suffix = target.suffix
    parent = target.parent
    counter = 1

    while True:
        new_name = f"{stem} ({counter}){suffix}"
        candidate = parent / new_name
        if not candidate.exists():
            return candidate
        counter += 1


def organize_folder(folder: Path) -> None:
    if not folder.exists() or not folder.is_dir():
        raise ValueError(f"Path does not exist or is not a directory: {folder}")

    print(f"Organizing files inside: {folder}")

    for item in folder.iterdir():
        if item.is_dir():
            if item.name in DEFAULT_FOLDERS or item.name == "Others":
                continue
            continue

        if item.name.startswith("."):
            continue

        category = find_category(item)
        destination_folder = folder / category
        destination_folder.mkdir(exist_ok=True)

        destination = destination_folder / item.name
        destination = make_unique_path(destination)
        item.replace(destination)
        print(f"Moved: {item.name} -> {destination_folder.name}")

    print("Organization complete.")


def main() -> None:
    default_downloads = Path.home() / "Downloads"
    print("Downloads Organizer")
    print("Leave blank to organize the default Downloads folder.")
    user_input = input(f"Enter folder path [{default_downloads}]: ").strip()

    target_folder = Path(user_input) if user_input else default_downloads
    organize_folder(target_folder)


if __name__ == "__main__":
    main()
