__author__ = 'Michele Bannister   git:@mtbannister'

import unittest

from astroquery import mpc


test_instance = mpc.Mpc()
test_instance._login('mpc_ws', 'mpc!!ws')

# tnos = 'semimajor_axis_min 15'
tnos = 'orbit_type 14'
print(len(test_instance.query_parameters(tnos, return_request='semimajor_axis')))



# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)
#
#
# if __name__ == '__main__':
#     unittest.main()
