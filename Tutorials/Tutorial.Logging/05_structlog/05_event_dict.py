import datetime
def timestamper(_, __, event_dict):
    event_dict["time"] = datetime.datetime.now().isoformat()
    return event_dict
