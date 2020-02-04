#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python imports
import signal
import subprocess

# Qt imports
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QTabWidget, QListView
from PyQt5.QtCore import QAbstractListModel

# Debugging imports
import sys

# Local imports
from lib.filemanagement import UsbVolumes

# Library

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
print([v.mountPoint for v in volumes])

# ============================================
# Get GUI.
#printerface.exec_()
