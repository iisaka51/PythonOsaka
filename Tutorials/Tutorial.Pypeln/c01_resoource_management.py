import pypeln as pl

def on_start():
    return dict(
        http_session = get_http_session(),
        db_session = get_db_session(),
    )

def func(x, http_session, db_session):
    # 何かしらの処理
    return v

def on_end(http_session, db_session):
    http_session.close()
    db_session.close()


stage = pl.process.map(func, stage, workers=3, on_start=on_start, on_end=on_end)
