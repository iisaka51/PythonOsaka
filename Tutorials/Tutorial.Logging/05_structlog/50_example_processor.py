import datetime, logging, sys
from structlog import wrap_logger
from structlog.processors import JSONRenderer
from structlog.stdlib import filter_by_level

logging.basicConfig(stream=sys.stdout, format="%(message)s")

def add_timestamp(_, __, event_dict):
    event_dict["timestamp"] = datetime.datetime.utcnow()
    return event_dict

def censor_password(_, __, event_dict):
    pw = event_dict.get("password")
    if pw:
        event_dict["password"] = "*CENSORED*"
    return event_dict

log = wrap_logger(
    logging.getLogger(__name__),
    processors=[
        filter_by_level,
        add_timestamp,
        censor_password,
        JSONRenderer(indent=1, sort_keys=True)
    ]
)

# log.info("something.filtered")
# log.warning("something.not_filtered", password="secret")
