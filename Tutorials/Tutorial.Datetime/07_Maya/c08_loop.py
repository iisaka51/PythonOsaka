import maya

event_start = maya.now()
event_end = event_start.add(minutes=2)

event = maya.MayaInterval(start=event_start, end=event_end)

