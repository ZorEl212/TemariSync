from os import getenv
storage_t = getenv('STORAGE_TYPE')
if storage_t != 'db':
    from models.engine.file import FileStorage
    storage = FileStorage()
else:
    from models.engine.db import DBStorage
    storage = DBStorage()

storage.reload()