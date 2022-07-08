from pydal import DAL, Field
import datetime

db = DAL("sqlite://log.db")
log = db.define_table('log',
                     Field('event'),
                     Field('event_time', 'datetime'),
                     Field('severity', 'integer'),
                     migrate='log.table')

if __name__ == '__main__':
    now = datetime.datetime.now()
    id = db.log.insert(event='port scan', event_time=now, severity=1)
    id = db.log.insert(event='xss injection', event_time=now, severity=2)
    id = db.log.insert(event='unauthorized login', event_time=now, severity=3)

    db.commit()
    db.close()
