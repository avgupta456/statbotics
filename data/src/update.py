import os
import random

from dotenv import load_dotenv

load_dotenv()

os.environ["LOCAL_DB"] = "True"

# Set random seed, for random team matches
random.seed(5511)

from process.process_main import process_main  # noqa: E402

start_year = 2022
end_year = 2022
clean = False

process_main(start_year, end_year, clean, True)
