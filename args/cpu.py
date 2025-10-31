import psutil
from cpuinfo import get_cpu_info


class CPU:
	@property
	def name(self):
		return get_cpu_info().get("brand_raw")

	@property
	def usage(self):
		return psutil.cpu_percent()

	@property
	def threads(self):
		return psutil.cpu_count()

	def __str__(self):
		return self.name

	cores = count = threads
