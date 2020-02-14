#-*- coding: utf-8 -*-

# Project imports
from lib.lsblk import LsblkSelector

class LsblkUsbSelector(LsblkSelector):
	
	"""Selects USB devices only.
	Must include "subsystems" column, lest the filtering will fail."""
	
	@property
	def columns(self):
		"""This makes sure the "subsystems" column is included."""
		return super().columns+["subsystems"]
	
	def filter(self, item):
		"""Filters out any non-USB devices."""
		# .split is used to make exact string matches, not substring.
		return "usb" in item[1]["subsystems"].split(":")
		return False
