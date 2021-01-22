import numpy
import orjson, datetime, numpy

data = {
    "type": "job",
    "created_at": datetime.datetime(1970, 1, 1),
    "status": "🆗",
    "payload": numpy.array([[1, 2], [3, 4]]),
}
sieiralized_data = orjson.dumps(data,
                    option=orjson.OPT_NAIVE_UTC | orjson.OPT_SERIALIZE_NUMPY)
new_data = orjson.loads(sieiralized_data)
print(new_data)

