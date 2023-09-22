"""Implementation of the ClusteringWindow class."""

import math
from random import random, seed
from matplotlib import pyplot as plt

class ClusteringWindow:
    """
    Class to display the clustering of the points.
    """
    def __init__(self, thickness = 0.5) -> None:
        self.x_max, self.x_min = - math.inf, math.inf
        self.y_max, self.y_min = - math.inf, math.inf
        self.thickness = thickness

    
    def update(self, x, y):
        """
        Updates the max/min coordinates to get a centered plot.

        Parameters
        ----------
        x : float
            x coordinate of the point
        y : float
            y coordinate of the point
        """
        if x < self.x_min:
            self.x_min = x - self.thickness
        if x > self.x_max:
            self.x_max = x + self.thickness
        if y < self.y_min:
            self.y_min = y - self.thickness
        if y > self.y_max:
            self.y_max = y + self.thickness
        

    def cluster(self, cloud, labels, neighbors=[], k=1, prefix="", suffix=""):
        """
        Creates a plot of the clusters, and saves it. 

        Parameters
        ----------
        cloud : List
            list of the points
        label : List
            list of the cluster label of each point
        neighbors : List
            list of the neighbors of each point
        k : int
            number of neighbors per point to be displayed
        """
        seed(1999)
        c = [
            [random(), random(), random()] for c in range(len(labels))
        ]
        colors = [c[l] for l in labels]
        for point in cloud: 
            self.update(point.coords[0], point.coords[1])
        figure , ax = plt.subplots(figsize=(10, 10))
        ax.grid(False)
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.set_title(f"Clustering, number of clusters: {len(list(set(labels)))}")
        x = [point.coords[0] for point in cloud]
        y = [point.coords[1] for point in cloud]
        ax.scatter(x, y, c=colors)
        for neigh in neighbors:
            for i in range(1, min(k, len(neigh))):
                ax.plot(
                    [cloud[neigh[0]].coords[0], cloud[neigh[i]].coords[0]],
                    [cloud[neigh[0]].coords[1], cloud[neigh[i]].coords[1]],
                    color="grey",
                    linewidth=0.1,
                )
        plt.savefig(f"{prefix}_res_{suffix}.png")
        plt.close()
        