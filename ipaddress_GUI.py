# IPv6 Expander and Shortener with GUI
# By Matias Acosta & Jorge Ferrando

# Can use this 3 versions of IPv6 to verify the program:
# 2001:db8::ff00:42:8329 (Shortest ver.)
# fe80:0000:0000:0000:0000:0000:0000:0001 (Expanded ver.)
# 2001:db8:0:0:1::1 (Normalized ver.)

import tkinter as tk
from tkinter import ttk, messagebox

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
        if not all(c in '0123456789abcdefABCDEF' for c in group):
            return None
        if len(group) > 4:
            return None
        # Pad to 4 digits
        expanded.append(group.zfill(4).lower())

    return ':'.join(expanded)

# Shortens an IPv6 address following standard compression rules
def ipv6_shortener(ip_str):
    expanded = ipv6_expander(ip_str)
    if not expanded:
        return None

    groups = expanded.split(':')

    # Remove leading zeros from each group
    groups = [group.lstrip('0') or '0' for group in groups]

    # Find the longest run of consecutive '0' groups
    max_start = -1
    max_len = 0
    current_start = -1
    current_len = 0

    for i, group in enumerate(groups):
        if group == '0':
            if current_start == -1:
                current_start = i
                current_len = 1
            else:
                current_len += 1
        else:
            if current_len > max_len:
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

# GUI Functions
def convert_ipv6():
    user_ip = input_entry.get().strip()
    
    if not user_ip:
        messagebox.showwarning("Empty Input", "Please enter an IPv6 address dumbass.")
        return
    
    # Clear previous results
    default_label.config(text="")
    expanded_label.config(text="")
    shortened_label.config(text="")
    status_label.config(text="", fg="black")
    
    # Process the IPv6 address
    expanded = ipv6_expander(user_ip)
    shortened = ipv6_shortener(user_ip)
    
    if expanded and shortened:
        # Display results
        default_label.config(text=f"Original input:    {user_ip}")
        expanded_label.config(text=f"Expanded format:   {expanded}")
        shortened_label.config(text=f"Shortened format:  {shortened}")
        
        # Determine status message
        if user_ip == shortened:
            status_label.config(text="✓ Your address is already in the shortest valid format.", fg="green")
        elif user_ip == expanded:
            status_label.config(text="✓ Your address was in full format, now shortened.", fg="green")
        else:
            status_label.config(text="✓ Your address has been normalized.", fg="green")
    else:
        messagebox.showerror("Invalid Address", f"'{user_ip}' is not a valid IPv6 address.")

# Clear all fields after use the program
def clear_fields():
    input_entry.delete(0, tk.END)
    default_label.config(text="")
    expanded_label.config(text="")
    shortened_label.config(text="")
    status_label.config(text="")

# Create main window
root = tk.Tk()
root.title("IPv6 Expander & Shortener")
root.geometry("750x500")
root.resizable(True, True)
root.configure(bg="#f0f0f0")
root.eval('tk::PlaceWindow . center')

# Title Frame
title_frame = tk.Frame(root, bg="#2c3e50", height=80)
title_frame.pack(fill="x")

# Title label
title_label = tk.Label(
    title_frame,
    text="IPv6 Address Converter",
    font=("Arial", 20, "bold"),
    bg="#2c3e50",
    fg="white"
)
title_label.pack(pady=15)

# Subtitle label
subtitle_label = tk.Label(
    title_frame,
    text="By Matias Acosta & Jorge Ferrando",
    font=("Arial", 10),
    bg="#2c3e50",
    fg="#ecf0f1"
)
subtitle_label.pack()

# Main content frame
content_frame = tk.Frame(root, bg="#f0f0f0")
content_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Input section
input_frame = tk.Frame(content_frame, bg="#f0f0f0")
input_frame.pack(pady=10)

input_label = tk.Label(
    input_frame,
    text="Enter IPv6 Address:",
    font=("Arial", 12, "bold"),
    bg="#f0f0f0"
)
input_label.pack(anchor="w")

input_entry = tk.Entry(input_frame, width=50, font=("Courier", 11))
input_entry.pack(pady=5, ipady=5)

# Buttons section
button_frame = tk.Frame(content_frame, bg="#f0f0f0")
button_frame.pack(pady=15)

# Convert IPv6 button
convert_btn = tk.Button(
    button_frame,
    text="Convert",
    command=convert_ipv6,
    bg="#27ae60",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12,
    height=1,
    cursor="hand2"
)
convert_btn.pack(side="left", padx=5)

# Clear button
clear_btn = tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    bg="#e74c3c",
    fg="white",
    font=("Arial", 11, "bold"),
    width=12,
    height=1,
    cursor="hand2"
)
clear_btn.pack(side="left", padx=5)

# Results section
results_frame = tk.Frame(content_frame, bg="white", relief="solid", borderwidth=1)
results_frame.pack(pady=15, padx=10, fill="both", expand=True)

# Results title in label
results_title = tk.Label(
    results_frame,
    text="Results:",
    font=("Arial", 12, "bold"),
    bg="white",
    anchor="w"
)
results_title.pack(anchor="w", padx=10, pady=(10, 5))

# Default label
default_label = tk.Label(
    results_frame,
    text="",
    font=("Courier", 10),
    bg="white",
    anchor="w",
    justify="left"
)
default_label.pack(anchor="w", padx=20, pady=2)

# Expanded label
expanded_label = tk.Label(
    results_frame,
    text="",
    font=("Courier", 10),
    bg="white",
    anchor="w",
    justify="left"
)
expanded_label.pack(anchor="w", padx=20, pady=2)

# Shortened label
shortened_label = tk.Label(
    results_frame,
    text="",
    font=("Courier", 10),
    bg="white",
    anchor="w",
    justify="left"
)
shortened_label.pack(anchor="w", padx=20, pady=2)

# Status label with the results
status_label = tk.Label(
    results_frame,
    text="",
    font=("Arial", 10, "italic"),
    bg="white",
    anchor="w"
)
status_label.pack(anchor="w", padx=20, pady=(10, 10))

# Bind Enter key to convert
input_entry.bind('<Return>', lambda event: convert_ipv6())

# Run the main program
root.mainloop()