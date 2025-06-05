import csv
import matplotlib.pyplot as plt
import numpy as np

silicon_file = 'logs/tube_silicon_1.csv'
alone_file = 'logs/earphon_silicon_1.csv'
PU_file = 'logs/tube_PU_1.csv'
PVC_file = 'logs/tube_PVC_1.csv'
# silicon_bent_file = 'logs/tube_silicone_bent_1.csv'


def load_data(file_name):
    timestamps = []
    values = []

# Check if the file exists
    try:
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2:
                    timestamps.append(float(row[0]))
                    values.append(int(row[1]))
    except FileNotFoundError:
        print(f"File {file_name} not found. Please check the path and try again.")
        exit(1)

    start_time = timestamps[0]
    timestamps = [t - start_time for t in timestamps]
    
    return timestamps,values

def process_data(timestamps, values, peak_threshold=0.95, offset=2):
    # Step 1: Find the reference high peak
    threshold = max(values) * peak_threshold
    reference_time = next(t for t, v in zip(timestamps, values) if v >= threshold)

    # Step 2: Define new start time
    new_start_time = reference_time + offset

    # Step 3: Filter the data after this time
    filtered_data = [(t, v) for t, v in zip(timestamps, values) if t >= new_start_time]

    # Step 4: Unpack the filtered data
    filtered_timestamps, filtered_values = zip(*filtered_data)

    # Optional: Normalize again to start at 0
    filtered_timestamps = [t - filtered_timestamps[0] for t in filtered_timestamps]

    # Calculate mean
    mean_value = np.mean(filtered_values)

    return filtered_timestamps, filtered_values, mean_value

# Load data
timestamps_tube, values_tube = load_data(silicon_file)
timestamps_alone, values_alone = load_data(alone_file)
timestamps_PU, values_PU = load_data(PU_file)
timestamps_PVC, values_PVC = load_data(PVC_file)
# timestamps_silicon_bent, values_silicon_bent = load_data(silicon_bent_file)

# Process data
timestamps_tube_filtered, values_tube_filtered, mean_tube = process_data(timestamps_tube, values_tube)
timestamps_alone_filtered, values_alone_filtered, mean_alone = process_data(timestamps_alone, values_alone)
timstamps_PU, values_PU_filtered, mean_PU = process_data(timestamps_PU, values_PU)
timestamps_PVC, values_PVC_filtered, mean_PVC = process_data(timestamps_PVC, values_PVC)
# timstamp_silicon_bent, values_silicon_bent_filtered, mean_silicon_bent = process_data(timestamps_silicon_bent, values_silicon_bent)

print(f"Mean Peak-to-Peak (Alone): {mean_alone}")
print(f"Mean Peak-to-Peak (Silicone): {mean_tube}")
print(f"Mean Peak-to-Peak (PVC): {mean_PVC}")
# print(f"Mean Peak-to-Peak (Silicone Bent): {mean_silicon_bent}")
print(f"Mean Peak-to-Peak (PU): {mean_PU}")

# Optional: Calculate the difference in %
difference = (mean_tube - mean_alone) / mean_alone * 100
difference_PU = (mean_PU - mean_alone) / mean_alone * 100
difference_PVC = (mean_PVC - mean_alone) / mean_alone * 100
# difference_silicon_bent = (mean_silicon_bent - mean_alone) / mean_alone * 100

print(f"Difference in %: {difference:.2f}%")
print(f"Difference in % (PVC): {difference_PVC:.2f}%")
# print(f"Difference in % (Silicon Bent): {difference_silicon_bent:.2f}%")
print(f"Difference in % (PU): {difference_PU:.2f}%")

# Step 5: Plot

label_alone = 'Earphone / mean = ' + str(round(mean_alone, 2))
label_tube = 'Silicone / mean = ' + str(round(mean_tube, 2))
label_PVC = 'PVC / mean = ' + str(round(mean_PVC, 2))
# label_silicon_bent = 'Silicone Bent / mean = ' + str(round(mean_silicon_bent, 2))
label_PU = 'PU / mean = ' + str(round(mean_PU, 2))
title = 'Microphone Peak-to-Peak Signal Comparison'

plt.figure(figsize=(10, 5))

# Plot the data
plt.plot(timestamps_alone_filtered, values_alone_filtered, label=label_alone, color='red', alpha=0.7)
plt.plot(timestamps_tube_filtered, values_tube_filtered, label=label_tube, color='royalblue', linewidth=2)
plt.plot(timestamps_PVC, values_PVC_filtered, label=label_PVC, color='purple', linewidth=2)
# plt.plot(timstamp_silicon_bent, values_silicon_bent_filtered, label=label_silicon_bent, color='orange', linewidth=2)
plt.plot(timstamps_PU, values_PU_filtered, label=label_PU, color='green', linewidth=2)


# Means
plt.axhline(y=mean_alone, color='red', linestyle='--', label='Earphone')
plt.axhline(y=mean_tube, color='royalblue', linestyle='--', label='Silicon')
plt.axhline(y=mean_PVC, color='purple', linestyle='--', label='PVC')
# plt.axhline(y=mean_silicon_bent, color='orange', linestyle='--', label='Silicon Bent')
plt.axhline(y=mean_PU, color='green', linestyle='--', label='PU')

plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.xlim(0, 15)

plt.title(title)
plt.grid(True)
plt.legend(loc='upper right', ncols=2)
plt.tight_layout()
plt.show()