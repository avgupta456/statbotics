import os

from dotenv import load_dotenv

load_dotenv()

os.environ["LOCAL_DB"] = "True"

from src.process.process_main import process_main  # noqa: E402

start_year = 2002
end_year = 2021
clean = True

process_main(start_year, end_year, clean)
