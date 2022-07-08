import re

sample_log = """
227.4.48.140 - - [19/Nov/2020:02:18:11 +0000] "PUT /customers HTTP/1.1" 401 2347
"""

re_apache_log = r'(?P<ip>.*?) - - \[(?P<date>.*?)(?= ) (?P<timezone>.*?)\] \"(?P<request_method>.*?) (?P<path>.*?)(?P<request_version> HTTP/.*)?\" (?P<status>.*?) (?P<length>.*?)'

def read_log(filepath):
    apachelog = dict()
    with open(filepath) as f:
        for line in f.readlines():
            match = re.search(re_apache_log, line)
            if match:
                log = dict()
                log['IP'] = match.group('ip')
                log['METHOD'] = match.group('request_method')
                log['STATUS'] = match.group('status')
                apachelog[match.group('date')] = log
    return apachelog

if __name__ == '__main__':
    log = read_log('access_log')
    for date in log.keys():
        print(f"{log[date]['IP']}, {log[date]['METHOD']}, {log[date]['STATUS']}")
