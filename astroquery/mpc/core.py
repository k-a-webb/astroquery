# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import print_function

# put all imports organized as shown below
# 1. standard library imports
import warnings

# 2. third party imports

# 3. local imports - use relative imports
from ..query import QueryWithLogin, suspend_cache # inherits from BaseQuery as required
from ..utils import commons # has common functions required by most modules incl. TimeoutError
from ..utils import prepend_docstr_noreturns # automatically generate docs for similar functions
from ..utils import async_to_sync # all class methods must be callable as static as well as instance methods.
from . import SERVER, TIMEOUT, RETRIEVAL_TIMEOUT # configurable items declared in __init__.py

import requests

__author__ = 'Michele Bannister   git:@mtbannister'

"""
Queries should be POSTed to either minorplanetcenter.net/ws/orbits or minorplanetcenter.net/ws/observations.
The message header should include basic authorization -- username: mpc_ws and password: mpc!!ws
The header should also declare Content-Type: application/xml
The body of the message should contain the parameters, wrapped in xml, e.g.:
    <designation>2008 TC3</designation>

Just to get things started, the designation is the only parameter currently supported, and the only accessible tables
are orbits and observations.
The web service should return the orbit (or observations) for the designated object wrapped in an array in xml.
"""

# export all the public classes and methods
__all__ = ['Mpc']

# declare global variables and constants if any
PAYLOAD = [u'absolute_magnitude', u'albedo', u'albedo_neowise', u'albedo_neowise_unc', u'albedo_unc',
           u'aphelion_distance', u'apparition_end_date', u'apparition_end_magn', u'apparition_start_date',
           u'apparition_start_magn', u'arc_length', u'argument_of_perihelion', u'ascending_node', u'b_minus_v',
           u'b_minus_v_source', u'binary_object', u'color_ignore', u'critical_list_numbered_object', u'delta_v',
           u'designation', u'diameter', u'diameter_neowise', u'diameter_neowise_unc', u'diameter_unc', u'earth_moid',
           u'eccentricity', u'epoch', u'epoch_jd', u'first_observation_date_used', u'first_opposition_used',
           u'g_adopted', u'g_adopted_source', u'g_neowise', u'greatest_elong', u'greatest_elong_date',
           u'greatest_elong_decl', u'greatest_elong_magn', u'h_neowise', u'inclination', u'jupiter_moid', u'km_neo',
           u'last_observation_date_used', u'last_opposition_used', u'lightcurve_notes', u'lightcurve_quality',
           u'mars_moid', u'mean_anomaly', u'mean_daily_motion', u'mercury_moid', u'name', u'neo', u'number',
           u'observations', u'oppositions', u'orbit_type', u'orbit_uncertainty', u'p_vector_x', u'p_vector_y',
           u'p_vector_z', u'panstarrs_v_minus_gprime', u'panstarrs_v_minus_gprime_source', u'panstarrs_v_minus_iprime',
           u'panstarrs_v_minus_iprime_source', u'panstarrs_v_minus_rprime', u'panstarrs_v_minus_rprime_source',
           u'panstarrs_v_minus_uprime', u'panstarrs_v_minus_wprime', u'panstarrs_v_minus_wprime_source',
           u'panstarrs_v_minus_yprime', u'panstarrs_v_minus_yprime_source', u'panstarrs_v_minus_zprime',
           u'panstarrs_v_minus_zprime_source', u'perihelion_date', u'perihelion_date_jd', u'perihelion_distance',
           u'period', u'pha', u'phase_slope', u'q_vector_x', u'q_vector_y', u'q_vector_z', u'rc_minus_ic',
           u'rc_minus_ic_source', u'residual_rms', u'saturn_moid', u'semimajor_axis', u'spin_amplitude_flag',
           u'spin_max_amplitude', u'spin_min_amplitude', u'spin_period', u'spin_period_description',
           u'spin_period_flag', u'taxonomy_class', u'taxonomy_class_source', u'tisserand_jupiter', u'u_minus_b',
           u'u_minus_b_source', u'uranus_moid', u'v_minus_gprime', u'v_minus_gprime_source', u'v_minus_iprime',
           u'v_minus_iprime_source', u'v_minus_rc', u'v_minus_rc_source', u'v_minus_rprime', u'v_minus_rprime_source',
           u'v_minus_uprime', u'v_minus_wprime', u'v_minus_yprime', u'v_minus_zprime', u'v_minus_zprime_source',
           u'venus_moid']

