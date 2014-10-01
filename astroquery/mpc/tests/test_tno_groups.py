__author__ = 'Michele Bannister   git:@mtbannister'

import unittest

from astroquery import mpc


test_instance = mpc.Mpc()
test_instance._login('mpc_ws', 'mpc!!ws')

# Test orbit type cycling
orbit_types = range(0, 11)
orbit_types += [14, 15, 16]

for orbtype in orbit_types[12:13]:
    print(len(test_instance.query_parameters('orbit_type '+ str(orbtype), return_request='inclination')))

# Test specific condition setting: all TNOs
print(len(test_instance.query_parameters('semimajor_axis_min 15', return_request='semimajor_axis, inclination, eccentricity')))

# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)
#
#
# if __name__ == '__main__':
#     unittest.main()
