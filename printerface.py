#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python imports
import signal
import subprocess
from pathlib import Path

# Qt imports
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QTabWidget, QListView, QMainWindow
from PyQt5.QtCore import QAbstractListModel, QAbstractTableModel
from PyQt5 import uic

# Debugging imports
import sys

# Local imports
from lib.filemanagement import UsbVolumes
from lib.configfiles import ConfigFile

# Library

class FileListModel(QAbstractTableModel):
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.files = []
		#test
		self.files.append("lala")
	
	def data(self, index, role):
		return self.files[index.row()]
	
	def rowCount(self, parent=None):
		return len(self.files)
	
class UsbVolumeListModel(QAbstractTableModel):
	
	def __init__(self, parent=None):
		self.mountedVolumes = UsbVolumes(onlyMounted=True)
	
	def data(self, index, role):
		return self.mountedVolumes[index.row()]
	
	def setData(self):
		pass#TODO
	
	def flags(self):
		pass#TODO
	
	def rowCount(self, parent=None):
		return len(self.mountedVolumes)
	
	def columnCount(self, parent=None):
		return 1
	
	
class Tabs(QTabWidget):
	def __init__(self):
		super().__init__()
		self.filesTab = QListView()
		self.filesTab.setModel(FileListModel())
		self.addTab(self.filesTab, "Files")
		
class PrinterfaceWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi(Path(Path(__file__).resolve().parent, "ui/main.ui"), self)
		self._initUi()
		self.show()
		
	def _initUi(self):
		"""Sets up the layout according to the .ui file.
		If changes to the .ui file are made, this is where it's at."""
		from PyQt5.QtWidgets import QTabWidget
		self.tabs = self.findChild(QTabWidget, "tabs")
		
class PrinterfaceApp(QApplication):
	pass

# ============================================
# Below follows some caveman dev-code
# for caveman prototyping and testing.
# ============================================

# ============================================
# Prepare GUI

# Make ctrl+c work with Qt by restoring SIGINT's default behaviour.
signal.signal(signal.SIGINT, signal.SIG_DFL)

printerfaceApp = PrinterfaceApp([])
window = PrinterfaceWindow()
#printerface._setUp()

## Layout
#layout = QVBoxLayout()
#layout.addWidget(QPushButton("Scan"))
## Tabs
#layout.addWidget(Tabs())
## Window
#window = QWidget()
#window.setLayout(layout)
#window.show()

# ============================================
# Work towards getting file list.
volumes = UsbVolumes(onlyMounted=True)
print([v.mountPoint for v in volumes])

# ============================================
# Get GUI.
#printerfaceApp.exec_()
