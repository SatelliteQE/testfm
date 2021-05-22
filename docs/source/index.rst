TestFM
======

`TestFM`_ is a test suite based on `pytest-ansible`_ that exercises The Foreman maintenance tool

.. contents::

Quickstart
^^^^^^^^^^

The following is only a brief setup guide for TestFM.
The section on Running the Tests provides a more comprehensive guide to using
TestFM.

TestFM requires SSH access to the server system under test, and this SSH access
is implemented by pytest-ansible.

Get the source code and install dependencies::

   git clone https://github.com/SatelliteQE/testfm.git
   pip3 install -r requirements.txt

Before running any tests, you must create a configuration file::

   cp testfm.sample.yaml testfm.local.yaml
   OR
   cp testfm.sample.yaml testfm.local.yaml

There are a few other things you need to do before continuing:

- Make sure ssh-key is copied to the test system.

- Make sure foreman maintain is installed on foreman/satellite server.

Running the Tests
^^^^^^^^^^^^^^^^^

Before running any tests, you must add foreman or satellite hostname to the
`testfm/inventory` file (first copy it from`testfm/inventory.sample`).

That done, you can run tests using pytest ::

    pytest -v --ansible-host-pattern server --ansible-user=root  --ansible-inventory testfm/inventory
    tests/

It is possible to run a specific subset of tests::

    pytest -v --ansible-host-pattern server --ansible-user=root --ansible-inventory testfm/inventory
    tests/test_case.py

    pytest -v --ansible-host-pattern server --ansible-user=root  --ansible-inventory testfm/inventory
    tests/test_case.py::test_case_name

Want to contribute?
^^^^^^^^^^^^^^^^^^^

Thank you for considering contributing to TestFM! If you have any
question or concerns, feel free to reach out to the team.

Recommended
^^^^^^^^^^^

- Import modules in alphabetical order.
- Every method and function will have a properly formatted docstring.


In order to ensure you are able to pass the Travis CI build,
it is recommended that you run the following commands in the base of your
testfm directory ::

    pre-commit autoupdate && pre-commit run -a

Pre-commit will ensure that the changes you made are not in violation of PEP8
standards.

If you have something great, please submit a pull request anyway!

Licensing
^^^^^^^^^

TestFM is licensed under GNU General Public License v3.0.

.. toctree::
   :hidden:

   api/index.rst

.. _TestFM: https://github.com/SatelliteQE/testfm#testfm
.. _pytest-ansible: https://github.com/ansible/pytest-ansible
