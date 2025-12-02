#  IPv6 Expander and shortener

# Can use this 3 versions of IPv6 to verify the program:
# 2001:db8::ff00:42:8329 (Shortest ver.)
# fe80:0000:0000:0000:0000:0000:0000:0001 (Expanded ver.)
# 2001:db8:0:0:1::1 (Normalized ver.)

import ipaddress

print("")
print("")
print("/////////////////////////////////////////")
print("//////////////Address IPv6///////////////")
print("////By Matias Acosta & Jorge Ferrando////")
print("/////////////////////////////////////////")
print("")
print("In this version will contain the following:")
print("1. Expand IPv6 addresses to full format.")
print("2. Shorten IPv6 addresses to compressed format.")
print("")
# Hi Vicente this is our IPv6 conversor I hope you like it.

# Expands an IPv6 address to its full format (all 8 groups, 4 hex digits each)
def ipv6_expander(ip_str):
	ip_str = ip_str.strip()

	# Handle :: expansion
	if '::' in ip_str:
		# Split by ::
		parts = ip_str.split('::')
		if len(parts) != 2:
			return None  # Invalid: more than one ::
		
		left = parts[0].split(':') if parts[0] else []
		right = parts[1].split(':') if parts[1] else []

		# Remove empty strings
		left = [x for x in left if x]
		right = [x for x in right if x]

		# Calculate how many groups of zeros to add
		missing = 8 - len(left) - len(right)
		if missing < 0:
			return None  # Invalid: too many groups
		
		# Combine with zeros in the middle
		groups = left + ['0'] * missing + right
	else:
		groups = ip_str.split(':')

	# Check if we have exactly 8 groups
	if len(groups) != 8:
		return None
	
	# Validate and pad each group to 4 hex digits
	expanded = []
	for group in groups:
		if not group:
			return None
		# Check if valid hex
		if not all(c in '0123456789abcdefABCDEF' for c in group): # Invalid hex character
			return None
		if len(group) > 4:
			return None
		# Pad to 4 digits
		expanded.append(group.zfill(4).lower()) # Pad with leading zeros and convert to lowercase

	return ':'.join(expanded) # Return the expanded IPv6 address

# Shortens an IPv6 address following standard compression rules
def ipv6_shortener(ip_str):
	expanded = ipv6_expander(ip_str) # First expand to get a valid full address
	if not expanded:
		return None

	groups = expanded.split(':') # Split into groups

	# Remove leading zeros from each group
	groups = [group.lstrip('0') or '0' for group in groups]

	# Find the longest run of consecutive '0' groups
	max_start = -1
	max_len = 0
	current_start = -1
	current_len = 0

	# Find the longest run of consecutive '0' groups
	for i, group in enumerate(groups):
		if group == '0': 
			if current_start == -1: # Start of a new run
				current_start = i
				current_len = 1
			else:
				current_len += 1
		else:
			if current_len > max_len: # New max found
				max_start = current_start
				max_len = current_len
				current_start = -1
				current_len = 0
	
	# Check the last run
	if current_len > max_len:
		max_start = current_start
		max_len = current_len
	
	# Replace the longest run with ::
	if max_len > 1:
		left = groups[:max_start]
		right = groups[max_start + max_len:]

		# Build the shortened address
		if max_start == 0 and max_start + max_len == 8:
			return '::'
		elif max_start == 0:
			return '::' + ':'.join(right)
		elif max_start + max_len == 8:
			return ':'.join(left) + '::'
		else:
			return ':'.join(left) + '::' + ':'.join(right)
	else:
		return ':'.join(groups)

# Main program
print("Please enter an IPv6 address to expand and shorten:")
user_IP = input("IPv6: ")
print("")

# Validate and process the IPv6 address
expanded = ipv6_expander(user_IP)
shortened = ipv6_shortener(user_IP)

# Display results
if expanded and shortened:
	print("")
	print("")
	print(f"Original input:    {user_IP}")
	print(f"Expanded format:   {expanded}")
	print(f"Shortened format:  {shortened}")
	print("")

	# Show if any changes were made
	if user_IP == shortened:
		print("Your address is already in the shortest valid format.")
		print("")
	elif user_IP == expanded:
		print("Your address was in full format, now shortened.")
		print("")
	else:
		print("Your address has been normalized.")
		print("")
else: 
	print(f"Error: '{user_IP}' is not a valid IPv6 address.")
	print("")

# This function making use of the ipaddress library collapses the IPv6 address and returns it with a port, if it can't be shortened, it will return the port and the full address.
#
# def ipshortener () :
# 	result = [ipaddr for ipaddr in
#	ipaddress.collapse_addresses([ipaddress.IPv6Network(user_IP),
# 	ipaddress.IPv6Address(user_IP)])]
# 	print(result)
# ipshortener()