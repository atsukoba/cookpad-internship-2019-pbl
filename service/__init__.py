import sys
import logging
from datetime import datetime as dt

now = dt.now().strftime('%m%d-%H%M%S')

logging.basicConfig(
    # filename=f"data/log/{now}.log",
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG, stream=sys.stdout)
