#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python
from pathlib import Path
import os

# Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QTabWidget, QListView
from PyQt5.QtCore import QAbstractListModel

# Local

# Library

class File(object):
<<<<<<< HEAD
	
	"""Handler for a file at a given path.
	Takes: 
		- path (str | Path): Path of the file."""
	
=======
>>>>>>> c4f55705ed7d13f4594959622c97380a4fe96d87
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

printerface.exec_()
