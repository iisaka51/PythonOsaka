import pydash as py_

beers = [
    { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
    { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
]

def get_abv(beer):
   v =  py_.get(beer, "abv")
   return beer["abv"]


v1 = ( py_.chain(beers)
       .map(get_abv)
       .sum()
     )

# v1
# v1.value()
