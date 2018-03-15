# Security Anomalies in Logs Data

Tarkin is a project aimed to perform anomaly detection over security logs data.

# Approach

Detecting a particular type of anomaly, and especially those related with security, requires something else apart from
statistics. For this reason, we decided to apply machine learning in order to simulate the intuition of human analysts
faced to this problem.

# Requirements

You need Python 3.6.x or later to run  Tarkin. You can have multiple Python versions (2.x and 3.x) installed on the same system without problems.

In Ubuntu, Mint and Debian you can install Python 3 like this:


    $ sudo apt-get install python3 python3-pip


For other Linux flavors, OS X and Windows, packages are available at

[http://www.python.org/getit/](http://www.python.org/getit/)

To run the project in your python3 environment, you will need to install the dependencies in the requirements.txt file, and
it's highly recommended to create a separate virtual env, see below. Execute the following n a terminal window:


    $ cd security-anomales-logs-data
    $ pip install -r requirements.txt


Then, you will need to run the following command:

    $ python -m spacy download en


## Working with virtualenv

If you are using virtualenv, make sure you are running a python3 environment. Installing via pip3 in a v2 environment
will not configure the environment to run installed modules from the command line.


    $ python3 -m pip install -U virtualenv
    $ python3 -m virtualenv env


# Quick start

There are several shell scripts available from the top level directory of the project:

* build.sh: Initializes the environment creating the necessary folders and building the docker images.

The project can be run in your own machine and python installation. You will first need to run the training script, then
you can execute check.sh or check-demo.sh to analyze files configured in the same script or quoted sentences
passed as command line parameters, respectively.

* train.sh: Starts the training of the letter frequency model, producing a letterspace.pkl binary file.
* check.sh: Evaluates the infrequency and applies sentiment analysis to the logs of the file configured in the script.     
* check-demo.sh: Useful for demo purposes; evaluates the infrequency and applies sentiment analysis to a quoted sentence
received as a script parameter. NOTICE: unlike check.sh, this script returns an evaluation result even if the sentiment
score value is above 0.   

You can also run the dockerized version of the project, which is launched using the following equivalent shell scripts:

* train-docker.sh
* check-docker.sh
* check-demo-docker.sh

# Notebooks

The project includes a notebook to illustrate how the fear indicator is calculated. Before being able to run it, 
you'll need to execute the following commands from your virtual env:

    $ python3 -m pip install jupyter seaborn matplotlib
    $ jupyter notebook

Then navigate on your browser to security-anomalies-logs-data/notebooks from the Jupyter Home tree 
and open the file <code>Log Mining.ipynb</code>. 

In case you experience an error running the notebook cells, make sure you executed the <code>./build.sh</code> script 
that sets up the project by building the docker images and downloading the default lexicon dictionary, which is used 
by the notebook, or do it again if unsure. 

# Contributing

Feedback, ideas and contributions are welcome. For more details, please see the CONTRIBUTING.md file.

# License

This project is distributed under the [Apache License](http://www.apache.org/licenses/LICENSE-2.0)
