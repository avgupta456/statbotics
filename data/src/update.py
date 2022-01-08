import os

from dotenv import load_dotenv

load_dotenv()

os.environ["LOCAL_DB"] = "True"

from process.process_main import process_main  # noqa: E402


start_year = 2022
end_year = 2022
clean = False

process_main(start_year, end_year, clean, True)
