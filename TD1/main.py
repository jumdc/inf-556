import pyrootutils
import logging

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
    hc = HillClimbing(path)
    logger_console.info("Computing neighbors")
    hc.compute_neighbors(max(k_density, k_graph))
    logger_console.info("Computing density")
    hc.compute_density(k_density)
    logger_console.info("Computing graph")
    hc.compute_forest(k_graph)
    logger_console.info("Computing labels")
    hc.compute_labels()
    cw = ClusteringWindow()
    cw.cluster(cloud=hc.cloud, labels=hc.label, 
               neighbors=hc.neighbors, k=k_graph, 
               prefix=prefix, suffix="mode-seeking")

    logger_console.info("ToMATo")
    hc.compute_persistence(k_graph, tau)
    hc.compute_labels()
    cw = ClusteringWindow()
    cw.cluster(cloud=hc.cloud, labels=hc.label,
                neighbors=hc.neighbors, k=k_graph, 
                prefix=prefix, suffix="tomato")


if __name__ == "__main__":

    logger_console.info("File text.xy")
    path = "TD1/data/test.xy"
    k_density = 10
    k_graph = 5
    tau = 0.35
    main(path, k_density, k_graph, tau, prefix="test")

    logger_console.info("File crater.xy")
    path = "TD1/data/crater.xy"
    k_density = 50
    k_graph = 15
    tau = 2
    main(path, k_density, k_graph, tau, prefix="crater")

    logger_console.info("File crater.xy")
    path = "TD1/data/spirals.xy"
    k_density = 100
    k_graph = 30
    tau = 0.03
    main(path, k_density, k_graph, tau, prefix="spirals")


