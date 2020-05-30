Social Media Analysis
=====================

Getting Started
---------------

Clone the repository

.. code-block:: bash

  git clone https://github.com/WMDA/social-media-analysis.git

You will need to install the python package in the repository. On a windows machine, open the Anaconda Prompt. On a OSX or Linux machine open the Terminal. Run:

.. code-block:: bash

  pip install -e local_path/reddata

Replace `local_path` with the path to your package.

  If you are unsure of the local_path navigate to the folder and run pwd


Environment
-----------
Setup a virtual environment.

.. code-block:: bash

  python3 -m venv venv

This sets up up the virtual environment, creating a venv folder.

To activate the virtual environment run:

.. code-block:: bash

  source venv/bin/activate

  # To deactivate
  deactivate


Once the virtual environment has been set up install the project dependencies listed in `requirements.txt`
using:

.. code-block:: bash

  pip3 install -r requirements.txt


PRAW Authentication
--------------------
To access reddit you will need,

1. Client ID & Client Secret:These two values are needed to access Reddit’s API as a script application.

2. User Agent:	A user agent is a unique identifier that helps Reddit determine the source of network requests.

You may choose to provide these by passing in three keyword arguments when calling the initializer of the Reddit class: client_id, client_secret, user_agent.

.. code-block:: python

  import praw

  reddit = praw.Reddit(client_id="my client id",
                       client_secret="my client secret",
                       user_agent="my user agent")


This method exposes the Authentication keys publicly as they are included in the GitHub code.

Authentication can also be provided in an `praw.ini` configuration file. To run the code in this project you will need to provide this.

  It is recommended to use a `praw.ini` file in order to keep your authentication information separate from your code.

You can obtain this by talking to a member of the team involved in this project.
Alternatively you can provide your own authentication. To provide your own then look at the `reddit documentation <https://github.com/reddit-archive/reddit/wiki/API>`_.

Once you have the `praw.ini` file then you need to place this file either:
* In the current working directory
* In the launching user’s config directory

The second option is the preferred method but either will work. This will vary depending on what system you run, Windows, OSC or Linux. See `PRAW Documentation <https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html>`_ for guidance for your system.

Pipeline
---------
You can run this pipeline by running in a Terminal:

.. code-block:: bash

  python3 pipeline.py

The pipeline takes a number of arguments:


optional arguments:

  -h, --help                                               show this help message and exit
  
  -t, --topics                                              Topics in for praw to search reddit
  
  -c COMMENTS --comments                                   COMMENTS
  
  -config                                                  Selects number of comments for praw to limit to.
                                                           Uses config.yaml file instead of providing options,
                                                           doesn't take any arguments but needs config.yaml file
                                                           (provided with package)

An example search would be:

.. code-block:: bash

  python3 pipeline.py -t cats  -c 5


The pipeline needs either -t and -c or -config. If none is provided an error message will appear.

-config uses a config.yaml file (provided in the package). To edit config file use`vim config.yaml` or open the `config.yaml` in your preferred text editor. If you are unsure about `YAML` then read this `quick guide <https://rollout.io/blog/yaml-tutorial-everything-you-need-get-started/>`_.

When the pipeline is running it should print out the list of topics being searched for in reddit and the number of comments.
