import matplotlib.pyplot as plt
import numpy as np

# Constants
h = 6.626e-34  # Planck's constant (J·s)
c = 3.0e8  # Speed of light (m/s)
k = 1.38e-23  # Boltzmann constant (J/K)
T = 5000  # Temperature (K)

# Wavelength range in micrometers
lambda_micrometers = np.linspace(0.1, 3, 1000)
lambda_meters = lambda_micrometers * 1e-6  # Convert to meters


# Planck's radiation law
def planck(wav, T):
    a = 8 * np.pi * h * c / wav**5
    b = h * c / (wav * k * T)
    return a / (np.exp(b) - 1)


B_planck = planck(lambda_meters, T)


# Rayleigh-Jeans law
def rayleigh_jeans(wav, T):
    return 8 * np.pi * k * T / wav**4


B_rj = rayleigh_jeans(lambda_meters, T)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(lambda_micrometers, B_planck, "b", label="Planck's Law")
plt.plot(lambda_micrometers, B_rj, "k--", label="Classical Theory (Rayleigh-Jeans)")

# Fill the ultraviolet catastrophe region
plt.fill_between(
    lambda_micrometers,
    B_planck,
    B_rj,
    where=(B_rj > B_planck),
    color="red",
    alpha=0.3,
    label="Ultraviolet Catastrophe",
)

# Formatting
plt.xlabel("Wavelength (µm)", fontsize=12)
plt.ylabel("Spectral Radiance (W·sr⁻¹·m⁻³)", fontsize=12)
plt.title("Ultraviolet Catastrophe: Classical vs Quantum Prediction", fontsize=14)
plt.yscale("log")  # Logarithmic scale to handle large ranges
plt.legend()
plt.grid(True, which="both", linestyle="--", alpha=0.7)
plt.tight_layout()

plt.show()
