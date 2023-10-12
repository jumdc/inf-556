import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
from copy import deepcopy

class Simplex:
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
    


class SparseComputePersistence:
    def __init__(self, path) -> None:
        self.filtration = SparseComputePersistence.read_file(path)
        self.boundary_matrix = None
        self.number_of_simplices = len(self.filtration)

    @staticmethod
    def read_file(path):
        """reads the file and create the filtration"""
        filtration = []
        with open(path, 'r') as file:
            lines = file.read().split('\n')
        for line in lines:
            if line != '':
                filtration.append(
                    Simplex(
                        val=float(line.split(' ')[0]),
                        dim=int(line.split(' ')[1]),
                        vertices=list(map(int, line.split(' ')[2:]))))
        filtration.sort(key=lambda x: x.val)
        return filtration
    
    def _get_boundary(self, face):
        """
        Returns the boundary of a simplex
        
        NB : 
        the boundary of the k-simplex is the simplex of dimension k-1
        the boundary of a vertex is the empty set
        the boundary of an edge is the set of its vertices
        the boundary of a triangle is the set of its edges ..

        Returns the indices of the simplex in the filtration.
        """
        res = []
        if face.dim > 0:
            dim_chain = face.dim - 1
            chains = [(i, s) for i, s in enumerate(self.filtration) if s.dim == dim_chain]
            for chain in chains:
                if all([True if v in face.vertices else False for v in chain[1].vertices]):
                    res.append(chain[0])
        return res

    def compute_boundary(self):
        """returns the boundary of a simplex"""
        # self.boundary_matrix = np.zeros((len(self.filtration), len(self.filtration)))
        self.boundary_matrix = [[] for _ in range(self.number_of_simplices)]
        for i, face in enumerate(self.filtration):
            # create labels for the rows and columns. 
            boundaries = self._get_boundary(face)
            if len(boundaries) > 0:
                self.boundary_matrix[i].extend([b for b in boundaries]) 
    
    @staticmethod
    def compute_low(reduced, column):
        res = []
        for line in reduced[column]: 
            res.append(line)
        res = (max(res) if len(res) > 0 else 0)
        return res

    def gaussian_elimination(self):
        """computes the reduced echelon form of the boundary matrix"""
        reduced = deepcopy(self.boundary_matrix)
        for column in range(self.number_of_simplices):
            low = self.compute_low(reduced, column) # O(n^2)
            low_j = [
                self.compute_low(reduced, i)  if i != column  else 0
                for i in range(self.number_of_simplices)
            ]
            same_pivot = (low_j.index(low) if low in low_j else False)
            while (same_pivot
                   and same_pivot < column):
                current_column = reduced[column]
                same_pivot_column = reduced[same_pivot]
                for i in range(self.number_of_simplices): # at most we have the number of simplices
                    # if the line is in both columns we remove it
                    if i in same_pivot_column and i in current_column:
                        reduced[column].remove(i)
                    elif i in same_pivot_column and i not in current_column:
                        reduced[column].append(i)
                low = self.compute_low(reduced, column)
                low_j = [
                    self.compute_low(reduced, i) if i != column  else 0
                    for i in range(self.number_of_simplices)]
                same_pivot = (low_j.index(low) if low in low_j else False)
        return reduced
    
    def barcode_output(self, reduced):
        barcode = []
        for column in range(self.number_of_simplices):
            if len(reduced[column]) == 0:
                death = "inf"
                for j in range(self.number_of_simplices):
                    low = self.compute_low(reduced, j)
                    if len(reduced[j]) > 0 and low == column: 
                        death = self.filtration[j].val
                barcode.append(
                    [self.filtration[column].dim, self.filtration[column].val, death])
        return sorted(barcode, key =lambda x : x[0])
    
    # @staticmethod
    # def plot_barcode(barcode, inf_delta=0.1):
    #     plt.rc("text", usetex=True)
    #     plt.rc("font", family="serif")
    #     fig, axes = plt.subplots(1, 1)
    #     fig.suptitle("Barcode of the filtration")
    #     colormap = plt.cm.Set1.colors
    #     min_birth = min(
    #         [interval[1] for interval in barcode]
    #     )
    #     max_death = max(
    #         [interval[2] for interval in barcode if interval[2] != "inf"]
    #     )
    #     infinity = (max_death - min_birth) * inf_delta + max_death
    #     x = [bar[1] for bar in barcode]
    #     y = [(bar[2] - bar[1]) if bar[2] != "inf" else (infinity - bar[1]) for bar in barcode]
    #     c = [colormap[bar[0]] for bar in barcode]

    #     axes.barh(range(len(x)), y, left=x, alpha=0.5, color=c, linewidth=0)
    #     plt.savefig("barcode.png")