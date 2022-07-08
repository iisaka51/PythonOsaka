from flask import Flask, render_template, request
from some_module2 import some_function
import sys
import uuid
import logging
import structlog

logger = structlog.get_logger()
app = Flask(__name__, template_folder='templates')
@app.route('/greeting/<name>')
def index(name):
    structlog.threadlocal.clear_threadlocal()
    structlog.threadlocal.bind_threadlocal(
        view=request.path,
        request_id=str(uuid.uuid4()),
        peer=request.access_route[0],
    )
    log = logger.bind()
    name = some_function(name)
    log.info('name: ', name=name)

    return render_template('index.html', name=name)

if __name__ == '__main__':
    logging.basicConfig(
        format="%(message)s", stream=sys.stdout, level=logging.INFO
    )
    structlog.configure(
        processors=[
            structlog.threadlocal.merge_threadlocal,
            structlog.processors.KeyValueRenderer(
                key_order=["event", "view", "peer"]
            ),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    app.run(debug=True)
