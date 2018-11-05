#!/usr/bin/env python
from __future__ import absolute_import
from contextlib import contextmanager
import time
import datetime
import json
import os, shutil
import zipfile

from virtualbox import VirtualBox
from virtualbox import Session
from virtualbox.library import LockType
from virtualbox.library import SessionState
from virtualbox.library import DeviceType
from virtualbox.library import DeviceActivity
from virtualbox.library import OleErrorUnexpected

VBOX_MACHINE_NAME = 'Malware'
VBOX_USER_NAME = 'Malware'
VBOX_PASSWORD = 'password'
VICTIMS_FOLDER_IN = 'Z:\\VictimsSharedFolder'
VICTIMS_FOLDER_OUT = 'Z:\\Victims\\'

class Malware:
	def init(self):
		with open("run.json", "r") as file:
			run = json.load(file)
			for commands in run:
				vbox = VirtualBox()
				session = Session()
				vm = vbox.find_machine(VBOX_MACHINE_NAME)
				p = vm.launch_vm_process(session, 'gui', '')
				p.wait_for_completion(60 * 1000)
				session = vm.create_session()
				gs = session.console.guest.create_session(VBOX_USER_NAME, VBOX_PASSWORD, timeout_ms = 300 * 1000)
				for command in commands:
					print("Command: %s" % (command['command']))
					print("Parameters: %s" % (command['parameters']))
					print("Sleep: %s" % (command['sleep']))
					try:
						process, stdout, stderr = gs.execute(command['command'], command['parameters'], timeout_ms = 30 * 1000)
						print(stdout)
						time.sleep(int(command['sleep']))
					except:
						pass

				self._power_down(session)
				self._extract_victims(VICTIMS_FOLDER_IN, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
				self._delete_victims(VICTIMS_FOLDER_IN)
			
	def _power_down(self, session):
		vbox = VirtualBox()
		vm = vbox.find_machine(session.machine.name)
		try:
			p = session.console.power_down()
			p.wait_for_completion(60 * 1000)
			try:
				if session.state == SessionState.locked:
					session.unlock_machine()
			except OleErrorUnexpected:
				# session seems to become unlocked automatically after
				# wait_for_completion is called after the power_down?
				pass
			session = vm.create_session(LockType.write)
			p = session.machine.restore_snapshot()
			p.wait_for_completion(60 * 1000)
			return vm
		finally:
			if session.state == SessionState.locked:
				session.unlock_machine()
				
	def _extract_victims(self, path, zip_name):
		shutil.make_archive(VICTIMS_FOLDER_OUT + zip_name, 'zip', path)
		
	def _delete_victims(self, path):
		for file in os.listdir(path):
			file_path = os.path.join(path, file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path): shutil.rmtree(file_path)
			except Exception as e:
				print(e)
				
	def _zipdir(self, path, ziph):
		for root, dirs, files in os.walk(path):
			for file in files:
				ziph.write(os.path.join(root, file))
				
malware = Malware()
malware.init()