import numpy as np


def read_file(path):
    """read the files and return the cloud of points"""
    with open(path, "r") as file: 
        lines = file.readlines()
        print(len(lines))
        lines = [line.strip().split("   ") for line in lines] # att : 3 spaces between the values
        lines = [[float(x) for x in line] for line in lines]
    return lines

def compute_mds(cloud, norm=False):
    """
    Compute the MDS 

    Parameters
    ----------
    cloud : list
        The cloud of points
    norm : bool, optional
        Normalize the cloud of points, by default False
    
    Returns
    -------
    dict
        The dictionnary containing the points, the variables and the spectrum
    """
    m = np.array(cloud)
    m = (m - m.mean(axis=0)) / (m.std(axis=0) if norm else 1) # center (and normalize) data
    # compute Gram matrix
    gram = np.dot(m, m.T)
    # diagonalize Gram matrix
    eig_val, eig_vec = np.linalg.eig(gram)

    # retrieve eigenvectors and eigenvalues
    indices = np.arange(0,len(eig_val), 1) # the eigen values are not sorted
    indices = ([x for _,x in sorted(zip(eig_val, indices))])[::-1] # sort the eigen values and get the indices
    eig_val = eig_val[indices]
    # eigenvectors[:,i] is the eigenvector corresponding to the eigenvalue eigenvalues[i].
    eig_vec = eig_vec[:,indices] 

    # compute new coordinates
    new_coordinates  = np.sqrt(eig_val)
    reduced = eig_vec * new_coordinates

    # output 
    dim_reduction = {"points": reduced, 
                     "variables": eig_vec, 
                     "spectrum": eig_val}
    return dim_reduction
