from sklearn.neighbors import KernelDensity
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
from matplotlib.colors import Normalize
from ase.neighborlist import neighbor_list as nl
import matplotlib.pyplot as plt
import matplotlib.cm
from scipy import constants
from ase.io import read
import numpy as np
plt.style.use('/home/nwlundgren/spanners/matsci/miscellaneous/mpltstyle.txt')


line1 = plt.Line2D([],[],color=colorx, lw=8)
line2 = plt.Line2D([],[],color=colory, lw=8)
lines = [line1, line2]
labels = ['X','Y']
ax.legend(lines, labels, loc='upper left', title='Axis')

