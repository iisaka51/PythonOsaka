from enum import Enum
import typer

class HashType(str, Enum):
    md5 = "md5"
    sha1 = "sha1"
    sha256 = "sha256"

def main(hash_type: HashType = HashType.md5):
    typer.echo(f"Hash Type: {hash_type.value}")


if __name__ == "__main__":
    typer.run(main)
