import peewee
import settings

database = peewee.SqliteDatabase(settings.DB_PATH, threadlocals=True)