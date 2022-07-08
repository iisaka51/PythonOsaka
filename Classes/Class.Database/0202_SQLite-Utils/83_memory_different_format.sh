cat creatures.csv
cat species.json
sqlite-utils memory creatures.csv species.json \
    "select * from creatures join species on creatures.id = species.id"


