list(db.query("""
    select
      creatures.id,
      creatures.name,
      creatures.age,
      species.id as species_id,
      species.species
    from creatures
      join species on creatures.species_id = species.id
"""))
