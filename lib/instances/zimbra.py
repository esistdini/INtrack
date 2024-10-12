import requests
from lib.headers.headers_handler import user_agents
from lib.color_handler import print_green, print_blue, print_red, print_yellow

def check_zimbra(ip, ports=None, timeout=10):
	headers = {"User-Agent": user_agents()}
	path = "/js/zimbraMail/share/model/ZmSettings.js"
	protocols = ["http", "https"]
	if ports is None:
		ports = [80]
	else:
		ports = [f":{port}" for port in ports]
	for protocol in protocols:
		for port in ports:
			url = f"{protocol}://{ip}{port}{path}"
			try:
				response = requests.get(url, verify=False, timeout=timeout, headers=headers)
				if "Zimbra Collaboration Suite Web Client" in response.text:
					print_green(f"Zimbra detected: {url}")
					return True
			except requests.RequestException:
				continue
	return False