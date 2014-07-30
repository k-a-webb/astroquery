# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
MPC
Access to data in the Minor Planet Center.
http://www.minorplanetcenter.net/iau/mpc.html
-------------------------

:author: Michele Bannister (micheleb@uvic.ca)
"""
import warnings
warnings.warn("MPC API is in alpha testing, and may alter as the MPC tweak their public-facing interface.")

from astropy.config import ConfigurationItem

# Make the URL of the server, timeout and other items configurable
# See <http://docs.astropy.org/en/latest/config/index.html#developer-usage>
# for docs and examples on how to do this
SERVER = ConfigurationItem('mpc_server',
                              ['http://mpcdb1.cfa.harvard.edu/ws/search'],
                              "MPC orbits, physical properties and observations query URL")

# Set the timeout for connecting to the server in seconds
TIMEOUT = ConfigurationItem('timeout', int(60), 'default timeout for connecting to MPC server')
RETRIEVAL_TIMEOUT = ConfigurationItem('retrieval_timeout', int(120),
                                          'time limit for retrieving a data file once it has been located')

# Now import your public class
# Should probably have the same name as your module

from .core import Mpc

__all__ = ['Mpc']
