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
    
    return timestamps, values

def process_data(timestamps, values, peak_threshold=0.95, offset=2):
    threshold = max(values) * peak_threshold
    reference_time = next(t for t, v in zip(timestamps, values) if v >= threshold)
    new_start_time = reference_time + offset
    filtered_data = [(t, v) for t, v in zip(timestamps, values) if t >= new_start_time]
    filtered_timestamps, filtered_values = zip(*filtered_data)
    filtered_timestamps = [t - filtered_timestamps[0] for t in filtered_timestamps]
    mean_value = np.mean(filtered_values)
    return filtered_timestamps, filtered_values, mean_value

def align_to_peak(data_dict, reference_label="Earphone"):
    # Find the peak time in the reference (alone) dataset
    ref_timestamps, ref_values, _, _ = data_dict[reference_label]
    ref_peak_idx = np.argmax(ref_values)
    ref_peak_time = ref_timestamps[ref_peak_idx]

    aligned_data_dict = {}
    for label, (timestamps, values, mean, color) in data_dict.items():
        peak_idx = np.argmax(values)
        peak_time = timestamps[peak_idx]
        # Calculate time shift needed to align this peak to the reference peak
        time_shift = ref_peak_time - peak_time
        # Shift timestamps
        aligned_timestamps = [t + time_shift for t in timestamps]
        aligned_data_dict[label] = (aligned_timestamps, values, mean, color)
    return aligned_data_dict

def calculate_difference(mean_reference, mean_values):
    return (mean_values - mean_reference) / mean_reference * 100

def plot_data(data_dict, title, xlim=(5, 20)):
    mean_alone = data_dict["Earphone"][2]
    plt.figure(figsize=(16, 10))
    for label, data in data_dict.items():
        timestamps, values, mean, color = data
        plt.plot(timestamps, values, label=f"{label}", color=color, linewidth=2, alpha=0.7)
        if label != "Earphone":
            difference = calculate_difference(mean_alone, data_dict[label][2])
            plt.axhline(y=mean, color=color, linestyle='--', label=f"{round(mean, 2)} ({difference:.2f}%)", linewidth=4)
        else :
            plt.axhline(y=mean, color=color, linestyle='--', label=f"{round(mean, 2)}", linewidth=4)
    plt.xlabel('Time (s)', fontsize=18)
    plt.ylabel('Amplitude', fontsize=18)
    plt.xlim(*xlim)
    plt.title(title, fontsize=22)
    plt.grid(True)
    plt.legend(loc='upper right', ncols=len(data_dict), fontsize='x-large')
    plt.tight_layout()
    # plt.show()

# File paths and labels
files = {
    "Earphone": (alone_file, 'red'),
    "Silicone": (silicon_file, 'royalblue'),
    "PVC": (PVC_file, 'purple'),
    "PU": (PU_file, 'green')
}

# Load, process, and store data
data_dict = {}
for label, (file, color) in files.items():
    timestamps, values = load_data(file)
    filtered_timestamps, filtered_values, mean = process_data(timestamps, values)
    data_dict[label] = (filtered_timestamps, filtered_values, mean, color)

data_dict = align_to_peak(data_dict, reference_label="Earphone")

# Calculate differences
mean_alone = data_dict["Earphone"][2]
for label in data_dict:
    if label != "Earphone":
        difference = calculate_difference(mean_alone, data_dict[label][2])
        print(f"Difference in % ({label}): {difference:.2f}%")

# Plot data
plot_data(data_dict, title='Microphone Peak-to-Peak Signal Comparison')

save = True

if save:
    plt.savefig('images/microphone_peak_to_peak_comparison.png', dpi=300, bbox_inches='tight')
    print("Plot saved as 'microphone_peak_to_peak_comparison.png'")
else:
    plt.show()
