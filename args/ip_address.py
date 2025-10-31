class IPAddress:
	def __init__(self, data: dict[str, str]):
		self._data = data

	@property
	def ip(self) -> str:
		return self._data.get("ip")

	@property
	def code(self) -> str:
		return self._data.get("country")

	country = code

	@property
	def hostname(self) -> str:
		return self._data.get("hostname")

	@property
	def city(self) -> str:
		return self._data.get("city")

	@property
	def region(self) -> str:
		return self._data.get("region")

	@property
	def postal(self) -> str:
		return self._data.get("postal")

	@property
	def timezone(self) -> str:
		return self._data.get("timezone")

	@property
	def organization(self) -> str:
		return self._data.get("org")

	org = organization

	@property
	def loc(self) -> str:
		return self._data.get("loc")
