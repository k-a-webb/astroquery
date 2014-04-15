__author__ = 'Michele Bannister   git:@mtbannister'

from astroquery import mpc

test_instance = mpc.Mpc()

test_instance._login('mpc_ws', 'mpc!!ws')

print test_instance.query_object('Eris', verbose=True)

