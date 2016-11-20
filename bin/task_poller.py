#!/project/backend/bin/python
import time
import yaml
import argparse
import os
from monitorit.metric import Metric
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from subprocess import Popen,PIPE,STDOUT

import logging
logging.basicConfig()

parser = argparse.ArgumentParser()
parser.add_argument('--task', help='task file')
args = parser.parse_args()

yaml_conf = yaml.load(open(args.task))

def exec_command(**task):
	if 'http' in task['monitor_type']:
		out = Popen(task['command'].split(' '),stderr=STDOUT,stdout=PIPE)
		t = out.communicate()[0],out.returncode
		print (t[0])

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    for task in yaml_conf:
	    scheduler.add_job(exec_command,kwargs=task)
	    scheduler.add_job(exec_command,'interval',seconds=3,kwargs=task)
    
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
