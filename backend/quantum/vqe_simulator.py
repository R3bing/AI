"""VQE (Variational Quantum Eigensolver) Simulator for Physics and Chemistry data.
Calculates ground state energy of molecular and spin Hamiltonians using parameterized quantum circuits.
"""

import time
from typing import Dict, Any, List
import numpy as np
from scipy.optimize import minimize


class VQESimulator:
    """Variational Quantum Eigensolver for molecular simulation and quantum chemistry."""

    def __init__(self, num_qubits: int = 2):
        self.num_qubits = num_qubits

    def _pauli_matrices(self):
        I = np.eye(2, dtype=complex)
        X = np.array([[0, 1], [1, 0]], dtype=complex)
        Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        Z = np.array([[1, 0], [0, -1]], dtype=complex)
        return I, X, Y, Z

    def build_h2_hamiltonian(self, bond_distance: float = 0.74) -> np.ndarray:
        """Constructs 2-qubit effective Hamiltonian for Hydrogen molecule H2 in STO-3G basis."""
        I, X, Y, Z = self._pauli_matrices()

        # Coefficients parameterized by interatomic bond distance R
        g0 = -0.3205 / bond_distance
        g1 = 0.1712
        g2 = -0.2227
        g3 = 0.1712
        g4 = 0.1205

        H = (
            g0 * np.kron(I, I)
            + g1 * np.kron(Z, I)
            + g2 * np.kron(I, Z)
            + g3 * np.kron(Z, Z)
            + g4 * np.kron(X, X)
        )
        return H

    def simulate_ground_state(self, bond_distance: float = 0.74) -> Dict[str, Any]:
        """Runs VQE to find the ground state energy of H2 at a specific bond distance."""
        start_time = time.perf_counter()
        H = self.build_h2_hamiltonian(bond_distance)

        # Exact diagonalization (ground truth comparison)
        exact_eigenvalues, exact_eigenvectors = np.linalg.eigh(H)
        exact_ground_energy = float(exact_eigenvalues[0])

        # Hardware-efficient ansatz simulation: |psi(theta)> = CNOT * (Ry(theta1) (x) Ry(theta2)) * |00>
        def ansatz(params):
            t1, t2 = params[0], params[1]
            # Ry gates
            Ry1 = np.array([[np.cos(t1 / 2), -np.sin(t1 / 2)], [np.sin(t1 / 2), np.cos(t1 / 2)]], dtype=complex)
            Ry2 = np.array([[np.cos(t2 / 2), -np.sin(t2 / 2)], [np.sin(t2 / 2), np.cos(t2 / 2)]], dtype=complex)
            state = np.kron(Ry1 @ np.array([1, 0]), Ry2 @ np.array([1, 0]))

            # CNOT gate (qubit 0 control, qubit 1 target)
            CNOT = np.array(
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex
            )
            return CNOT @ state

        def cost_fn(params):
            psi = ansatz(params)
            energy = np.real(np.vdot(psi, H @ psi))
            return float(energy)

        # Classical optimizer Nelder-Mead
        init_params = np.array([0.1, 0.1])
        res = minimize(cost_fn, init_params, method="Nelder-Mead", options={"maxiter": 60})

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return {
            "molecule": "H2 (Hydrogen Molecule)",
            "bond_distance_angstrom": bond_distance,
            "vqe_ground_state_energy_hartree": round(float(res.fun), 6),
            "exact_fci_energy_hartree": round(exact_ground_energy, 6),
            "absolute_error_hartree": round(abs(float(res.fun) - exact_ground_energy), 6),
            "ansatz_parameters": [round(float(p), 4) for p in res.x],
            "iterations": int(res.nfev),
            "execution_time_ms": round(elapsed_ms, 2),
        }


vqe_simulator = VQESimulator()
