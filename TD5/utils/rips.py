"""Rips class to build a Rips complex from a point cloud"""

import math
from matplotlib import pyplot as plt


class Simplex:
    """Simplex class"""
    def __init__(self, val, dim, vertices) -> None:
        """
        NB : there is no TreeSet in python, instead use dict which presevre the order of insertion
        """
        self.val = val
        self.dim = dim 
        self.vertices = vertices

    def __str__(self) -> str:
        return f"Value : {self.val}, Dim:  {self.dim}, vertices {self.vertices}"

    def __repr__(self):
        return self.__str__()


class Point:
    """
    Point class. From TD2. 
    Attributes
    ----------
    coords : Tuple
        coordinates of a point
    """
    def __init__(self, coords=None) -> None:
        self.coords = coords
    
    def __str__(self) -> str:
        """overload of the string function to pring a point"""
        res = "("
        for coord in self.coords[:-1]:
            res += f"{str(coord)}, "
        return f"{res} {str(self.coords[-1])})"
    
    @staticmethod
    def sqrt_distance(point_a, point_b) -> float:
        """
        Computes the square distance between two points
        
        Parameters
        ----------
        a : Point
            first point
        b : Point
            second point
        
        Returns
        -------
        float
        """
        distance = 0
        for i in range(len(point_a.coords)):
            distance += (point_a.coords[i] - point_b.coords[i]) ** 2
        return math.sqrt(distance)
    

class Rips:
    """Rips class"""
    def __init__(self, path) -> None:
       self.cloud = self.read_data(path)
       self.complex = []

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

    def build_rips(self):
        for i in range(len(self.cloud)):
            self.complex.append(Simplex(0, 0, [i]))
            for j in range(i+1, len(self.cloud)):
                value = Point.sqrt_distance(self.cloud[i], self.cloud[j])
                self.complex.append(Simplex(math.sqrt(value), 1, [i,j]))
                for k in range(j+1, len(self.cloud)):
                    value_3 = max(value, Point.sqrt_distance(self.cloud[i], self.cloud[k]), Point.sqrt_distance(self.cloud[j], self.cloud[k]))
                    self.complex.append(Simplex(math.sqrt(value_3), 2, [i,j,k]))

