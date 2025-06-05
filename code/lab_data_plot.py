import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Step 1: Load the data while skipping the header
def load_data(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()[84:-7]  # Skip first 87 and last 7 lines
    from io import StringIO
    data = np.loadtxt(StringIO(''.join(lines)))
    freq = data[:, 1]  # Frequency column
    real = data[:, 2]
    imag = data[:, 3]
    return freq, real, imag

# Step 2: Convert complex values to amplitude (magnitude)
def compute_amplitude_db(real, imag, reference=0.1):
    magnitude = np.sqrt(real**2 + imag**2)
    magnitude[magnitude == 0] = 1e-12  # Avoid log(0)
    amplitude_db = 20 * np.log10(magnitude / reference)
    return amplitude_db

# Step 3: Plot the frequency response
def plot_frequency_response(frequencies, amplitudes, legend=None):
    plt.figure(figsize=(10, 6))

    for freq, amplitude, name in zip(frequencies, amplitudes, legend):
        plt.plot(freq, amplitude, label=name[-7:-4], linewidth=2)

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.legend(loc='lower left')
    plt.title("Frequency Response")
    plt.grid(True)
    plt.xscale('log')
    plt.xlim(20, 20000)  # Set x-axis limits
    plt.tight_layout()
    plt.show()

def compute_mean_with_std(reals_list, imags_list, reference=1.0):
    # Stack amplitudes in dB from multiple datasets
    db_data = []
    for real, imag in zip(reals_list, imags_list):
        db = compute_amplitude_db(real, imag, reference)
        db_data.append(db)
    
    db_array = np.vstack(db_data)  # Shape: (n_measurements, n_points)
    
    mean_db = np.mean(db_array, axis=0)
    std_db = np.std(db_array, axis=0)

    return mean_db, std_db

def plot_frequency_response_with_std(frequencies, mean_db, std_db, legend=None, colors=None, accentuate=""):
    # Plot
    plt.figure(figsize=(16, 10))

    for freq, mean, std, name, color in zip(frequencies, mean_db, std_db, legend, colors):
        plt.plot(freq, mean, label=name, color=color, linewidth=2 if color is not accentuate else 5)
        plt.fill_between(freq, mean - std, mean + std,
                        color=color, alpha=0.2)
    
    # Set a reference lina at 80 dB in dashed line
    plt.axhline(y=80, color='purple', linestyle='--', label='Benchmark (80 dB)', linewidth=2)
    plt.axvspan(50, 300, color='gray', alpha=0.2, label='50-300 Hz region')
    plt.axvspan(5000, 20000, color='red', alpha=0.2, label='> 5000 Hz region')
        
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude (dB)')
    # plt.title('Mean Frequency Response ± Std Dev')
    plt.legend(loc='lower left', fontsize='xx-large')
    plt.xscale('log')
    plt.xlim(20, 20000)  # Set x-axis limits
    plt.ylim(10, 130)  # Set y-axis limits
    plt.grid(True, which='both', ls='--', alpha=0.5)


    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=15))
    ax.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs=np.arange(2, 10)*0.1, numticks=100))
    ax.xaxis.set_minor_formatter(ticker.NullFormatter())

    plt.tight_layout()
    # plt.show()

# === Main ===
filenames = [f"lab_data/FRF_A0{i+1}.txt" for i in range(3)]  # Add more files if needed
filenames += [f"lab_data/FRF_B0{i+1}.txt" for i in range(1,4)]  # Replace with your actual filename
filenames += [f"lab_data/FRF_C0{i+1}.txt" for i in range(3)]  # Add more files if needed

baseline = ["lab_data/FRF_Baseline.txt"]
ear = ["lab_data/EarReference_1.txt"]

ref = 20e-6  # Reference value for amplitude calculation

freq, real, imag = [], [], []
for filename in filenames:
    freq_i, real_i, imag_i = load_data(filename)
    freq.append(freq_i)
    real.append(real_i)
    imag.append(imag_i)

freq_baseline, real_baseline, imag_baseline = load_data(baseline[0])
freq_ear, real_ear, imag_ear = load_data(ear[0])

amplitude_db = []  

for r, i in zip(real, imag):
    amplitude_db.append(compute_amplitude_db(r, i, reference=ref))

amplitude_db_baseline = compute_amplitude_db(real_baseline, imag_baseline, reference=ref)
amplitude_db_ear = compute_amplitude_db(real_ear, imag_ear, reference=ref*10)

mean_db, std_db = [], []

# Define the index ranges for each group (A: 0-2, B: 3-5, C: 6-8)
group_indices = [(0, 3), (3, 6), (6, 9)]
for start, end in group_indices:
    mean, std = compute_mean_with_std(real[start:end], imag[start:end], reference=ref)
    mean_db.append(mean)
    std_db.append(std)

mean_db.append(amplitude_db_baseline)
mean_db.append(amplitude_db_ear)
std_db.append(np.zeros_like(mean_db[-1]))  # Baseline std is zero
std_db.append(np.zeros_like(mean_db[-1]))  # Baseline std is zero

imgs_to_plot = {
    'A': ['blue'],
    'AB': ['blue', 'orange'],
    'ABC': ['blue', 'orange', 'green'],
    'ABC_acc': ['blue', 'orange', 'green'],
    'ABC_ref': ['blue', 'orange', 'green', 'red'],
    'ABC_ref_ear': ['blue', 'orange', 'green', 'red', 'black']
}
accents = {
    'A': "",
    'AB': "",
    'ABC': "",
    'ABC_acc': "green",
    'ABC_ref': 'red',
    'ABC_ref_ear': "black"
}

colors = ['blue', 'orange', 'green', 'red', 'black']

plot_frequency_response_with_std(freq, mean_db, std_db, legend=['Sound Box A', 'Sound Box B', 'Sound Box C', 'Baseline', 'Ear Reference'], colors=colors, accentuate="")
plt.show()

save = False
for img_name, colors in imgs_to_plot.items():
    plot_frequency_response_with_std(
        freq, 
        mean_db, 
        std_db, 
        legend=['Sound Box A', 'Sound Box B', 'Sound Box C', 'Baseline', 'Ear Reference'], 
        colors=colors, 
        accentuate=accents[img_name]
    )

    # Save the plot with the corresponding image name
    plt.title(f"Frequency Response", fontsize=25)
    img_name = f"FRF_{img_name}_v3.png"
    if save:
        plt.savefig(f'images/{img_name}', dpi=300, bbox_inches='tight')
        print(f"Saved plot as {img_name}")
    # else:
        # plt.show()