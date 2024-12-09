class InMemoryDB:
    def __init__(self):
        self.db = {}
        self.transaction = None

    # return the value associated with the key or null if the key doesn’t exist
    # can be called anytime even when a transaction is not in progress
    # within a transaction you can make as many changes to as many keys as you like. however, they should not be “visible” 
    # to get(), until the transaction is committed.
    def get(self, key: str) -> int:
        if self.transaction and key in self.transaction:
            return self.transaction[key]
        return self.db.get(key)

    # create a new key with the provided value if a key doesn’t exist, otherwise it will update the value of an existing key
    # if put(key, val) is called when a transaction is not in progress throw an exception
    def put(self, key: str, val: int):
        if self.transaction is None:
            raise Exception("No active transaction. Call begin_transaction() first.")
        self.transaction[key] = val

    # starts a new transaction
    # at a time only a single transaction may exist
    def begin_transaction(self):
        if self.transaction is not None:
            raise Exception("A transaction is already in progress.")
        self.transaction = {}

    # a transaction ends when either commit() or rollback() is called
    # commit() applies changes made within the transaction to the main state. allowing any future gets() to “see” the 
    # changes made within the transaction.
    def commit(self):
        if self.transaction is None:
            raise Exception("No active transaction to commit.")
        for key, value in self.transaction.items():
            self.db[key] = value
        self.transaction = None

    # rollback() should abort all the changes made within the transaction and everything should go back to the way it was before.
    def rollback(self):
        if self.transaction is None:
            raise Exception("No active transaction to rollback.")
        self.transaction = None



# create an instance of the in-memory database
inmemoryDB = InMemoryDB()

# should return None, because "A" doesn’t exist in the DB yet
print(inmemoryDB.get("A"))

# should throw an error because a transaction is not in progress
try:
    inmemoryDB.put("A", 5)
except Exception as e:
    print(e)

# starts a new transaction
inmemoryDB.begin_transaction()

# sets value of "A" to 5, but it's not committed yet
inmemoryDB.put("A", 5)

# should return None, because updates to "A" are not committed yet
print(inmemoryDB.get("A"))

# update "A"’s value to 6 within the transaction
inmemoryDB.put("A", 6)

# commits the open transaction
inmemoryDB.commit()

# should return 6, the last value of "A" to be committed
print(inmemoryDB.get("A"))

# throws an error, because there is no open transaction
try:
    inmemoryDB.commit()
except Exception as e:
    print(e)

# throws an error because there is no ongoing transaction
try:
    inmemoryDB.rollback()
except Exception as e:
    print(e)

# should return None because "B" does not exist in the database
print(inmemoryDB.get("B"))

# starts a new transaction
inmemoryDB.begin_transaction()

# sets key "B"’s value to 10 within the transaction
inmemoryDB.put("B", 10)

# rollback the transaction - revert any changes made to "B"
inmemoryDB.rollback()

# should return None because changes to "B" were rolled back
print(inmemoryDB.get("B"))