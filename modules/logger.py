# Import Logly
from logly import Logly
import os
logly = Logly()
logly.start_logging()

logger = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../log.txt")
logly.set_default_file_path(logger)

# Start logging again
logly.start_logging()