from dotenv import load_dotenv

load_dotenv()

from new_process.process_tba import main as process_tba

process_tba(2002, 2020, cache=True)

print("Done!")
