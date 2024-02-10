from sqlalchemy import inspect

from src.db.main import engine


def print_all_tables():
    schema = "public"
    inspector = inspect(engine)
    for table_name in inspector.get_table_names(schema):
        print(f"{table_name}")
        for column in inspector.get_columns(table_name, schema):
            print("Column: %s" % column)
        print()
