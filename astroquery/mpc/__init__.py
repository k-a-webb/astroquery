__author__ = 'Michele Bannister @mtbannister'

"""
Access to data in the Minor Planet Center.
http://www.minorplanetcenter.net/iau/mpc.html
"""
from astropy.config import ConfigurationItem

MPC_ORBITS_URL = ConfigurationItem('mpc_orbits_url',
                              ['http://minorplanetcenter.net/ws/orbits'],
                              "MPC orbits query URL")
MPC_OBS_URL = ConfigurationItem('mpc_obs_url',
                              ['http://minorplanetcenter.net/ws/observations'],
                              "MPC observations query URL")
MPC_TIMEOUT = ConfigurationItem('timeout', 60, 'time limit for connecting to MPC server')
MPC_RETRIEVAL_TIMEOUT = ConfigurationItem('retrieval_timeout', 120,
                                          'time limit for retrieving a data file once it has been located')



import warnings
warnings.warn("MPC API is in alpha testing, and may alter as the MPC tweak their public-facing interface.")
