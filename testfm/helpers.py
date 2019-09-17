# helpers required for TestFM
from fabric import Connection
from testfm.constants import SAT_HOSTNAME
import os


def product():
    sat_version = os.popen(
        'ansible -i testfm/inventory satellite --user root -m shell '
        '-a "rpm -q satellite --queryformat=%{VERSION}" -o').read()
    project = sat_version.splitlines()[0].split(' ')[-1]
    if project.startswith('6.6'):
        return ['sat66', '6.6']
    if project.startswith('6.5'):
        return ['sat65', '6.5']
    elif project.startswith('6.4'):
        return ['sat64', '6.4']
    elif project.startswith('6.3'):
        return ['sat63', '6.3']
    elif project.startswith('6.2'):
        return ['sat62', '6.2']
    else:
        return ['sat61', '6.1']


def run(command):
    """ Use this helper to execute shell command on Satellite"""
    return Connection(SAT_HOSTNAME, 'root').run(command)
