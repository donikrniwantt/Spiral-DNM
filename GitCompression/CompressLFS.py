import os
import sys
import zipfile


def compress_file(file_path, output_zip):
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, os.path.basename(file_path))


def split_file(file_path, max_size):
    part_paths = []
    try:
        with open(file_path, "rb") as source:
            part_num = 1
            while True:
                chunk = source.read(max_size)
                if not chunk:
                    break
                part_file = f"{file_path}.part{part_num}"
                with open(part_file, "xb") as part:
                    part.write(chunk)
                part_paths.append(part_file)
                part_num += 1
        return part_paths
    except Exception:
        for part_path in part_paths:
            if os.path.exists(part_path):
                os.remove(part_path)
        raise


def process_files(directory, max_size=50 * 1024 * 1024, split_size=50 * 1024 * 1024):
    log_file = os.path.join(directory, "compression_log.txt")
    try:
        with open(log_file, "w", encoding="utf-8", newline="\n") as log:
            for root, dirs, files in os.walk(directory):
                dirs[:] = [name for name in dirs if name != ".git"]

                for filename in files:
                    file_path = os.path.join(root, filename)
                    if filename == "compression_log.txt" or filename.endswith(".zip"):
                        continue
                    if ".part" in filename:
                        continue

                    file_size = os.path.getsize(file_path)
                    if file_size <= max_size:
                        continue

                    zip_file = f"{file_path}.zip"
                    if os.path.exists(zip_file):
                        raise FileExistsError(f"Archive already exists: {zip_file}")

                    print(f"Compressing {file_path}...")
                    try:
                        compress_file(file_path, zip_file)
                        zip_size = os.path.getsize(zip_file)
                        relative_file_path = os.path.relpath(file_path, directory)
                        relative_zip_file = os.path.relpath(zip_file, directory)

                        if zip_size > max_size:
                            print(f"Archive remains too large; splitting {zip_file}...")
                            part_paths = split_file(zip_file, split_size)
                            if not part_paths:
                                raise RuntimeError(f"No split parts were created for {zip_file}")
                            log.write(f"{relative_file_path}|{relative_zip_file}.part*\n")
                            log.flush()
                            os.fsync(log.fileno())
                            os.remove(zip_file)
                            for part_path in part_paths:
                                print(f"Created {part_path}")
                        else:
                            log.write(f"{relative_file_path}|{relative_zip_file}\n")
                            log.flush()
                            os.fsync(log.fileno())

                        os.remove(file_path)
                    except Exception:
                        if os.path.exists(zip_file):
                            os.remove(zip_file)
                        raise

        return True
    except Exception as error:
        print(f"Compression failed: {error}", file=sys.stderr)
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python CompressLFS.py <directory>", file=sys.stderr)
        sys.exit(2)

    directory_to_process = sys.argv[1]
    if not os.path.isdir(directory_to_process):
        print(f"Error: {directory_to_process} is not a valid directory.", file=sys.stderr)
        sys.exit(2)

    sys.exit(0 if process_files(directory_to_process) else 1)
