import typer
from pathlib import Path

app = typer.Typer()

def human_readable_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024

def collect_files(root: Path):
    files = []
    for path in root.rglob("*"):
        if path.is_file():
            try:
                size = path.stat().st_size
                files.append((path, size))
            except OSError:
                # 某些文件可能没有权限访问，跳过
                pass
    return files


@app.command()
def stats(path: str = typer.Argument("."), top: int = 3):
    if top <= 0:
        raise typer.BadParameter("Invalid parameter!")
    p = Path(path)
    files = collect_files(p);
    files.sort(key = lambda x: x[1], reverse = True)
    total_size = sum(size for _, size in files)
    print(f"directory: {p.resolve()}")
    print(f"files: {len(files)}")
    print(f"size: {human_readable_size(total_size)}")
    if len(files) >= 1 :
        show_len = min(len(files), top)
        print()
        print(f"largest {show_len} files: ")
        for i, (path, size) in enumerate(files[:show_len], 1):
            print(f"{i:>2}. {human_readable_size(size):>10}  {path}")

if __name__ == "__main__":
    app()
