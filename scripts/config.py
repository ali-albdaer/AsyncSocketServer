"""Configuration for the async socket server/client.

HOST is auto-detected to the local IPv4 address in the 192.168.1.x subnet
when available, otherwise falls back to 'localhost'.
"""

import socket


def _detect_192_168_1_ip() -> str | None:
	"""Return the first local IPv4 address matching 192.168.1.* if found.

	Tries a few strategies using only Python's standard library (no external deps):
	- Hostname resolution (gethostbyname_ex)
	- getaddrinfo on the current hostname
	- UDP 'connect' trick to the typical gateway 192.168.1.1 to infer the bound IP
	"""
	candidates: set[str] = set()

	# 1) Hostname -> IPs
	try:
		hostname = socket.gethostname()
		host_ips = socket.gethostbyname_ex(hostname)[2]
		candidates.update(host_ips)
	except Exception:
		pass

	# 2) getaddrinfo for hostname
	try:
		infos = socket.getaddrinfo(socket.gethostname(), None, family=socket.AF_INET)
		candidates.update(ai[4][0] for ai in infos)
	except Exception:
		pass

	# 3) UDP connect trick to a likely gateway on this subnet
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
			# No packets are actually sent; this sets routing/binding
			s.connect(("192.168.1.1", 1))
			candidates.add(s.getsockname()[0])
	except Exception:
		pass

	for ip in candidates:
		if ip.startswith("192.168.1."):
			return ip

	return None


HOST = _detect_192_168_1_ip() or "localhost"
PORT = 8000
PRINT_COLOR = True  # Print colored text in terminal