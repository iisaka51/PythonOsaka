from croniter import croniter

v1 = croniter.is_valid('*/2 * * * *')
v2 = croniter.is_valid('wrang_format * * *')
