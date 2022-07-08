import pydash as py_

beers = [ "Pale Ale", "ICHI SENSHIN", "ICHIGO ICHIE", "Pilserl" ]

v1 = ( py_.chain(beers)
       .without("Pale Ale")
       .reject(lambda x: x.startswith("P"))
     )

v2 = ( py_.chain(beers)
       .without("Pale Ale")
       .reject(lambda x: x.startswith("P"))
       .value()
     )

v3 = v1.value()

# v1
# v2
# v3

