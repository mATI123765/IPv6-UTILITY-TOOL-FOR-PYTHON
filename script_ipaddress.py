# Expander and shortener IPv6

import ipaddress

print("")
print("")
print("/////////////////////////////////////////")
print("//////////////IPv6 SHORTENER/////////////")
print("////By Matias Acosta & Jorge Ferrando////")
print("/////////////////////////////////////////")
print("")
print("In this version will contain the following:")
print("1. IPv6 Shortener, our own version.")
print("2. IPv6 Expender, our own version.")

# Hi Vicente this is our IPv6 conversor I hope you like it.

print("")
print("Give me your full IPv6 address or shorter address and this program will shorten it and expand it for you.")
user_IP = input("IPv6: ")
print("")

print(user_IP)

# This function making use of the ipaddress library collapses the IPv6 address and returns it with a port, if it can't be shortened, it will return the port and the full address.
#
# def ipshortener () :
# 	result = [ipaddr for ipaddr in
#	ipaddress.collapse_addresses([ipaddress.IPv6Network(user_IP),
# 	ipaddress.IPv6Address(user_IP)])]
# 	print(result)
# ipshortener()

# This is our own function that reads the user input and, when theres 4 zeros, it replaces the user's ip to a shortened version, where the 4 zeros are replaced to ::
def ipshortenerPRO():
	ip = user_IP
	changed = False
	# Keeps collapsing any literal ":0000:" runs until there are none left.
	while ":0000:" in ip:
		ip = ip.replace(":0000:", "::")
		changed = True
	# this while loop, prevents the "ip.replace to add too many :: and replaces the extra : with two.
	while ":::" in ip: 
		ip = ip.replace(":::", "::")
	while ip.count("::") > 1:
		ip = ip.replace("::", ":0000:")
	while ip.startswith("0000:"):
		ip = ip.replace("0000:", "::", 1)
	while ip.endswith(":0000"):
		ip = ip[::-1].replace("0000:", "::", 1)[::-1]
	while ip.startswith(":"):
		ip = ip.replace(":", "0000:", 1)
	while ip.endswith(":"):
		ip = ip[::-1].replace(":", ":0000", 1)[::-1]
		changed = True
	# this if checks if any change was made, if so it prints the shortened ip, else it tells the user that his ip cant be shortened.
	if changed:
		print(ip)
		return ip
	else:
		print("")
		print(user_IP + " This is not a valid IPv6 Address.")
		print("Your IP Address can't be shortened bro, why are you sending it through here.")
		return user_IP
ipshortenerPRO()