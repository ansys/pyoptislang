.. _ref_contributing:

==========
Contribute
==========
We absolutely welcome any code contributions and we hope that this
guide will facilitate an understanding of the PyOptiSLang code
repository. It is important to note that while the PyOptiSLang software
package is maintained by ANSYS and any submissions will be reviewed
thoroughly before merging, we still seek to foster a community that can
support user questions and develop new features to make this software
a useful tool for all users.  As such, we welcome and encourage any
questions or submissions to this repository.

For contributing to this project, please refer to the [PyAnsys Developer's Guide](https://dev.docs.pyansys.com/).
Further information about contributing to PyOptiSLang can be found in [Contributing](https://optislang.docs.pyansys.com/version/stable/contributing/index.html).

The following contribution information is specific to PyOptiSLang.

Clone the repository and install the package
--------------------------------------------
To clone the PyOptiSLang repository and install the latest PyOptiSLang
release in development mode, run this code:

.. code::

    git clone https://github.com/pyansys/pyoptislang
    cd pyoptislang
    pip install pip -U
    pip install -e .


Post issues
-----------
Use the `PyOptiSLang Issues <https://github.com/pyansys/pyoptislang/issues>`_
page to submit questions, report bugs, and request new features. When possible,
use these issue templates:

* Bug report template
* Feature request template

If your issue does not fit into one of these template categories, create your
own issue.

To reach the project support team, email `pyansys.core@ansys.com <pyansys.core@ansys.com>`_.

View documentation
-------------------
Documentation for the latest stable release of PyOptiSLang is hosted at
`PyOptiSLang Documentation <https://optislang.docs.pyansys.com>`_.

In the upper right corner of the documentation's title bar, there is an option
for switching from viewing the documentation for the latest stable release
to viewing the documentation for the development version or previously
released versions.

Adhere to code style
--------------------
PyOptiSLang follows the PEP8 standard as outlined in the `PyAnsys Development Guide
<https://dev.docs.pyansys.com>`_ and implements style checking using
`pre-commit <https://pre-commit.com/>`_.

To ensure your code meets minimum code styling standards, run this code::

  pip install pre-commit
  pre-commit run --all-files


You can also install this as a pre-commit hook by running this code::

  pre-commit install

This way, it's not possible for you to push code that fails the style checks::

  $ pre-commit install
  $ git commit -am "added my cool feature"
  black....................................................................Passed
  isort....................................................................Passed
  flake8...................................................................Passed
  codespell................................................................Passed
