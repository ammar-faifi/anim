import matplotlib.pyplot as plt
import numpy as np


def plot_planck_law(
    temperatures=[3000, 4000, 5000, 6000],
    wavelength_range=(200e-9, 3000e-9),
    num_points=1000,
):
    """
    Plot Planck's law for blackbody radiation at different temperatures.

    Parameters:
    -----------
    temperatures : list
        List of temperatures in Kelvin
    wavelength_range : tuple
        Wavelength range in meters (min_wavelength, max_wavelength)
    num_points : int
        Number of points for wavelength array

    Returns:
    --------
    fig, ax : matplotlib figure and axes objects
    """

    # Physical constants
    h = 6.62607015e-34  # Planck constant (J⋅s)
    c = 299792458  # Speed of light (m/s)
    k_B = 1.380649e-23  # Boltzmann constant (J/K)

    # Create wavelength array
    wavelength = np.linspace(wavelength_range[0], wavelength_range[1], num_points)

    def planck_spectral_radiance(wavelength, temperature):
        """
        Calculate spectral radiance using Planck's law.

        B(λ,T) = (2hc²/λ⁵) × 1/(exp(hc/λkT) - 1)

        Parameters:
        -----------
        wavelength : array
            Wavelength in meters
        temperature : float
            Temperature in Kelvin

        Returns:
        --------
        array : Spectral radiance in W⋅sr⁻¹⋅m⁻³
        """
        # Avoid division by zero and overflow
        exponent = (h * c) / (wavelength * k_B * temperature)

        # Use np.clip to avoid overflow in exponential
        exponent = np.clip(exponent, 0, 700)  # e^700 is near float64 limit

        numerator = 2 * h * c**2 / (wavelength**5)
        denominator = np.expm1(
            exponent
        )  # expm1(x) = exp(x) - 1, more accurate for small x

        return numerator / denominator

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot curves for different temperatures
    colors = plt.cm.viridis(np.linspace(0, 1, len(temperatures)))

    for i, temp in enumerate(temperatures):
        spectral_radiance = planck_spectral_radiance(wavelength, temp)

        # Convert wavelength to nanometers for plotting
        wavelength_nm = wavelength * 1e9

        # Convert spectral radiance to more convenient units (kW⋅sr⁻¹⋅m⁻²⋅nm⁻¹)
        spectral_radiance_scaled = spectral_radiance * 1e-12  # Convert to kW and per nm

        ax.plot(
            wavelength_nm,
            spectral_radiance_scaled,
            color=colors[i],
            linewidth=2,
            label=f"{temp} K",
        )

    # Customize the plot
    ax.set_xlabel("Wavelength (nm)", fontsize=12)
    ax.set_ylabel("Spectral Radiance (kW⋅sr⁻¹⋅m⁻²⋅nm⁻¹)", fontsize=12)
    ax.set_title(
        "Planck's Law: Blackbody Radiation Spectrum", fontsize=14, fontweight="bold"
    )
    ax.legend(title="Temperature", fontsize=10)
    ax.grid(True, alpha=0.3)

    # Set logarithmic scale for better visualization
    # ax.set_yscale("log")

    # Add visible light region
    visible_start, visible_end = 380, 750
    ax.axvspan(
        visible_start, visible_end, alpha=0.1, color="yellow", label="Visible Light"
    )

    # Improve layout
    plt.tight_layout()

    return fig, ax


def find_wien_displacement_peak(temperature):
    """
    Find the wavelength of maximum emission using Wien's displacement law.

    λ_max = b / T, where b = 2.897771955×10⁻³ m⋅K

    Parameters:
    -----------
    temperature : float
        Temperature in Kelvin

    Returns:
    --------
    float : Peak wavelength in meters
    """
    wien_constant = 2.897771955e-3  # Wien's displacement constant (m⋅K)
    return wien_constant / temperature


# Example usage and demonstration
if __name__ == "__main__":
    # Plot standard blackbody curves
    fig, ax = plot_planck_law()

    # Add Wien's displacement law peaks
    temperatures = [3000, 4000, 5000, 6000]
    for temp in temperatures:
        peak_wavelength = find_wien_displacement_peak(temp)
        peak_wavelength_nm = peak_wavelength * 1e9

        # Find the spectral radiance at peak
        h = 6.62607015e-34
        c = 299792458
        k_B = 1.380649e-23

        exponent = (h * c) / (peak_wavelength * k_B * temp)
        numerator = 2 * h * c**2 / (peak_wavelength**5)
        denominator = np.expm1(exponent)
        peak_radiance = (numerator / denominator) * 1e-12

        # Mark the peak on the plot
        ax.plot(peak_wavelength_nm, peak_radiance, "ro", markersize=6)

    plt.show()

    # Print Wien's displacement law results
    print("\nWien's Displacement Law - Peak Wavelengths:")
    print("-" * 40)
    for temp in temperatures:
        peak_wavelength_nm = find_wien_displacement_peak(temp) * 1e9
        print(f"T = {temp} K: λ_max = {peak_wavelength_nm:.0f} nm")

    # Additional example: Solar temperature
    print(f"\nSun's surface temperature (~5778 K):")
    solar_peak = find_wien_displacement_peak(5778) * 1e9
    print(f"Peak wavelength: {solar_peak:.0f} nm (Green light)")
