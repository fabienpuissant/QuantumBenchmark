import numpy as np
import matplotlib.pyplot as plt

import qiskit
from qiskit.providers.aer.noise.errors.standard_errors import thermal_relaxation_error
from qiskit.providers.aer.noise import NoiseModel
from qiskit.ignis.characterization.coherence import t1_circuits, t2_circuits, T1Fitter
from qiskit.providers.aer import*


def t1_noise_model(gate_time=0.1, t=[70.5, 85.0, 80.0, 90.5, 77.5]):
    """
    Return a NoiseModel object for T1.
    
    Parameters
        - gate_time: gate time (in microseconds) for a single-qubit gate
        - t: simulated times (in microseconds) for a set of five qubits 
    """
    
    t1_noise_model = NoiseModel()
    error = [0 for i in range(5)]
    
    for i in range(5):
        error[i] = thermal_relaxation_error(t[i], 2*t[i], gate_time)
        t1_noise_model.add_quantum_error(error[i], 'id', [i])
    
    return t1_noise_model


def t2_star_noise_model(gate_time=0.1, t=[70.5, 85.0, 80.0, 90.5, 77.5]):
    """
    Return a NoiseModel object for T2*.
    
    Parameters
        - gate_time: gate time (in microseconds) for a single-qubit gate
        - t: simulated times (in microseconds) for a set of five qubits 
    """

    t2_star_noise_model = NoiseModel()
    error = [0 for i in range(5)]
    
    for i in range(5):
        error[i] = thermal_relaxation_error(np.inf, t[i], gate_time, 0.5)
        t2_star_noise_model.add_quantum_error(error[i], 'id', [i])
    
    return t2_star_noise_model

def exponential(x, a, b, c):
    return a * np.exp(-b * x) + c

def T2_func(x, a, b, c, phi):
    return a * np.exp(- 2* b* x) * np.sin(phi) + c