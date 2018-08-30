from datetime import datetime
from datetime import timedelta


time1 = datetime.now()
for i in range(12302355):
    x = i
time2 = datetime.now()
new = (time2 - time1).seconds

print(type(new))