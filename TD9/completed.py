"""skeleton.py for TD9 -- INF 556

Fill in the skeleton: look for the TODOs.
"""

import math
from tqdm import tqdm
########## TODO ##########
class Point:
    """
    TODO: complete 

    Point class.

    Attributes
    ----------
    id: int
        id of a point
    filter: float
        filter value of a point
    coords: iterable
        coordinates of a point
    """
    def __init__(self, id, coords, func=None) -> None:
        self.id = id
        self.coords = coords
        self.func = func

    def euclidean_distance(self, point_a):
        distance = 0
        for i in range(len(self.coords)):
            distance += (self.coords[i] - point_a.coords[i]) ** 2
        return math.sqrt(distance)
    
        pass

    def __str__(self) -> str:
        return f"Point {self.id} with coordinates {self.coords} and function value {self.func}"

class Cover:
    def __init__(self, minf=None, maxf=None, resolution=None, gain=None, name=None):
        self.res = 0
        self.intervals = []
        if minf is not None and maxf is not None and resolution is not None and gain is not None:
            # Constructor with minf, maxf, resolution, and gain parameters
            incr = (maxf - minf) / resolution
            x = minf
            alpha = (incr * gain) / (2 * (1 - gain))
            y = min(x + incr + 2 * alpha, maxf)
            while y != maxf:
                inter = (x, y)
                self.intervals.append(inter)
                x = y - 2 * alpha
                y = min(x + incr + 2 * alpha, maxf)
            inter = (x, y)
            self.intervals.append(inter)
            self.res = len(self.intervals)
        elif name is not None:
            # Constructor with name parameter
            input = open(name, "r")
            self.intervals.clear()
            if input:
                for line in input:
                    inter = ()
                    x = float("inf")
                    stream = line.split()
                    x = float(stream[0])
                    inter = (x,)
                    x = float(stream[1])
                    inter += (x,)
                    if x != float("inf"):
                        assert inter[0] <= inter[1]
                        self.intervals.append(inter)
                self.res = len(self.intervals)
            else:
                print(f"  Failed to read file {name}")
    
    def sort_covering(self):
        # Sort the intervals by their first element
        self.intervals.sort(key=lambda x: x[0])

def dfs(graph:dict, point:Point, cc:list, visit:dict):
    cc.append(point)
    visit[point] = True
    neighb = len(graph[point])
    for i in range(neighb):
        if graph[point][i] in visit and not visit[graph[point][i]]:
            return dfs(graph, graph[point][i], cc, visit)
        else :
            return visit

def count_cc(graph:dict, idx=0):
    visit = {}
    for it in graph:
        visit[it] = False
    connected_components = {}
    if graph:
        for it in graph:
            if not visit[it]:
                cc = []
                visit = dfs(graph, it, cc, visit)
                connected_components[idx] = cc
                idx += 1
    return connected_components

def MapperElts(graph, cover):
    pos = iter(graph)
    mapper_elts = []
    id = 0
    for i in range(cover.res):
        inter1 = cover.intervals[i]
        graph_1, graph_2 = {}, {}
        tmp = pos
        if i != cover.res - 1:
            graph_1.clear()
            graph_2.clear()
            inter2 = graph.intervals[i + 1]
            while tmp != graph.end() and tmp.first.func < inter2.first:
                graph_1[tmp.first] = tmp.second
                tmp += 1
            pos = tmp
            while tmp != graph.end() and tmp.first.func < inter1.second:
                graph_1.insert(pair<Point, vector<Point>>(tmp.first, tmp.second))
                graph_2.insert(pair<Point, vector<Point>>(tmp.first, tmp.second))
                tmp += 1
            CC1 = count_cc(graph_1, id)
            mapper_elts.append(CC1)
            # print(i, ": added ", CC1.size(), " proper nodes")
            CC2 = count_cc(graph_2, id)
            mapper_elts.append(CC2)
            # print(i, ": added ", CC2.size(), " intersections")
        else:
            graph_1.clear()
            while tmp != graph.end():
                graph_1.insert(pair<Point, vector<Point>>(tmp.first, tmp.second))
                tmp += 1
            CC1 = count_cc(graph_1, id)
            mapper_elts.append(CC1)
            # print(i, ": added ", CC1.size(), " proper nodes")
    return mapper_elts


########## END TODO ##########


#### HELPERS ####
def read_cloud(filename: str):
    """ builds the cloud (i.e. vector of points) from the file
    
    Parameters
    ----------
    filename : str
        name of the file containing the cloud
    Returns
    -------
    cloud : list
        list of points
    """
    cloud = []
    with open(filename, 'r') as f:
        for idx, line in enumerate(f):
            coordinates = tuple(map(float, line.split())) # convert to floats
            cloud.append(Point(id=idx, coords=coordinates))
    return cloud

def read_function_from_file(filename:str, cloud:list):
    """filter function
    
    Parameters
    ----------
    filename : str
        name of the file containing the filter values
    cloud : list
        point cloud
    """
    with open(filename, 'r') as f:
        content = f.read().split('\n')
    for idx, line in enumerate(content[:-1]): # remove the last \n
        cloud[idx].func = float(line)
    return cloud

def read_coordinates(k:int, cloud:list):
    """read the coordinates of the k-th dimension
    
    Parameters
    ----------
    k : int
        choose the k-th coordinate as the filter value
    cloud : list
        point cloud
    """
    num_pts = len(cloud)
    for i in range(num_pts):
        cloud[i].func = cloud[i].coords[k]
    return cloud


def build_neighborhood_graph(cloud:list, delta:float, name:str):   
    graph, nb, adj, dist = {}, len(cloud), [], []
    for i in range(nb):
        graph[cloud[i]] =  adj
    m = 0
    k = 0
    for i in tqdm(range(nb)):
        dis = []
        for j in range(i + 1, nb):
            d = cloud[i].euclidean_distance(cloud[j])
            dis.append(d)
            if m <= d:
                m = d
        dist.append(dis)
    for i in range(nb):
        for j in range(i + 1, nb):
            if dist[i][j - i - 1] <= delta * m:
                graph[cloud[i]].append(cloud[j])
                graph[cloud[j]].append(cloud[i])
                k += 1
    print(str(100 * k / (nb * (nb - 1) / 2)) + "% of pairs selected.")
    return graph


if __name__ == "__main__":

    path = input("Enter the path to the file: ")
    path = "/Users/julie/Documents/PhD/01-TA/TDA/kelen-inf556/S9_Reeb_Mapper/TD/data/crater.xy"

    ## Use the x-coordinate as the filter value
    # cloud = read_cloud(path)
    # cloud = read_coordinates(k=1, cloud=cloud)

    ## use the density function as the filter value
    path_filter = "/Users/julie/Documents/PhD/01-TA/TDA/kelen-inf556/S9_Reeb_Mapper/TD/data/crater_density.txt"
    cloud = read_cloud(path)
    cloud = read_function_from_file(path_filter, cloud)
    graph = build_neighborhood_graph(cloud, 0.05, "crater")
    connected_components = count_cc(graph)
