table = db["creatures"]

table.insert_all([{
     "name": "Cleo",
     "species": "dog",
     "age": 6
 }, {
     "name": "Lila",
     "species": "chicken",
     "age": 0.8,
 }, {
     "name": "Bants",
     "species": "chicken",
     "age": 0.8,
 }])
