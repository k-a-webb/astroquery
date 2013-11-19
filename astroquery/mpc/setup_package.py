import os

def get_package_data():
    paths_test = [os.path.join('data', '*.html')]

    return {
            'astroquery.mpc.tests': paths_test,
    }
