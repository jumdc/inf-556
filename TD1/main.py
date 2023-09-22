"""Main file."""

# pylint:disable=C0303

import logging
import pyrootutils

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)

from TD1.utils.hill_climbing import HillClimbing
from TD1.utils.clustering_window import ClusteringWindow

logging.basicConfig(
    format="%(asctime)s -  %(message)s",
    level=logging.INFO,
)
logger_console = logging.getLogger(__name__)

def main(path, k_density, k_graph, tau, prefix=""):
    """main function
    
    Parameters
    ----------
    path : str
        path to the file containing the data
    k_density : int
        number of neighbors to consider for the density
    k_graph : int
        number of neighbors to consider for the graph
    tau : float
        threshold for the persistence
    prefix : str, optional
        prefix for the name of the saved files, by default ""
    """
    hill_climbing = HillClimbing(path)
    logger_console.info("Computing neighbors")
    hill_climbing.compute_neighbors(max(k_density, k_graph))
    logger_console.info("Computing density")
    hill_climbing.compute_density(k_density)
    logger_console.info("Computing graph")
    hill_climbing.compute_forest(k_graph)
    logger_console.info("Computing labels")
    hill_climbing.compute_labels()
    cluster_window = ClusteringWindow()
    cluster_window.cluster(cloud=hill_climbing.cloud, 
               labels=hill_climbing.label, 
               neighbors=hill_climbing.neighbors, 
               k=k_graph, 
               prefix=prefix, suffix="mode-seeking")

    logger_console.info("ToMATo")
    hill_climbing.compute_persistence(k_graph, tau)
    hill_climbing.compute_labels()
    cluster_window_pers = ClusteringWindow()
    cluster_window_pers.cluster(cloud=hill_climbing.cloud, 
               labels=hill_climbing.label,
               neighbors=hill_climbing.neighbors, 
               k=k_graph, 
               prefix=prefix, 
               suffix="tomato")


if __name__ == "__main__":

    logger_console.info("File text.xy")
    main(path="TD1/data/test.xy", 
         k_density=10, 
         k_graph=5, 
         tau=0.35, 
         prefix="test")

    logger_console.info("File crater.xy")
    main(path="TD1/data/crater.xy", 
         k_density=50, 
         k_graph=15, 
         tau=2, 
         prefix="crater")

    # logger_console.info("File spirals.xy")
    # main(path="TD1/data/spirals.xy", 
    #     k_density=100, 
    #     k_graph=30, 
    #     tau=0.03, 
    #     prefix="spirals")

