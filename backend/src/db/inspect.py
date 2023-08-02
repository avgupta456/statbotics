from sqlalchemy import inspect  # type: ignore

from src.db.main import engine  # type: ignore


def print_all_tables():
    schema = "public"
    inspector = inspect(engine)  # type: ignore
    for table_name in inspector.get_table_names(schema):  # type: ignore
        print(f"{table_name}")
        for column in inspector.get_columns(table_name, schema):  # type: ignore
            print("Column: %s" % column)  # type: ignore
        print()
