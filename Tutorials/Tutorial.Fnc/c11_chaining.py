import fnc
from functools import partial

beers = [ "Pale Ale", "ICHI SENSHIN", "ICHIGO ICHIE", "Pilserl" ]

do_without_paleale = partial(fnc.sequences.without,
                            ["Pale Ale"])
do_reject_start_p = partial(fnc.sequences.reject,
                            lambda x: x.startswith("P"))

do_choice_beers = fnc.compose(
     do_without_paleale,
     do_reject_start_p,
     )
v1 = do_choice_beers(beers)

# list(v1)
