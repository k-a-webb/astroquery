__author__ = 'Michele Bannister   git:@mtbannister'

from astroquery import mpc

test_instance = mpc.Mpc()

print test_instance.query_object('Eris', verbose=True)

