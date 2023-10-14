from itertools import combinations
import os

def create_sphere_filtration(dim=1):
    """creates the filtration of the sphere of dimension dim"""
    vertices = list(range(dim+2))
    filtration = []
    filtration.extend(
        [[0, 0, v] for v in vertices])
    ## create the combination in all degrees
    for i in range(1, dim+1):
        filtration.extend([
            [i, i, *s]
            for s in list(combinations(vertices, i+1))
            ])
    save_filtration(filtration, f"TD4/data/{dim}d_sphere.txt")
    return filtration
           
def create_ball_filtration(dim=1):
    vertices = list(range(dim+2))
    filtration = []
    filtration.extend(
        [[0, 0, v] for v in vertices])
    ## create the combination in all degrees
    for i in range(1, dim+2):
        filtration.extend([
            [i, i, *s]
            for s in list(combinations(vertices, i+1))
            ])
    save_filtration(filtration, f"TD4/data/{dim}d_ball.txt")
    return filtration


def save_filtration(filtration, path):
    """save the filtration in a file"""
    with open(path, 'w') as file:
        for simplex in filtration:
            file.write(' '.join(map(str, simplex)) + '\n')
    return True



    
if __name__ == "__main__":
    create_ball_filtration(3)