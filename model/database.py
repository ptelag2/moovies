'''This program is responsible load query result into a dict.'''

def test(db_connection):
    results = db_connection.execute('Select * From Movies Limit 10')
    print([x for x in results])

'''
You should implement your backend code here and in model.py.
Look at the example use of model.database in app.py to debug.
I will soon write some documentation in app.py to specify some expected behavior of each call.
'''