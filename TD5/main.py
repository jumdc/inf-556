import os
import pyrootutils
import matplotlib.pyplot as plt
import numpy as np

root = pyrootutils.setup_root(
    search_from=__file__,
    indicator=[".git", "pyproject.toml"],
    pythonpath=True,
    dotenv=True,
)

from TD5.utils.mds import compute_mds, read_file

def apply_mds_ind_files(path):
    for idx, file in enumerate(sorted(os.listdir(path))):
        print(f"Processing {idx}-th file {file}")
        point_cloud = read_file(os.path.join(path, file))
        dim_reduction = compute_mds(point_cloud)["points"]
        np.savetxt(f"TD5/data/3d_files/3d_{file}", dim_reduction[:,:3])
        fig = plt.figure()
        # syntax for 3-D projection
        ax = plt.axes(projection ='3d')
        # plotting
        ax.scatter(dim_reduction[:,0], dim_reduction[:,1], 
                  dim_reduction[:,2], c='#f94144')
        ax.set_title(f'3d plot of file {file.split(".")[0]}')
        ax.set_xlabel('V1')
        ax.grid(False)
        ax.set_ylabel('V2')
        ax.set_zlabel('V3')
        ax.view_init(elev=20, azim=-90, roll=0)
        plt.savefig("TD5/data/3d_plots/" + file + ".png")
        plt.close()

def apply_mds_full(path):
    point_cloud_full = []
    ids = []
    labels = []
    print(len(os.listdir(path)))
    for idx, file in enumerate(os.listdir(path)):
        print(f"Processing {idx}-th file {file}")
        point_cloud = read_file(os.path.join(path, file))
        point_cloud_full.extend(point_cloud)
        ids.extend([idx+1]*len(point_cloud))
        labels.append(file.split(".")[0])
    print(len(point_cloud_full))
    dim_reduction = compute_mds(point_cloud_full)["points"]
    np.savetxt("TD5/data/3d_files/3d_full", dim_reduction[:,:3])
    fig = plt.figure(figsize=(10,10))
    # syntax for 3-D projection
    ax = plt.axes(projection ='3d')

    s = ax.scatter(dim_reduction[:,0], dim_reduction[:,1], 
              dim_reduction[:,2],c=ids, s=4)
    ax.set_title(f'3d plot of all clouds')
    ax.set_xlabel('V1')
    ax.grid(False)
    ax.set_ylabel('V2')
    ax.set_zlabel('V3')
    ax.view_init(elev=20, azim=-90, roll=0)
    plt.savefig("TD5/data/3d_plots/full.png")
    plt.close()


if __name__ == "__main__":
    # apply_mds_ind_files("TD5/data/clouds")
    apply_mds_full("TD5/data/clouds")
