from sh import curl

# curl http://www.google.com -o google.html --slient

curl("http://www.google.com/", "-o", "google.html", "--silent")
curl("http://www.google.com/", o="google.html", silent=True)
