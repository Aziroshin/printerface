# -*- coding: utf-8 -*-

# Python imports
import subprocess
from pathlib import Path

# Project imports
from lib.datatypes import ReadOnlyUserList
from lib.lsblk import LsblkBlockdevices, LsblkSelector
from lib.lsblkselectors import LsblkUsbSelector

class Volume(object):
	
	"""A storage volume.
	Takes:
		- device (pyudev.Device)
			Device object as provided by pyudev."""
			
	def __init__(self, kname, mountpoint, label, uuid, model, size, deviceType, subsystems):
		self.device
		
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
			return Path(self.mountInfo.target)
		else:
			return None
		
	def __repr__(self):
		return "<device={device}, mountInfo={mountInfo}>"\
			.format(device=self.device, mountInfo=self.mountInfo)
		
class UsbVolumes(ReadOnlyUserList):
	
	"""A list of Volume objects for USB device hosted partitions.
		If self.onlyMounted, will contain mounted ones only.
		Otherwise, it'll contain all USB volumes it finds."""
	
	def __init__(self, onlyMounted=False, lsblkSelector=LsblkUsbSelector()):
		self.lsblkSelector = lsblkSelector
		self.onlyMounted = onlyMounted
		self._cached = None
	
	@property
	def lsblkColumns(self):
		"""List of columns lsblk should return data for."""
		return ["kname", "mountpoint", "label", "uuid", "model", "size", "type", "subsystems"]
	
	@property
	def data(self):
		"""Returns cached (maybe stale) list of USB volumes."""
		return self.cached
		
	@property
	def cached(self):
		"""A fresh or stale list of USB volumes."""
		if self._cached == None:
			self.refreshCache()
		return self._cached
		
	@property
	def fresh(self):
		"""A fresh list of USB volumes."""
		volumes = []
		lsblkVoumes = LsblkBlockdevices(self.lsblkSelector)
		return volumes
		
		
	def refreshCache(self):
		"""Initialize in-memory cache with a fresh list of USB volumes."""
		self._cached = self.fresh
