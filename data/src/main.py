import os

from dotenv import load_dotenv

load_dotenv()

os.environ["LOCAL_DB"] = "True"

from process.process_main import process_main


start_year = 2002
end_year = 2020

process_main(start_year, end_year)
