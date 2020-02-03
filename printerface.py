#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python
from pathlib import Path
import os
import signal
import pyudev
from collections import UserList, UserDict
from typing import NamedTuple
import subprocess
import psutil

# Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QTabWidget, QListView
from PyQt5.QtCore import QAbstractListModel

# Debugging
import sys

# Local

# Library

class ReadOnlyUserList(UserList):
	
	"""UserList with a blind setter method for self.data.
	Override the data property to expose the read-only list."""
	
	@property
	def data(self):
		"""Override in subclass. Has to return a list."""
		pass
	@data.setter
	def data(self):
		"""We're read-only, we don't set. Exists to make collections.UserList happy."""
		pass

class Mount(object):
	
	"""Represents an entry of /proc/mounts.
	The format of /proc/mounts is rendered as attributes, like this (one line):
		source target fstype options dumpFlag passFlag
		These correspond to self.source, self.target... you get the idea.
	Takes (str):
		source target, fstype, options, dumpFlag, passFlag
	__repr__ is customized to properly reflect these attributes and their values."""
	
	
	def __init__(self, source, target, fstype, options, dumpFlag, passFlag):
		self.source = source
		self.target = target
		self.fstype = fstype
		self.options = options
		self.dumpFlag = dumpFlag
		self.passFlag = passFlag
		
	def __repr__(self):
		return "(source={source}, target={target}, fstype={fstype}, options={options}, dump={dumpFlag}, pass={passFlag})".format(\
			source=self.source, target=self.target, fstype=self.fstype,\
			options=self.options, dumpFlag=self.dumpFlag, passFlag=self.passFlag)
		
class Mounts(ReadOnlyUserList):
	
	"""Read-only list of Mount objects."""
	
	@property
	def data(self):
		return self.fresh
	
	@data.setter
	def data(self, dataList):
		"""This needs never be written to. Exists to make collections.UserList happy."""
		pass
	
	@property
	def fresh(self):
		"""A list of Mount objects, freshly initialized from /proc/mounts."""
		rawLines = self.raw.strip().split("\n")
		mounts = []
		for line in rawLines:
			#We're working around the mount target, to avoid whitespace issues.
			source, rawRest = line.partition(" ")[0::2]
			target, fstype, options, dumpFlag, passFlag = rawRest.rsplit(" ", maxsplit=4)
			mounts.append(Mount(\
				source=source,\
				target=target,\
				fstype=fstype,\
				options=options,\
				dumpFlag=dumpFlag,\
				passFlag=passFlag\
			))
		return mounts
	
	@property
	def raw(self):
		"""Raw content of /proc/mounts."""
		with open("/proc/mounts", "r") as mountsProcFile:
			return mountsProcFile.read()

class Volume(object):
	
	"""A storage volume.
	Takes:
		- device (pyudev.Device)
			Device object as provided by pyudev."""
			
	def __init__(self, device):
		self.device = device
		
	@property
	def mountInfo(self):
		"""Mount object holding info on how we're mounted, if at all.
		Returns None if no entry could be found in /proc/mounts."""
		try:
			return list(filter(lambda m: m.source == self.device.device_node, Mounts()))[0]
		except IndexError:
			return None
	
	@property
	def mounted(self):
		"""If there is no entry in /proc/mounts, we'll consider ourselves not mounted.
		Returns True if we're mounted, False if not."""
		return not self.mountInfo is None
		
	@property
	def mountPoint(self):
		"""Path object for the mount point path.
		Returns None if we aren't mounted."""
		if self.mounted:
			return self.mountInfo.target
		else:
			return None
		
	def __repr__(self):
		return "<device={device}, mountInfo={mountInfo}>"\
			.format(device=self.device, mountInfo=self.mountInfo)
	
class UsbVolumes(ReadOnlyUserList):
	
	def __init__(self, onlyMounted=False):
		self.onlyMounted = onlyMounted
	
	@property
	def usbStorageFilterTerms(self):
		"""Filtering for these attributes will yield USB storage partitions only."""
		return {"DEVTYPE": "partition", "ID_USB_DRIVER": "usb-storage"}
	
	@property
	def data(self):
		
		""""""
		
		volumes = []
		
		for device in pyudev.Context().list_devices(DEVTYPE="partition"):
			if device.get("ID_USB_DRIVER") == "usb-storage":
				volumes.append(Volume(device))
		
		if self.onlyMounted:
			return [v for v in volumes if v.mounted]
		else:
			return volumes

