import pyrootutils
import logging

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)

logging.basicConfig(
    format="%(asctime)s -  %(message)s",
    level=logging.INFO,
)
logger_console = logging.getLogger(__name__)

from TD1.utils.hill_climbing import HillClimbing
from TD1.utils.clustering_window import ClusteringWindow


def main(path, k_density, k_graph, tau):
    hc = HillClimbing(path)
    logger_console.info("Computing neighbors")
    # display the point cloud
    cw = ClusteringWindow()
    cw.cluster(cloud= hc.cloud, labels=[i for i in range(len(hc.cloud))], suffix="point-cloud")

    hc.compute_neighbors(max(k_density, k_graph))
    logger_console.info("Computing density")
    hc.compute_density(k_density)
    logger_console.info("Computing graph")
    hc.compute_forest(k_graph)
    logger_console.info("Computing labels")
    hc.compute_labels()
    cw = ClusteringWindow()
    cw.cluster(cloud=hc.cloud, labels=hc.label, neighbors=hc.neighbors, k=k_graph, suffix="mode-seeking")


    logger_console.info("ToMATo")
    hc.compute_persistence(k_graph, tau)
    hc.compute_labels()
    cw = ClusteringWindow()
    cw.cluster(cloud=hc.cloud, labels=hc.label, neighbors=hc.neighbors, k=k_graph, suffix="persistence")


if __name__ == "__main__":

    logger_console.info("File text.xy")
    path = "TD1/data/test.xy"
    k_density = 10
    k_graph = 5
    tau = 0.35
    main(path, k_density, k_graph, tau)

    # logger_console.info("File crater.xy")
    # path = "TD1/data/crater.xy"
    # k_density = 50
    # k_graph = 15
    # tau = 2
    # main(path, k_density, k_graph, tau)


