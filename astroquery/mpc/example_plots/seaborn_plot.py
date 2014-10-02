__author__ = 'Michele Bannister   git:@mtbannister'

"""
    An interactive plot of the orbital elements of trans-Neptunian objects as supplied by the Minor Planet Center.
            Comparison of the effectiveness of producing this in different plotting packages.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from astroquery import mpc


mpccenter = mpc.Mpc()
mpccenter._login('mpc_ws', 'mpc!!ws')
tnos = mpccenter.query_parameters('semimajor_axis_min 15',
                                  return_request='semimajor_axis, inclination, eccentricity, name, designation')

print(len(tnos))

tnos_df = pd.DataFrame(tnos)
    # np.c_[[n['semimajor_axis'] for n in tnos], [n['inclination'] for n in tnos],
    #                          [n['eccentricity'] for n in tnos], [n['name'] for n in tnos],
    #                          [n['designation'] for n in tnos]],
    #                    columns=["semimajor_axis", "inclination", "eccentricity", "name", "designation"])

print tnos_df

with sns.axes_style("white"):
    sns.jointplot("semimajor_axis", "eccentricity", tnos_df, kind="kde")

# g = sns.FacetGrid(tnos_df, col="semimajor_axis")

# fig, (ax1, ax2) = plt.subplots(2, 1)
# sns.set(style="darkgrid")

# sns.factorplot("semimajor_axis", "eccentricity", data=tnos_df)


