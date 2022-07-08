async with timeout(1.5) as cm:
    cm.shift(1)  # add another second on waiting
    cm.update(loop.time() + 5)  # reschedule to now+5 seconds
