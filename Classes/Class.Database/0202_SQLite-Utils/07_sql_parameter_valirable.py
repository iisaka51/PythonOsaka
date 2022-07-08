list(db.query("select * from creatures where species = :species",
              {"species": "chicken"}))
