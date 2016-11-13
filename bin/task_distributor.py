#!/project/backend/bin/python
import time
import yaml
import argparse
from monitorit.taskgenerator import TaskGenerator

parser = argparse.ArgumentParser()
parser.add_argument('--conf', help='conf file')
args = parser.parse_args()

yaml_conf = yaml.load(open(args.conf))

while(1):
	task_gen = TaskGenerator(yaml_conf)
	task_gen.generate_tasks();
	time.sleep(30)
