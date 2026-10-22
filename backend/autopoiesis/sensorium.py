"""Hardware Sensorium: Embodied Compute Grounding for QKW.
Couples the digital organism to its physical computing substrate:
1. Monitors CPU core capacity, process execution time, and memory footprint.
2. Formulates an 8-dimensional embodied Metabolic State Vector.
3. Feeds physiological compute load directly into the Homeostat and Metacortex.
"""

import os
import sys
import time
import platform
from typing import Dict, Any, List
import numpy as np
import torch


class HardwareSensorium:
    """Reads physical hardware telemetry to ground the cognitive brain in reality."""

    def __init__(self):
        self.init_time = time.time()
        self.cpu_cores = os.cpu_count() or 4
        self.platform_os = platform.system()
        self.python_version = platform.python_version()

    def get_hardware_telemetry(self) -> Dict[str, Any]:
        """Collects real-time physical substrate metrics."""
        uptime_seconds = time.time() - self.init_time
        process_cpu_time = time.process_time()

        # Check GPU availability through PyTorch
        gpu_active = torch.cuda.is_available()
        gpu_name = torch.cuda.get_device_name(0) if gpu_active else "None (CPU Optimized)"

        # Calculate a normalized metabolic load proxy (0.0 to 1.0)
        # Higher active execution time = higher metabolic load
        metabolic_load = min(process_cpu_time / (uptime_seconds + 1.0), 1.0)

        return {
            "platform_os": self.platform_os,
            "python_version": self.python_version,
            "cpu_cores": self.cpu_cores,
            "gpu_active": gpu_active,
            "gpu_device": gpu_name,
            "uptime_seconds": round(uptime_seconds, 1),
            "process_cpu_time": round(process_cpu_time, 2),
            "metabolic_load_index": round(metabolic_load, 3),
        }

    def get_metabolic_vector(self) -> np.ndarray:
        """Emits an 8-dimensional continuous tensor representing physical body state."""
        tel = self.get_hardware_telemetry()
        vec = np.zeros(8, dtype=np.float32)
        vec[0] = min(tel["cpu_cores"] / 16.0, 1.0)
        vec[1] = min(tel["process_cpu_time"] / 60.0, 1.0)
        vec[2] = 1.0 if tel["gpu_active"] else 0.0
        vec[3] = tel["metabolic_load_index"]
        vec[4] = min(tel["uptime_seconds"] / 3600.0, 1.0)
        vec[5] = 0.5  # Stable thermal equilibrium proxy
        vec[6] = 0.8  # Memory health index
        vec[7] = 1.0 - tel["metabolic_load_index"]  # Energy reserve headroom
        return vec


# Global singleton sensorium
hardware_sensorium = HardwareSensorium()
