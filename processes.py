# Importing libraries
import os
import re
import sys
import time
import psutil
import inspect
import fileinput
import subprocess
import detect_hands

file_path = 'processList.txt'

def getArgs():
	'''Returns GestureDriving class constructor's arguments'''
	return inspect.getargspec(func=detect_hands.GestureDriving.__init__)


def processFile():
	'''Returns a list of app-paths enlisted in collection'''
	app_paths = []
	with open(file=file_path, mode='r') as f:
		for line in f:
			app_paths.append(line.strip())
	if not app_paths:
		print('No Processes enlisted!')
		return None
	return app_paths


def convert(p):
	'''
	`Input`
		- p: psutil.Process object

	`Output`
		- Returns Process Path: str
	'''
	return p.exe().strip()


def lstDisplay(lst, exe=False):
	'''
	`Input`
		- lst: A list object
		- exe: A boolean value. If exe is `true`, lst values are expected to be psutil.Process object

	`Output`
		- Display/Echo the list values
	'''
	if lst:
		proc_paths = lst.copy()
		if exe:
			proc_paths = list(map(convert, proc_paths))
		for i, proc_path in enumerate(iterable=proc_paths, start=1):
			print('{}. {}'.format(i, proc_path), sep=' ', end='\n', flush=False)


def processTxt(txt):
	'''
	`Input`
		- txt: a str object
	
	`Output`
		- Returns the input str without any quotes
	'''
	return (re.sub(pattern="\"|\'", repl="", string=txt).strip() + '\n')


def runningProcesses():
	'''Returns a list of running process's paths'''
	procs = []
	for proc in psutil.process_iter():
		try:
			if convert(p=proc)[-4:] == '.exe':
				procs.append(proc)
		except:
			continue
	return procs


def runCall(process, arguments=None):
	'''
	`Input`
		- process: a psutil.Process object
		- arguments: a dictionary object of args

	`Output`
		- Calls GestureDriving program
	'''
	if arguments:
		gest = detect_hands.GestureDriving(proc=process, **arguments)
	else:
		gest = detect_hands.GestureDriving(proc=process)
	gest.execute()


def run(args=None):
	'''
	`Input`
		- args: a dictionary object of args

	`Ouput`
		- Runs GestureDriving program for specified enlisted program
	'''
	while True:
		app_paths = processFile()
		if app_paths:
			running_procs = runningProcesses()
			for proc in running_procs:
				if convert(p=proc) in app_paths:
					print('Found: {}'.format(proc.name()), sep=' ', end='\n', flush=False)
					runCall(process=proc, arguments=args)
		else:
			print('Entering into Demo Mode...', sep=' ', end='\n', flush=False)
			runCall(process=proc, arguments=args)


def handleArg(key=None, value=None):
	'''
	`Input`
		- key: A command-line optional argument
		- value: Command-line optional argument's value

	`Output`
		- Determines the process on the basis of key & value
	'''
	if key:
		if (key == 'displayRunning'):
			lstDisplay(lst=runningProcesses(), exe=True)

		elif (key == 'displayEnlisted'):
			lstDisplay(lst=processFile(), exe=False)

		elif (key == 'add'):
			new_paths = []
			for n in range(value):
				new_paths.append(processTxt(txt=input('Enter new path: ')))
			with open(file=file_path, mode='a') as f:
				f.writelines(new_paths)
			del(new_paths)
			print('Successfully added new path(s) to collection!', sep=' ', end='\n', flush=False)

		elif (key == 'remove'):
			lstDisplay(lst=processFile(), exe=False)
			rm_lst = list(map(int, input('Enter line numbers to be removed (space-separated): ').split()))
			for line_number, line in enumerate(fileinput.input(files=file_path, inplace=1), start=1):
				flag = True
				for i, rm in enumerate(iterable=rm_lst, start=0):
					if (line_number == rm):
						rm_lst.pop(i)
						flag = False
						break
				if flag:
					sys.stdout.write(line)
			print('Successfully removed path(s) from collection!', sep=' ', end='\n', flush=False)

		elif (key == 'edit'):
			if sys.platform.startswith('win'):
				# !notepad "$file_path"
				# subprocess.Popen(("notepad", file_path)).wait()
				os.system(command="notepad {}".format(file_path))
			elif sys.platform.startswith('linux'):
				os.system(command="gedit {}".format(file_path))

		elif (key == 'default_configuration'):
			args = getArgs()
			for i, (arg_key, arg_value) in enumerate(zip(args.args[2:], args.defaults), start=1):
				print('{}. {}: {}'.format(i, arg_key, arg_value), sep=' ', end='\n', flush=False)

		elif (key == 'configure'):
			arg_dct = {}
			args = getArgs()
			for arg_key, arg_default, arg_value in zip(args.args[2:], args.defaults, value):
				if (arg_value == -1):
					arg_dct[arg_key] = arg_default
				else:
					arg_dct[arg_key] = arg_value
			run(args=arg_dct)

	else:
		run(args=None)