@async_to_sync
class Mpc(QueryWithLogin):
    """
    Connects to the Minor Planet Center public-facing database and allows queries on specific objects.
    """
    # use the Configuration Items imported from __init__.py to set the URL, TIMEOUT, etc.
    SERVER_URL = SERVER.defaultvalue
    TIMEOUT = TIMEOUT.defaultvalue

    def __init__(self):
        super(Mpc, self).__init__()
        self.orbit = None
        self.observations = None

    def _login(self, username, password):
        self.username = username
        self.password = password
        return self.username, self.password

    def _validate_object_id(self, object_id):
        assert isinstance(object_id, str)
        # object_id_type = {'name':None, "number":None, "designation":None}
        if object_id.isalpha():
            retval = "name"
        elif object_id.isalnum() and len(object_id) == 7:
            retval = 'designation'
        elif object_id.isdigit():
            retval = 'number'
        else:
            raise ValueError('%s unknown type: neither name, number nor provisional designation.' % object_id)

        return retval

    def query_object(self, object_id, get_query_payload=False, verbose=False):
        """
        Retrieve orbital elements and observations of the given object from the MPC.
        This implements the same as
        http://mpcdb1.cfa.harvard.edu/ws/search?number=134340&json=1
        for object (134340)

        Parameters
        ----------
        object_name : str
            name of the identifier to query.
        get_query_payload : bool, optional
            This should default to False. When set to `True` the method
            should return the HTTP request parameters as a dict.
        verbose : bool, optional
           This should default to `False`, when set to `True` it displays
           VOTable warnings.

        Returns
        -------
        result : `astropy.table.Table`
            The result of the query as an `astropy.table.Table` object.

        Examples
        --------
        While this section is optional you may put in some examples that
        show how to use the method. The examples are written similar to
        standard doctests in python.
        """

        # typically query_object should have the following steps:
        # 1. call the corresponding query_object_async method, and
        #    get the HTTP response of the query
        # 2. check if 'get_query_payload' is set to True, then
        #    simply return the dict of HTTP request parameters.
        # 3. otherwise call the parse_result method on the
        #    HTTP response returned by query_object_async and
        #    return the result parsed as astropy.Table
        # These steps are filled in below, but may be replaced
        # or modified as required.

        response = self.query_object_async(object_id, get_query_payload=get_query_payload)
        if get_query_payload:
            return response
        result = self._parse_result(response, verbose=verbose)
        return result

    # all query methods usually have a corresponding async method
    # that handles making the actual HTTP request and returns the
    # raw HTTP response, which should be parsed by a separate
    # parse_result method. Since these async counterparts take in
    # the same parameters as the corresponding query methods, but
    # differ only in the return value, they should be decorated with
    # prepend_docstr_noreturns which will automatically generate
    # the common docs. See below for an example.


    @prepend_docstr_noreturns(query_object.__doc__)
    def query_object_async(self, object_name, get_query_payload=False):
        """
        Returns
        -------
        response : `requests.Response`
            The HTTP response returned from the service.
            All async methods should return the raw HTTP response.
        """
        # the async method should typically have the following steps:
        # 1. First construct the dictionary of the HTTP request params.
        # 2. If get_query_payload is `True` then simply return this dict.
        # 3. Else make the actual HTTP request and return the corresponding
        #    HTTP response
        # All HTTP requests are made via the `commons.send_request` method.
        # This uses the Python Requests library internally, and also takes
        # care of error handling.
        # See below for an example:

        # first initialize the dictionary of HTTP request parameters
        request_payload = self._args_to_payload(object_id=object_name)

        if get_query_payload:
            return request_payload
        # commons.send_request takes 4 parameters - the URL to query, the dict of
        # HTTP request parameters we constructed above, the TIMEOUT which we imported
        # from __init__.py and the type of HTTP request - either 'GET' or 'POST'.
        obs_response = commons.send_request(self.SERVER_URL,
                                        request_payload,
                                        self.TIMEOUT,
                                        request_type='POST',
                                        auth = (self.username, self.password))

        return obs_response  # currently a requests.models.Response

    def _args_to_payload(self, object_id=None, constraints=None, return_request=None, json='1'):
        payload = dict()
        # Here the dictionary key should match
        # the exact parameter name as expected by the remote server. The
        # corresponding dict value should also be in the same format as
        # expected by the server.

        print(object_id, constraints, return_request)

        assert (object_id is not None) or (constraints is not None)  # have to have one or the other!

        if object_id:
            oID = object_id.strip()
            object_id_type = self._validate_object_id(oID)
            payload[object_id_type] = oID

        if constraints:
            for n in constraints.split(','):
                base = n.split(' ')[0].strip('_max').strip('_min')
                if not base.isdigit():
                    assert base in PAYLOAD  # make sure the input is valid
                    m = n.split(' ')[1]
                    assert m.isdigit()
                    payload[n.split(' ')[0]] = m

        if return_request:
            payload['return'] = return_request

        payload['json'] = json  # ensures results are in JSON rather than xml

        print(payload)

        assert len(payload.items()) > 1  # make sure it didn't fail somehow and only loaded the json setting

        return payload

    def _parse_result(self, response, verbose=False):
        """
        Parses the results from the HTTP response to `astropy.table.Table`.
        This is currently expecting _args_to_payload() to have set the return type to JSON.

        Parameters
        ----------
        response : `requests.Response`
            The HTTP response object
        verbose : bool, optional
            Defaults to false. When true it will display warnings whenever the JSON
            returned from the MPC doesn't conform to the standard.

        Returns
        -------
        table : `astropy.table.Table`
        """
        retval = None

        if not verbose:
            commons.suppress_vo_warnings()

        print(response.json())

        if len(response.json()) > 0:

            # Fix this so it parses the objects correctly.
            retval = response.json()[0]['properties']
            if len(retval.keys()) > 0:
                return retval
        else:
            warnings.warn("Query returned no results, so the table will be empty")

    def query_parameters(self, constraints, return_request=None, get_query_payload=False, verbose=False):
        """
        Search based on eccentricity, orbital major axis,
        or some other parameter that is likely to be catalogued.



        """
        response = self.query_parameters_async(constraints, return_request=return_request,
                                               get_query_payload=get_query_payload)
        if get_query_payload:
            return response
        result = self._parse_result(response, verbose=verbose)

        return result

    @prepend_docstr_noreturns(query_parameters.__doc__)
    def query_parameters_async(self, constraints, return_request=None, get_query_payload=False):
        """
        Returns
        -------
        response : `requests.Response`
            The HTTP response returned from the service.
            All async methods should return the raw HTTP response.
        """
        # first initialize the dictionary of HTTP request parameters
        request_payload = self._args_to_payload(constraints=constraints, return_request=return_request)

        if get_query_payload:
            return request_payload

        obs_response = commons.send_request(self.SERVER_URL,
                                        request_payload,
                                        self.TIMEOUT,
                                        request_type='POST',
                                        auth = (self.username, self.password))

        return obs_response  # currently a requests.models.Response

    def query_observations(self, name, get_query_payload=False, verbose=False):
        """
        e.g. http://mpcdb1.cfa.harvard.edu/ws/observations?number=134340&json=1
        :param name: Object name (e.g. Eris) or designation (134340 or 2010 VW93)
        :param get_query_payload:
        :param verbose:
        :return:
        """
        raise NotImplementedError

# the default tool for users to interact with is an instance of the Class
mpc_instance = Mpc()

# once your class is done, tests should be written
# See ./tests for examples on this

# Next you should write the docs in astroquery/docs/module_name
# using Sphinx.


