import dataset

db = dataset.connect('sqlite:///stock_portfolio.db')

table = db['Stock_Portfolio']


def upsert_record(table, record, keys):
    """
    Upserts a record into the specified table.

    :param table: The table object where the record will be upserted.
    :param record: A dictionary representing the record to be upserted.
    :param keys: A list of keys to identify the record for upsert.
    """
    table.upsert(record, keys)


table.insert(dict(stock_name="APPL", price=1112, quant=3))

table.delete(name='John Doe')