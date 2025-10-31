import psutil


class Disk:
	def __init__(self):
		self._disk = psutil.disk_usage("/")

	@property
	def percent(self):
		return self._disk.percent

	@property
	def total(self):
		return self._disk.total / 1073741824

	@property
	def used(self):
		return self._disk.total / 1073741824

	@property
	def free(self):
		return self._disk.total / 1073741824

	def __str__(self):
		return f"{self.percent}%"
