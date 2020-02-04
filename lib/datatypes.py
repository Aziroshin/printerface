# -*- coding: utf-8 -*-

# Python imports
from collections import UserList

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