class File(object):
	
	"""Handler for a file at a given path.
	Takes: 
		- path (str | Path): Path of the file."""

	def __init__(self, path):
		self.path = Path(path)
	
	@property
	def exists(self):
		"""Does a file exist at our path?"""
		return self.path.exists()
	
	def make(self):
		"""Create an empty file."""
		self.path.touch()
		 
class TextFile(File):
	
	def write(self, content):
		"""(Over)write content of the file."""
		with open(self.path, "w") as fileObject:
			fileObject.write(content)
	
	def append(self, content):
		"""Add specified string at the end of the file."""
		with open(self.path, "a") as fileObject:
			fileObject.write(content)
			
	def read(self):
		"""Return file contents."""
		with open(self.path) as fileObject:
			 return fileObject.read()
		 
class Directory(File):
	
	"""Handler for a directory type file."""
	
	@property
	def paths(self):
		"""All paths immediately in the directory (not recursive)."""
		return [p for p in self.path.iterdir()]
	
	@property
	def allPaths(self):
		"""All paths in the directory and sub-directories (recursive)."""
		return [Path(pathInfo[0]) for pathInfo in os.walk(top=self.path)]
	
	@property
	def files(self, FileType=TextFile):
		"""Every file in the directory (not recursive).
		For further details, see self.allFiles."""
		paths = []
		for path in self.paths:
			if path.is_dir:
				paths.append(self.__class__(path))
			else:
				path.append(FileType(path))
		return paths
	
	@property
	def allFiles(self, FileType=TextFile):
		"""Every file in the directory and sub-directories.
		Returns a list of handlers representing every file,
		with self.__class__ for every directory, and whatever
		class the defaultFileType parameter references for
		every non-directory path found.
		
		Takes:
			- FileType (File) (default: TextFile)
				Every non-directory path will be represented
				by an instance of this class in the resulting list.
				Designed with the File class or a sub-class thereof
				in mind."""
		paths = []
		for path in self.allPaths:
			if path.is_dir:
				paths.append(self.__class__(path))
			else:
				path.append(FileType(path))
		return paths
	
	def make(self):
		"""Create directory."""
		self.path.mkdir()
		
class Document(File): pass

class FileListModel(QAbstractListModel):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.files = []
		#test
		self.files.append("lala")
	def data(self, index, role):
		return self.files[index.row()]
	def rowCount(self, parent=None):
		return len(self.files)

class Tabs(QTabWidget):
	def __init__(self):
		super().__init__()
		self.filesTab = QListView()
		self.filesTab.setModel(FileListModel())
		self.addTab(self.filesTab, "Files")

class Printerface(QApplication):
	pass

# ============================================
# Below follows some caveman dev-code
# for caveman prototyping and testing.
# ============================================

# ============================================
# Prepare GUI

# Make ctrl+c work with Qt by restoring SIGINT's default behaviour.
signal.signal(signal.SIGINT, signal.SIG_DFL)

printerface = Printerface([])
#printerface._setUp()

# Layout
layout = QVBoxLayout()
layout.addWidget(QPushButton("Scan"))
# Tabs
layout.addWidget(Tabs())
# Window
window = QWidget()
window.setLayout(layout)
window.show()

# ============================================
# Work towards getting file list.
volumes = UsbVolumes(onlyMounted=True)
#partitions = lambda p: p if p.device in [v.device.device_node for v in volumes] else None
#print([n for n in psutil.disk_partitions()])
#print([m for m in map(partitions, psutil.disk_partitions())])
#print([f for f in filter(lambda p: p.device in [v.device.device_node for v in volumes], psutil.disk_partitions())])
#print(["Links: "+"".join([l for l in v.device.device_links]) for v in volumes])

print([v.mountPoint for v in volumes])

# ============================================
# Get GUI.
#printerface.exec_()
