import psrchive
import numpy as np
import matplotlib.pyplot as plt

# Load the archive

name = 'L2049635_SAP000_B004' 
arch = psrchive.Archive_load(name + '.med')
arch.dedisperse()
arch.remove_baseline()
arch.convert_state('Stokes')

# Create a figure with 2x2 subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle(name + '.med')
# 1) Fully scrunched pulsar profile (Flux over phase)
profile_arch = arch.clone()
profile_arch.fscrunch()
#profile_arch.bscrunch()
profile_arch.tscrunch()
profile_data = profile_arch.get_data()

# Extract phase bins and flux
flux = profile_data[0, 0, 0, :]  # First pol, first freq channel, first subint
phase_bins = np.linspace(0, 1, len(flux))

axs[0, 0].plot(phase_bins, flux, 'k-')
axs[0, 0].set_xlabel("Pulse Phase")
axs[0, 0].set_ylabel("Flux Density")


# 2) Frequency vs Phase (Intensity map)
arch_freq = arch.clone()
arch_freq.bscrunch_to_nbin(256)
#arch_freq.fscrunch_to_nchan(512)
data_freq = arch_freq.get_data()

freq_lo = arch_freq.get_centre_frequency() - arch_freq.get_bandwidth() / 2.0
freq_hi = arch_freq.get_centre_frequency() + arch_freq.get_bandwidth() / 2.0

im1 = axs[0, 1].imshow(data_freq[:, 0, :, :].mean(0), extent=(0, 1, freq_lo, freq_hi), 
                        aspect='auto', origin='lower', cmap='viridis')
axs[0, 1].set_xlabel("Pulse Phase")
axs[0, 1].set_ylabel("Frequency (MHz)")

fig.colorbar(im1, ax=axs[0, 1], label="Flux Density")

# 3) Time vs Phase (Intensity map)
arch_time = arch.clone()
arch_time.bscrunch_to_nbin(256)
#arch_time.tscrunch_to_nsubint(100)  # Reduce to 100 time bins for better resolution
data_time = arch_time.get_data()

im2 = axs[1, 0].imshow(data_time[:, 0, :, :].mean(1), extent=(0, 1, 0, data_time.shape[0]), 
                        aspect='auto', origin='lower', cmap='viridis')
axs[1, 0].set_xlabel("Pulse Phase")
axs[1, 0].set_ylabel("Time (Subintegrations)")
fig.colorbar(im2, ax=axs[1, 0], label="Flux Density")

# 4) Dynamic Spectrum (Frequency vs Time)
arch_dynspec = arch.clone()
arch_dynspec.bscrunch_to_nbin(256)
data_dynspec = arch_dynspec.get_data()

im3 = axs[1, 1].imshow(data_dynspec[:, 0, :, :].mean(-1), extent=(0, data_dynspec.shape[0], freq_lo, freq_hi), 
                        aspect='auto', origin='lower', cmap='viridis')
axs[1, 1].set_xlabel("Time (Subintegrations)")
axs[1, 1].set_ylabel("Frequency (MHz)")
fig.colorbar(im3, ax=axs[1, 1], label="Flux Density")

# Adjust layout
plt.tight_layout()
#plt.show()
plt.savefig(name + '.png')

