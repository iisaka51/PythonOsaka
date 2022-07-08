import pydash as py_

forex = {
    "mxnjpy": {
        "long": {"open": {"lots": 10000, "swap": 8}},
        "short": {"open": {"lots": 2000, "swap": -24}},
    }
}

v1 = forex["mxnjpy"]["long"]["open"]["swap"]

v2 = py_.get(forex, "mxnjpy.long.open.swap")

# v1
# v2
