import orjson, datetime

data = orjson.dumps(
    { "other": 1,
      datetime.date(2021, 1, 5): 2,
      datetime.date(2021, 1, 3): 3
    },
    option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS
)
print(data)
