import time
import yaml
import argparse
from monitorit.taskgenerator import TaskGenerator

parser = argparse.ArgumentParser()
parser.add_argument('--conf', help='conf file')
parser.add_argument('--dbconf', help='db conf file')
args = parser.parse_args()

yaml_conf = yaml.load(open(args.conf))
yaml_dbconf = yaml.load(open(args.dbconf))

while(1):
	task_gen = TaskGenerator(yaml_conf,yaml_dbconf)
	task_gen.generate_tasks();
	time.sleep(30)
