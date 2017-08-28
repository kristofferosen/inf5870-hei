from time import sleep
from progress.bar import Bar

bar = Bar('Processing', max=20)
for i in range(20):
    # Do some work
    sleep(0.1)
    bar.next()
bar.finish()

import time
import sys

for i in range(10):
    time.sleep(0.1)
    sys.stdout.write("\r%d%%" % i)
    sys.stdout.flush()