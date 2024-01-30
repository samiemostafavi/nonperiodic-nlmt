import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import gzip
import sys

if len(sys.argv) != 2:
    print("Usage: python validate.py <file_name.json.gz>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    # Open the gzip file and load JSON data
    with gzip.open(file_path, 'rb') as f:
        json_data = f.read().decode('utf-8')
    
except FileNotFoundError:
    print("File not found:", file_path)

# Parse JSON data into a dictionary
data_dict = json.loads(json_data)
send_times = []
for item in data_dict['oneway_trips']:
    if 'wall' in item['timestamps']['client']['send']:
        send_times.append(item['timestamps']['client']['send']['wall'])

send_times_ms = np.array(send_times)/1.0e+6
frame_number = np.floor(send_times_ms/10.0)
frame_number = np.array(frame_number,dtype=np.int64)
offsets = send_times_ms-(frame_number*10.0)

fig, ax = plt.subplots(1,1, figsize=(10,6))
ax.hist(offsets, density=True, bins=100)
ax.set_xlim([0,9])

ax.set_xlabel("Delay [ms]")
ax.set_ylabel('PDF')
# Adjust layout
plt.tight_layout()

# Save the figure to a file
plt.savefig("validate.jpg")