import logging
import pyrootutils
import os

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)

from TD4.utils import ComputePersistence


if __name__ == "__main__":
    persistence = ComputePersistence("TD4/data/filtration.xy")
    persistence.compute_boundary()
    reduced = persistence.gaussian_elimination()
    barcode = persistence.barcode_output(reduced)
    for bar in barcode: 
        print(bar)
    persistence.plot_barcode(barcode)