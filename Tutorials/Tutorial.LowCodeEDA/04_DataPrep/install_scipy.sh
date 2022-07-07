# for macOS
export OPENBLAS=$(brew --prefix openblas)
export CFLAGS="-falign-functions=8 ${CFLAGS}"
python -m pip install Cython pybind11 pythran
python -m pip install --no-use-pep517 scipy
