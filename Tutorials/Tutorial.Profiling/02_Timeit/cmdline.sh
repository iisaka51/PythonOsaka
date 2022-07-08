#!/bin/bash

python3 -m timeit '"-".join(str(n) for n in range(100))'
python3 -m timeit '"-".join([str(n) for n in range(100)])'
python3 -m timeit '"-".join(map(str, range(100)))'
