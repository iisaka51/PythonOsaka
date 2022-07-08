from pathlib import Path
from InquirerPy import inquirer
from InquirerPy.validator import PathValidator

src_path = inquirer.filepath(
    message="Enter file to upload:",
    default=str(Path('/tmp')),
    validate=PathValidator(is_file=True, message="Input is not a file"),
    only_files=True,
).execute()

dest_path = inquirer.filepath(
    message="Enter path to download:",
    validate=PathValidator(is_dir=True, message="Input is not a directory"),
    only_directories=True,
).execute()

print(f'src_path: {src_path}, dest_path: {dest_path}')
