#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Python
from pathlib import Path

# Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QTabWidget, QListView
from PyQt5.QtCore import QAbstractListModel

# Local

# Library

class File(object):
	def __init__(self, path):
		self.path = path

class Directory(File):
	def files(self): pass
	
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
