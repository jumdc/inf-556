"""Utils to plot the barcode of a filtration"""

from matplotlib import pyplot as plt

@staticmethod
def plot_barcode(barcode, inf_delta=0.1):
    """Plot the barcode."""
    plt.rc("text", usetex=True)
    plt.rc("font", family="serif")
    fig, axes = plt.subplots(1, 1)
    fig.suptitle("Barcode of the filtration")
    colormap = plt.cm.Set1.colors
    min_birth = min(
        [interval[1] for interval in barcode]
    )
    max_death = max(
        [interval[2] for interval in barcode if interval[2] != "inf"]
    )
    infinity = (max_death - min_birth) * inf_delta + max_death
    x = [bar[1] for bar in barcode]
    y = [(bar[2] - bar[1]) if bar[2] != "inf" else (infinity - bar[1]) for bar in barcode]
    c = [colormap[bar[0]] for bar in barcode]

    axes.barh(range(len(x)), y, left=x, alpha=0.5, color=c, linewidth=0)
    plt.savefig("barcode.png")
    plt.close()