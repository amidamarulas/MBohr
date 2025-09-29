# src/bohratom/core.py
"""
Módulo core: contiene la clase BohrAtom con métodos para:
 - energy(n)
 - radius(n)
 - transition_energy(n_i, n_f)
 - frequency(n_i, n_f)
 - wavelength(n_i, n_f)
Unidades por defecto: energía -> eV, radios -> metros, longitud de onda -> metros.
"""

from __future__ import annotations
from typing import Union
import math

# Constantes (CODATA 2019/2018 exactas donde aplica)
_h = 6.62607015e-34           # J·s
_hbar = _h / (2 * math.pi)
_e = 1.602176634e-19          # C (elemental charge)
_m_e = 9.1093837015e-31       # kg (masa del electrón)
_epsilon0 = 8.8541878128e-12  # F/m (permitividad del vacío)
_c = 299792458.0              # m/s (velocidad de la luz)

class BohrAtom:
    """
    Clase que representa un átomo hidrogenoide según el modelo de Bohr.
    Parámetros:
        Z (int): número atómico (carga nuclear), Z=1 para hidrógeno.
    """
    def __init__(self, Z: int = 1):
        if Z < 1:
            raise ValueError("Z debe ser >= 1")
        self.Z = int(Z)
        # Constantes asociadas al objeto (pueden sobreescribirse si se desea)
        self._h = _h
        self._hbar = _hbar
        self._e = _e
        self._m_e = _m_e
        self._epsilon0 = _epsilon0
        self._c = _c

        # Bohr radius a0 (para Z=1)
        self.a0 = 4 * math.pi * self._epsilon0 * self._hbar**2 / (self._m_e * self._e**2)

    def energy_joule(self, n: int) -> float:
        """Energía del nivel n en julios (valor negativo)."""
        if n < 1:
            raise ValueError("n debe ser >= 1")
        # E_n = - (m_e * e^4 * Z^2) / (8 * epsilon0^2 * h^2 * n^2)
        E = - (self._m_e * self._e**4 * self.Z**2) / (8 * self._epsilon0**2 * self._h**2 * n**2)
        return E

    def energy(self, n: int, unit: str = "eV") -> float:
        """Energía del nivel n. unit='eV' o 'J'."""
        E_j = self.energy_joule(n)
        if unit.lower() == "j":
            return E_j
        elif unit.lower() == "ev":
            return E_j / self._e
        else:
            raise ValueError("Unidad desconocida. Use 'eV' o 'J'.")

    def radius(self, n: int) -> float:
        """Radio de la órbita para nivel n (en metros). r_n = a0 * n^2 / Z"""
        if n < 1:
            raise ValueError("n debe ser >= 1")
        return self.a0 * n**2 / self.Z

    def transition_energy_joule(self, n_i: int, n_f: int) -> float:
        """ΔE = E_f - E_i en julios (puede ser negativo)."""
        E_i = self.energy_joule(n_i)
        E_f = self.energy_joule(n_f)
        return E_f - E_i

    def transition_energy(self, n_i: int, n_f: int, unit: str = "eV") -> float:
        """Valor absoluto de la energía intercambiada (emisión o absorción)."""
        dE_j = self.transition_energy_joule(n_i, n_f)
        if unit.lower() == "j":
            return abs(dE_j)
        elif unit.lower() == "ev":
            return abs(dE_j) / self._e
        else:
            raise ValueError("Unidad desconocida. Use 'eV' o 'J'.")

    def frequency(self, n_i: int, n_f: int) -> float:
        """Frecuencia del fotón asociado (Hz): nu = |ΔE| / h"""
        dE = abs(self.transition_energy_joule(n_i, n_f))
        return dE / self._h

    def wavelength(self, n_i: int, n_f: int) -> float:
        """Longitud de onda en metros: lambda = c / nu"""
        nu = self.frequency(n_i, n_f)
        return self._c / nu

    def __repr__(self) -> str:
        return f"<BohrAtom Z={self.Z} a0={self.a0:.3e} m>"

