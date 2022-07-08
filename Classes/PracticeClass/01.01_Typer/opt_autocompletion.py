import typer

valid_hashtypes = ["md5", "sha1", "sha256"]


def complete_hash(incomplete: str):
    completion = []
    for name in valid_hashtypes:
        if name.startswith(incomplete):
            completion.append(name)
    return completion


def main(
    hash_type: str = typer.Option( "md5", '-H', '--hash-type',
                           autocompletion=complete_hash,
                           help="Hash type")
    ):
    typer.echo(f"Hash type: {hash_type}")


if __name__ == "__main__":
    typer.run(main)
