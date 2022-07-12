import arrow

builtin_formats = {
    'FORMAT_ATOM': arrow.FORMAT_ATOM,
    'FORMAT_COOKIE':  arrow.FORMAT_COOKIE,
    'FORMAT_RFC1036': arrow.FORMAT_RFC1036,
    'FORMAT_RFC1123': arrow.FORMAT_RFC1123,
    'FORMAT_RFC2822':  arrow.FORMAT_RFC2822,
    'FORMAT_RFC3339':  arrow.FORMAT_RFC3339,
    'FORMAT_RFC822': arrow.FORMAT_RFC822,
    'FORMAT_RFC850':  arrow.FORMAT_RFC850,
    'FORMAT_RFC850':  arrow.FORMAT_RFC850,
    'FORMAT_RSS':  arrow.FORMAT_RSS,
    'FORMAT_W3C':  arrow.FORMAT_W3C,
}

dt = arrow.utcnow()
for name, format in builtin_formats.items():
    date = dt.format(format)
    print(f'{name:16}: {date}' )
