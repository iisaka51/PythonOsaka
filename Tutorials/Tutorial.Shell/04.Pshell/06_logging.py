import logging
import pshell as sh

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s'
    )

with sh.open("hello.txt", "w") as fh:
    fh.write("Hello world!")
