__author__ = 'Michele Bannister   git:@mtbannister'

from astroquery import mpc

test_instance = mpc.Mpc()

test_instance._login('mpc_ws', 'mpc!!ws')

print test_instance._args_to_payload("Eris")

print test_instance.query_object('Eris')

# payload['order_by_desc'] = 'order_by_desc'
# payload['spin_period'] = 'spin_period'
# payload['limit 10'] = 'limit 10'
# payload['orbit_type'] = '16'
# payload['limit'] = '10'


return_request = 'name,inclination'
