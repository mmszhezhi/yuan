import time
from progressbar import *
total = 1000
def dosomework():

    time.sleep(2)
progress = ProgressBar()
for i in progress(range(10)):
    dosomework()