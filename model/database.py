def test(db_connection):
    results = db_connection.execute('Select * From Movies Limit 10')
    print([x for x in results])