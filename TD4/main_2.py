"""Main file."""

# pylint:disable=C0303

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
from TD4.utils_sparse import SparseComputePersistence

logging.basicConfig(
    format="%(asctime)s -  %(message)s",
    level=logging.INFO,
)
logger_console = logging.getLogger(__name__)

if __name__ == "__main__":
    # Non sparse version
    # persistence = ComputePersistence("TD4/data/filtration.xy")
    # print(len(persistence.filtration))
    # logger_console.info("Computing boundary")
    # persistence.compute_boundary()
    # print(persistence.boundary_matrix)
    # logger_console.info("Gaussian elimination")
    # reduced = persistence.gaussian_elimination()
    # logger_console.info("Output the barcode")
    # barcode = persistence.barcode_output(reduced)
    # for bar in barcode: 
    #     print(bar)

    persistence = SparseComputePersistence("TD4/data/filtration.xy")
    logger_console.info("Computing boundary")
    persistence.compute_boundary()
    logger_console.info("Gaussian elimination")
    reduced = persistence.gaussian_elimination()
    logger_console.info("Output the barcode")
    barcode = persistence.barcode_output(reduced)
    persistence.plot_barcode(barcode, name="toy")

    # # Sparse version
    # logger_console.info("Filtration A")
    # persistence = SparseComputePersistence("TD4/data/filtration_A.txt")
    # print(len(persistence.filtration))
    # logger_console.info("Computing boundary")
    # persistence.compute_boundary()
    # logger_console.info("Gaussian elimination")
    # reduced = persistence.gaussian_elimination()
    # logger_console.info("Output the barcode")
    # barcode = persistence.barcode_output(reduced)
    # persistence.plot_barcode(barcode, name="A")

    # logger_console.info("Filtration B")
    # persistence = SparseComputePersistence("TD4/data/filtration_B.txt")
    # print(len(persistence.filtration))
    # logger_console.info("Computing boundary")
    # persistence.compute_boundary()
    # logger_console.info("Gaussian elimination")
    # reduced = persistence.gaussian_elimination()
    # logger_console.info("Output the barcode")
    # barcode = persistence.barcode_output(reduced)
    # persistence.plot_barcode(barcode, name="B")

    logger_console.info("Filtration C")
    persistence = SparseComputePersistence("TD4/data/filtration_B.txt")
    print(len(persistence.filtration))
    logger_console.info("Computing boundary")
    persistence.compute_boundary()
    logger_console.info("Gaussian elimination")
    reduced = persistence.gaussian_elimination()
    logger_console.info("Output the barcode")
    barcode = persistence.barcode_output(reduced)
    persistence.plot_barcode(barcode, name="C")

    # logger_console.info("Filtration D")
    # persistence = SparseComputePersistence("TD4/data/filtration_D.txt")
    # print(len(persistence.filtration))
    # logger_console.info("Computing boundary")
    # persistence.compute_boundary()
    # logger_console.info("Gaussian elimination")
    # reduced = persistence.gaussian_elimination()
    # logger_console.info("Output the barcode")
    # barcode = persistence.barcode_output(reduced)
    # persistence.plot_barcode(barcode, name="D")