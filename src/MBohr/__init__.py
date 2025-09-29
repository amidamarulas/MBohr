# src/bohratom/__init__.py
"""bohratom: librería para cálculos y visualizaciones del modelo de Bohr."""
from .core import BohrAtom
from .plotting import plot_energy_levels, plot_orbits

__all__ = ["BohrAtom", "plot_energy_levels", "plot_orbits"]
__version__ = "0.1.0"
