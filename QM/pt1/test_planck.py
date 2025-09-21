import matplotlib.pyplot as plt
import numpy as np

h = 6.626e-34
c = 3.0e8
k = 1.38e-23

# Physical constants
h = 6.62607015e-34  # Planck constant (J⋅s)
c = 299792458  # Speed of light (m/s)
k_B = 1.380649e-23  # Boltzmann constant (J/K)

def planck(wav, T):
    a = 2.0 * h * c**2
    b = h * c / (wav * k * T)
    intensity = a / ((wav**5) * (np.exp(b) - 1.0))
    return intensity

def planck_spectral_radiance(wavelength, temperature):
    h = 6.626e-34
    c = 3.0e8
    k = 1.38e-23

    # a = 2.0 * h * c**2
    # b = h * c / (wavelength * k * temperature)
    # intensity = a / ((wavelength**5) * (np.exp(b) - 1.0))
    # return intensity

    # Avoid division by zero and overflow
    exponent = (h * c) / (wavelength * k_B * temperature)

    # Use np.clip to avoid overflow in exponential
    exponent = np.clip(exponent, 0, 700)  # e^700 is near float64 limit

    numerator = 2 * h * c**2 / (wavelength**5)
    denominator = np.expm1(
        exponent
    )  # expm1(x) = exp(x) - 1, more accurate for small x

    return numerator / denominator

wavelengths = np.arange(1e-9, 3e-6, 1e-9)
wavelengths = np.linspace(1e-9, 3e-6, 1000)

intensity4000 = planck_spectral_radiance(wavelengths, 3000.0)


plt.plot(wavelengths * 1e9, intensity4000, "r-")

# show the plot
plt.show()
