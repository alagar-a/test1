import monitorit.db as monitordb
import yaml
import os
import subprocess

class TaskGenerator:
	def __init__(self,conf):
		self.conf = conf
		self.cmdmappings = yaml.load(open("/project/backend/conf/cmdmappings.yaml"))
	
	def generate_tasks(self):
		monitordb.initialize_connection()
		monitor_objs = monitordb.get_monitor_objects()
		self.tasks = list()

		needs_processing = 0;
		for obj in monitor_objs:
			if (obj['state'] == 'PROCESSED'):
				pass;
			else:
				needs_processing = 1;
				break;

		if (needs_processing == 0):
			print "all tasks are already processed."
			return;
				
		for obj in monitor_objs:
			task_obj = dict()
			task_obj['frequency'] = obj['polling_frequency']

			task_obj['monitor_type'] = obj['monitor_type']
			if (obj['addr_type'] == 'ipv4'):
				task_obj['monitor_type'] += '4' 
			if (obj['addr_type'] == 'ipv6'):
				task_obj['monitor_type'] += '6' 
				
			cmd = self.cmdmappings[task_obj['monitor_type']]		
			if ('port' in obj['monitor_type']): 
				(host,port) = obj['addr'].split(':')
				task_obj['command'] = cmd.format(host,port)
			else:
				task_obj['command'] = cmd.format(obj['addr'].format('addr'))
			self.tasks.append(task_obj)
		print "task generation done"
##		print self.tasks
				
	def distribute_tasks(self):
		if (len(self.tasks) == 0):
			print "no tasks to distribute .. exiting .."
			return
		
		pollers = self.conf["poller"];
		
		split_tasks = zip(*[iter(self.tasks)]*(len(self.tasks)/len(pollers)))
	
		self.hosttotaskfile = dict()	
		for i in range(0,len(pollers)):
			dirname = self.conf['tasks_location']+pollers[i];
			if not os.path.exists(dirname):
				os.makedirs(dirname)
			filename = dirname + "/tasks.yaml"
			with open(filename,'w') as yaml_file:
				yaml.dump(split_tasks[i], yaml_file, default_flow_style=False)
			
			self.hosttotaskfile[pollers[i]] = filename
		
		for k in self.hosttotaskfile.keys():
			rsync_cmd = "/usr/bin/rsync -vrz --timeout=10 --password-file=/etc/rsync.password "+self.hosttotaskfile[k]+" monitit@"+k+"::share"
			try: 
				output = subprocess.check_output(rsync_cmd, shell=True)
			except Exception as e:
				print str(e)

		print "task distribution done"
