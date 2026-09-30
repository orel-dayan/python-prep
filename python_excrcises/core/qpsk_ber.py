"""QPSK modulation over an AWGN channel: how link quality (SNR) drives BER.

Maps random bit pairs onto QPSK constellation points, adds complex Gaussian
noise scaled to a target SNR, demodulates with a hard decision, and reports
the resulting bit error rate. Run across a few SNR values to see the BER
drop as the simulated link improves.
"""

from __future__ import annotations

import numpy as np


def simulate_ber(snr_db: float, num_symbols: int = 1000, seed: int = 0) -> float:
    rng = np.random.default_rng(seed=seed)

    bits = rng.integers(0, 2, size=(num_symbols, 2))
    symbols = ((2 * bits[:, 0] - 1) + 1j * (2 * bits[:, 1] - 1)) / np.sqrt(2)

    noise_power = 10 ** (-snr_db / 10)
    noise = np.sqrt(noise_power / 2) * (
        rng.standard_normal(num_symbols) + 1j * rng.standard_normal(num_symbols)
    )
    received = symbols + noise

    decoded = np.column_stack((received.real > 0, received.imag > 0)).astype(int)
    return float(np.mean(decoded != bits))


if __name__ == "__main__":
    for snr_db in (0, 5, 10):
        ber = simulate_ber(snr_db)
        print(f"SNR={snr_db} dB, BER={ber:.4f}")
