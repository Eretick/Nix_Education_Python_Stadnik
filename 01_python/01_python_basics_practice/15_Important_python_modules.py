# there is no task link
import os
import sys
import time
current_time = time.ctime()
print("Time just now:", current_time)
print("Year:", time.strptime(current_time).tm_year)
print("Your OS is", "windows" if os.name == "nt" else os.name)
print("So your platform should be", sys.platform)
print("Your user account should be", os.getlogin())
print("Your python installed at", sys.exec_prefix)


