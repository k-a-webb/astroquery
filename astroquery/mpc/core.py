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

