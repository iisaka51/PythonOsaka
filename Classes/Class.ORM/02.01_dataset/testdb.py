import dataset

db = dataset.connect('sqlite:///users.sqlite')
table = db['users']

if __name__ == '__main__':
    try:
        from test_data import test_data
    except ModuleNotFoundError as msg:
        import sys
        print(msg)
        sys.exit(0)

    for t in test_data:
        table.insert(t)

    db.commit()
    db.close()
