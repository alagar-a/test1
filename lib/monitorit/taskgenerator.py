import monitorit.db as monitordb
import yaml

class TaskGenerator:
	def __init__(self,conf):
		self.conf = conf
		self.cmdmappings = yaml.load(open("/project/backend/conf/cmdmappings.yaml"))
	
	def generate_tasks(self):
		monitordb.initialize_connection()
		monitor_objs = monitordb.get_monitor_objects()
		self.tasks = dict()

		for obj in monitor_objs:
			task_obj = dict()
			task_obj['monitor_type'] == obj['monitor_type']
			if (obj['addr_type'] == 'ipv4')
				task['monitor_type'] += '4' 
			if (obj['addr_type'] == 'ipv6')
				task['monitor_type'] += '6' 
			tasl
			

	def distribute_tasks(self):
		pass;
