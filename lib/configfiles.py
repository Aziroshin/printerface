# -*- coding: utf-8 -*-

# Python
from configparser import ConfigParser

# Local
from lib.filemanagement import File

class ConfigFile(File):
	
	def __init__(self, path):
		super().__init__(path)
		self.config = ConfigParser()
		self.config.update(self.default)
	
	@property
	def default(self):
		"""Returns a dict with the default values.
		This is used to initialize with default values, but
		may also serve external reference purposes.
		
		Meant to be overriden in subclass."""
		return {}
	
	def read(self):
		"""Reads the file and returns the updated config ConfigParser object."""
		self.config.read(self.path)
		return self.config
		
	def write(self):
		"""Writes the state of the ConfigParser object to the file."""
		with open(self.path, "w") as fileObject:
			self.config.write(fileObject)
			
