#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python
from pathlib import Path
import os
import signal
import pyudev
from collections import UserList

# Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QTabWidget, QListView
from PyQt5.QtCore import QAbstractListModel

# Local

# Library

class Volume(object):
	"""A storage volume.
	Takes:
		- device (pyudev.Device)
			Device object as provided by pyudev."""
	def __init__(self, device):
		self.device = device
		
class Volumes(UserList):
	
	SUBSYSTEM=None #NOTE: That approach may need a little work.
	DEVTYPE=None
	
	def __init__(self):
		self.data = self.freshVolumeList
		
	@property
	def freshVolumeList(self):
		"""List of device objects."""
		
		return [Volume(d) for d in pyudev.Context().list_devices(**self.filterTerms)]
	
	@property
	def filterTerms(self):
		"""Filter terms to narrow down device selection.
		The kind of stuff you pass to pyudev.Context().list_devices().
		Returns a dict which you'll want to expand when calling pyudev matching methods."""
		filterTerms = {}
		if not self.subsystem == None:
			filterTerms["subsystem"] = self.subsystem
		if not self.devtype == None:
			filterTerms["DEVTYPE"] = self.devtype
		return filterTerms
	
	@property
	def subsystem(self):
		"""Subsystem as it would be passed to pyudev.Context().list_devices(SUBSYSTEM=)."""
		return self.__class__.SUBSYSTEM
	
	@property
	def devtype(self):
		"""Device types as it would be passed to pyudev.Context().list_devices(DEVTYPE=)."""
		return self.__class__.DEVTYPE
	
class UsbVolume(Volume):
	SUBSYSTEM="usb"

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

#printerface.exec_()
volumes = Volumes()
print(volumes)
