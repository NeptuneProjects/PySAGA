#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union

import numpy as np


class CovarianceMatrixDimensionError(Exception):
    """Raised when the covariance matrix has the wrong dimensions."""

    pass


def readascii(filename: Path):
    return


def write_covmat(
    covariance_matrix: np.ndarray,
    freqs: Union[np.ndarray, list],
    depths: Union[np.ndarray, list],
) -> str:
    (M, N, F) = covariance_matrix.shape

    if M != N:
        raise CovarianceMatrixDimensionError("The covariance matrix must be square.")
    if F != len(freqs):
        raise CovarianceMatrixDimensionError(
            "The covariance matrix must have the same number of frequencies as the frequency vector."
        )
    if M != len(depths):
        raise CovarianceMatrixDimensionError(
            "The covariance matrix must have the same number of depths as the depth vector."
        )

    fidout = "cov.in"

    with open(fidout, "w") as f:
        for ff, freq in enumerate(freqs):
            f.write(" estimated covariance matrices using dpss\n")
            f.write(f"{freq:.6f}     0.000 dB\n")
            f.write(f"{int(N):d}\n")
            [f.write(f"{depth:.6f}\n") for depth in depths]

            Cx = covariance_matrix[:, :, ff]
            for i, row in enumerate(Cx):
                # print(row, file=sys.stderr)  # Why do this??
                for j, col in enumerate(row):
                    f.write(
                        f"{i+1}".rjust(10)
                        + f"{j+1}".rjust(10)
                        + f" ({np.real(col):.6e},{np.imag(col):.6e})"
                        + "\n"
                    )
        f.write("!  \n")
        return fidout


def write_dformat(pres: np.ndarray, comment: str) -> str:
    (nfr, nr, nd) = pres.shape

    fidout = "pres.in"

    with open(fidout, "w") as f:
        f.write(f"! {comment}\n")
        f.write("! frequencies range depth pressure \n")
        for i in range(nfr):
            for j in range(nr):
                for k in range(nd):
                    f.write(
                        f" {i+1} {j+1} {k+1}   "
                        + f"({np.real(pres[i,j,k]):.6e}, {np.imag(pres[i,j,k]):.6e}) \n"
                    )
        f.write("!  \n")
    return fidout


if __name__ == "__main__":
    N = 10  # Number of sensors
    F = 7  # Number of frequencies
    freqvec = np.linspace(10, 100, F)
    cov = np.random.randn(N, N, F) + 1j * np.random.randn(N, N, F)
    depths = np.linspace(50, 150, N)
    write_covmat(cov, freqvec, depths)

    NR = 3
    ranges = np.linspace(0, 1000, NR)
    pres = np.random.randn(F, NR, N) + 1j * np.random.randn(F, NR, N)
    write_dformat(pres, "test comment")
