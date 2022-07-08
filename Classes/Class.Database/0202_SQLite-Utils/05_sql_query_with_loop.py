for row in db.query("select name, species from creatures"):
    print(f'{row["name"]} is a {row["species"]}')
