# -*- coding: utf-8 -*-

# Python
import json
import subprocess
from collections import UserDict

class LsblkSelector(object):
	
	"""Determines the selection of items for Lsblk objects.
	This is where the selection of columns as well as items
	in general from lsblk output for a Lsblk object is determined."""
	
	@property
	def columns(self):
		"""A list determining column selection.
		The default columns in the non-overriden method are:
			name,maj:min,size,ro,type,mountpoint"""
		return ["name", "maj:min", "size", "ro", "type", "mountpoint"]
	
	def filter(self, item):
		
		"""This is passed to the Lsblk objects' filtering method.
		
		Intended to be subclassed. Always returns True if not overriden.
		
		This is used during post-init in order to alter the 
		dataset as it was provided by lsblk. It's primarily
		intended to enable filtering 
		
		Takes .items() of dictified lsblk JSON data.
		Returns True if the item is to be included in the
		selection, False if it's not."""
		
		return True

class Lsblk(UserDict):
	
	#TODO: Should probably be be a "read-only" dict.
	
	"""UserDict initialized with lsblk JSON data.
	Takes:
		- selector (LsblkSelector):
			If no initial data is specified, will get fresh data
			from lsblk, with the columns as specified in the
			selector and subsequently filtered according to
			the selector's filter method.
		- initialData (dict):
			If specified, will initialize from this instead of
			getting fresh data through lsblk.
			Mind that _initWithLsblkData and _initFilter will not
			be executed, and that the selector only
			serves reference purposes if this is specified."""
			
	def __init__(self, selector=LsblkSelector(), initialData={}):
		self.selector = selector
		if initialData:
			self.data = initialData
		else: 
			if self.columnCount > 0:
				self._initWithLsblkData()
			self._initFilter()
			
	@property
	def columnCount(self):
		return len(self.selector.columns)
	
	@property
	def columnsAsString(self):
		"""Columns as a comma-separated string."""
		return ",".join(self.selector.columns)
		
	@property
	def fresh(self):
		"""Raw JSON output (str) as received from lsblk."""
		return subprocess.check_output(["lsblk", "-b", "--json", "-o", self.columnsAsString])
	
	@property
	def freshAsDict(self):
		"""JSON output as received from lsblk, but as dict."""
		return json.loads(self.fresh)
	
	def _initWithLsblkData(self):
		"""Init dict with lsblk data.
		Mainly serves the purpose of easy subclassing."""
		self.data = self.freshAsDict
		
	def _initFilter(self):
		"""Filter the dict according to the selector's filter method."""
		self.data = dict(filter(self.selector.filter, self.data.items()))
	
class LsblkBlockdevices(Lsblk):
	
	"""The blockdevice list as provided by lsblk, as a dict object.
		The first column is used as a key, but is still contained
		in the corresponding data dict as well.
		Example:
			[{"kname": "lala", "type": "disk"}] becomes:
			{"lala": {"kname": "lala", "type": "disk"}}"""
	
	@property
	def asList(self):
		"""The blockdevice list as provided by lsblk, as a list object."""
		return self.freshAsDict["blockdevices"]
	
	@property
	def asDict(self):
		"""Blockdevices list as first-column keyed dict."""
		blockdevicesDict = {}
		for deviceData in self.asList:
			deviceName = deviceData[self.selector.columns[0]]
			blockdevicesDict[deviceName] = deviceData
		return blockdevicesDict
	
	def _initWithLsblkData(self):
		"""Init dict with the the blockdevices portion of lsblk data only."""
		self.data = self.asDict
		
	def columnAsList(self, column):
		"""Returns list of all fields in the specified column."""
		return [self.data[kname][column] for kname in self.data.keys()]
