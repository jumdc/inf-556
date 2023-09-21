import math

class Point:
    """
    Point class.

    Attributes
    ----------
    coords : Tuple
        coordinates of a point
    """
    def __init__(self, coords=[]) -> None:
        self.coords = coords
    
    def __str__(self) -> str:
        """overload of the string function to pring a point"""
        res = "("
        for coord in self.coords[:-1]:
            res += f"{str(coord)}, "
        return f"{res} {str(self.coords[-1])})"
    
    @staticmethod
    def sqrt_distance(a, b):
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
        d = 0
        for i in range(len(a.coords)):
            d += (a.coords[i] - b.coords[i]) ** 2
        return math.sqrt(d)
    
    # def scanner():
    # implicit implementation in the HillClimbing class