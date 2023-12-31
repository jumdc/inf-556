"""Implementation of the Hill Climbing algorithm."""

import math
from TD1.utils.point import Point


class HillClimbing:
    """
    Implementation of the Hill Climbing algorithm.

    Attributes
    ----------
    cloud : List
        list to store the points
    neighbors : List
        list to store the indices of the neighbors of the data points. 
        One List per point.
    density : List
        list to store the density of the points
        one value per point
    parent : List
        list of the parent of each point in its cluster tree
    label : List
        list of cluster label of each point
    
    """
    def __init__(self, file) -> None:
        self.cloud, self.neighbors, self.density = [], [], []
        self.parent, self.label = [], []
        self.read_data(file)

    def __str__(self) -> str:
        """Str overload"""
        res = "Cloud: "
        for idx in self.cloud[:-1]:
            res += str(idx) + ", "
        return res + str(self.cloud[-1])

    def read_data(self, file) -> None:
        """
        Read the data from the file and store it in the cloud attribute.

        Parameters
        ----------
        path : str
            path to the file containing the data
        """
        with open(file, "r") as f:
            for line in f:
                coords = line.split()
                coords = [float(c) for c in coords]
                self.cloud.append(Point(coords))


    def compute_neighbors(self, k) -> None:
        """
        Compute the neighbors of each point and store them in the neighbors attribute.

        Parameters
        ----------
        k: int
            number of neighbors to consider
        """
        # for each point in the point cloud, let's compute its neighbors
        distances  = [0 for i in self.cloud]
        neighbors = [0 for i in self.cloud]
        for point in self.cloud:
            c = 0
            for other_point in self.cloud:
                distances[c] = Point.sqrt_distance(point, other_point)
                neighbors[c] = c
                c += 1
            # sort the neighbors by distance
            neighbors.sort(key=lambda x: distances[x])
            k_p = min(k, len(neighbors) - 1)
            self.neighbors.append(neighbors[1:k_p+1]) # start at one to exclude the point itself

    def compute_density(self, k) -> None:
        """
        Compute the density of each point and store it in the density attribute.
        Use the distance to a measure density estimate.

        Parameters
        ----------
        k: int
            number of neighbors to consider
        """
        for idx in range(len(self.cloud)):
            f = 0
            for idx_j in range(0, k):
                f +=  Point.sqrt_distance(self.cloud[idx], 
                                          self.cloud[self.neighbors[idx][idx_j]]) ** 2
            f = 1 / math.sqrt(f / k) # inverse of the average of the square root
            self.density.append(f)

    def compute_forest(self, k) -> None:
        """
        Connects each data point to its parent, 
        which is its neighbor in the k-NN graph with highest density 
        value among the ones with strictly higher density (if they exist) 
        or itself (otherwise).

        Parameters
        ----------
        k: int
            number of neighbors to consider
        """
        for idx in range(len(self.cloud)):
            p = idx # temp parent
            for idx_j in range(0, k):
                if self.density[self.neighbors[idx][idx_j]] > self.density[p]:
                    p = self.neighbors[idx][idx_j]
            self.parent.append(p) # final parent
            
    def compute_labels(self) -> None:
        """
        Computes the label of each point in the cloud and stores it in the label attribute.
        """
        self.label = []
        for idx in range(len(self.cloud)):
            p = idx
            while self.parent[p] != p:
                p = self.parent[p]
            self.label.append(p)

    def compute_persistence(self, k, tau):
        """
        ToMATo - persistence computation [1]
        Sorts the data points by decreasing estimated density values, 
        then computes the 0-dimensional persistence of the superlevel sets of the density estimator 
        via a union-find on the k-NN graph

        NB
        --
        root of an e (an entry) stands for the vertex in e whose f-estimated values 
        is the highest among the ones of the vertices in e.

        Parameters
        ----------
        k: int
            number of neighbors to consider
        tau: float
            threshold for the persistence

        Returns
        -------
        pers : Set
            set of the persistence values

        References
        ----------
        [1] : 
        https://geometrica.saclay.inria.fr/team/Steve.Oudot/papers/cgos-pbc-09/cgos-pbcrm-11.pdf
        """
        pers = set()
        fusion = [False] * len(self.cloud)
        # sort the points by decreasing order of density
        P = list(range(len(self.cloud)))
        P.sort(key=lambda i: self.density[i], reverse=True)
        # go through the points in decreasing order of density
        for i in range(len(P)):
            p = P[i]  # p : root of the tree of point P[i]
            while p != self.parent[p]:
                p = self.parent[p]
            for j in range(k):  # iteration sur les neighbors de P[i]
                q = self.neighbors[P[i]][j]  # q: root of the tree for the j-th neighbor of P[i]
                while q != self.parent[q]:
                    q = self.parent[q]
                if q != p:  # vertex is not a peak
                    m = (p 
                         if self.density[p] < self.density[q] 
                         else q)
                    M = p + q - m
                    if self.density[m] < self.density[P[i]] + tau:  # do fusion
                        self.parent[m] = M  # update parent
                    elif not fusion[m]:  # cancel fusion 
                        pers.add(self.density[m] - self.density[P[i]])
                        fusion[m] = True
        return pers
    