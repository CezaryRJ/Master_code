from datetime import datetime, timedelta
from pytz import timezone
import pytz


tz = timezone('Iceland')
utc_offset = timedelta(hours=-8, minutes=0)  # +5:30

print(pytz.timezone('PST'))