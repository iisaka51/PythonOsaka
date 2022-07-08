import dataset

db = dataset.connect('sqlite:///users.sqlite')
table = db['users']

if __name__ == '__main__':
    test_data = [
        { 'name': 'Jack Bauer', 'age': 55, 'belongs': 'CTU' },
        { 'name': "Chloe O'Brian", 'age': 0, 'belongs': 'CTU' },
        { 'name': 'Anthony Tony', 'age': 29, 'belongs': 'CTU' },
        { 'name': 'David Gilmour', 'age': 75, 'belongs': 'Pink Floyd' },
        { 'name': 'Ann Wilson', 'age': 71, 'belongs': 'Heart' },
        { 'name': 'Nacy Wilson', 'age': 67, 'belongs': 'Heart' },
    ]
    for t in test_data:
        table.insert(t)
    db.commit()
    db.close()
