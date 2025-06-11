import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl


figcounter = 0
def fig_title():
    """Function that returns the numbered title of a figure.
    Parameters:
         ---------
         None

        Returns:
         ---------
         A string of the form "Figure <count>" where count increases each time this function is called"""
    global figcounter
    figcounter += 1
    return f'Figure {figcounter}'


def colours(dataPoints, colourmap='viridis'):
    """Function that returns a valid set of colour values with dataPoints different colours
    Parameters:
         ---------
         dataPoints: number of points which need colours
         colourmap: the colourmap to use (see matplotlib documentation at https://matplotlib.org/stable/users/explain/colors/colormaps.html#)
         The default colormap is viridis, as it is perceptually uniform.

        Returns:
         ---------
         a list of colours which can be iteratively parsed to the color kwarg of pyplot.plot()"""
    r = np.linspace(0, 1, dataPoints + 2)
    color = eval(f'plt.cm.{colourmap}(r)')

    return color


def shapes(dataPoints):
    """Function that returns an array of repeating markers of length dataPoints. The function tiles in the following order:
    . v ^ < > 1 2 3 4 8 s p P *
        Parameters:
             ---------
             dataPoints: number of markers to give

            Returns:
             ---------
             an array of markers"""
    chars = np.array([".", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", 'P', '*'])
    # The final set of characters is determined by tiling the first array however much is needed to have at least dataPoints
    # points, and then slicing the array to achieve the right length.
    return np.tile(chars, int(np.ceil(dataPoints/len(chars))))[:dataPoints]

def lines(dataPoints):
    """Function that returns an array of repeating linestyles of length dataPoints. The function tiles in the following order:
    - -- -. :
            Parameters:
                 ---------
                 dataPoints: number of lines to give

                Returns:
                 ---------
                 an array of linestyles"""

    chars = np.array(["-", "--", "-.", ":"])
    # The final set of characters is determined by tiling the first array however much is needed to have at least dataPoints
    # points, and then slicing the array to achieve the right length.
    return np.tile(chars, int(np.ceil(dataPoints / len(chars))))[:dataPoints]
