"""Implementation of the Point class."""

import math

class Point:
    """
    Point class.

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
    def sqrt_distance(point_a, point_b):
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
    
    # def scanner():
    # implicit implementation in the HillClimbing class
