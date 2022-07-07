pdt_diff = pdt_tokyo.tz_localize(None) - pdt_london.tz_localize(None)
diff_time = pdt_diff.total_seconds() / 3600

# pdt_diff
# diff_time
