# 4320_Project
CS4320 Final Project

For our Final Project we propose the development of a system which can effectively track and organize active contributors and their responsibilities.
By optimizing how each issue is addressed and how work is distributed, project productivity can be largely increased. This will be done through a 
combination of Augurs existing CHAOSS spreadsheet and a standalone tracking system.

Our deployment server can be accessed [here](http://ec2-3-142-49-181.us-east-2.compute.amazonaws.com:5000)

# Getting Started - Hello World
Instructions needed get started accessing basic contributor analytics have been taken from [Augur's community reports repository](https://github.com/chaoss/augur-community-reports). They are as follows:


## Setup
### Prerequisites
1. Python 3.x
2. pip
3. virtualenv package `pip3 install virtualenv`
4. Install `geckodriver` for your platform if you want to write annotated PNG files out. This is a great way to automate report generation!
    - osx: `brew install geckodriver`
    - Linux, Windows: Download the latest geckodriver release for your platform from `https://github.com/mozilla/geckodriver/releases` and follow installation instructions. You can also get source code from that link. 

### Setup augur-community-reports
1. Fork the augur-community-reports repository
2. Clone your fork of the repository locally
```
git clone https://github.com/<your-fork>/augur-community-reports
````
3. Create your python virtual environment wherever you routinely store them. We use a `virtualenvs` directory. 
```
virtualenv --python=python3 virtualenvs/augur-community-reports
```
4. Activate your virtual environment
```
source  ../../virtualenvs/augur-community-reports/bin/activate
```
5. Install the necessary Python libraries for Python 3.8 and earlier
```
pip install -r requirements.txt
```
6. Install the necessary Python libraries for Python 3.9 and later
```
pip install -r requirements3.9.txt 
```
7. Change into the directory of your clone
```
cd augur-community-reports
```
8. Run Jupyter Lab
```
jupyter lab
```
## Hello world

Our basic helloworld script can be run through jupyter lab after following the above commands. This notebook simply interacts with Augur's database, extracting contribution information and organizing them based on user and number of commits. The data is then visualized with a bar chart. In later sprints, similar data will
be used to inform our responsibility delegation system.


# Augur's ReadME

branch | status
   --- | ---
master | [![Build Status](https://travis-ci.com/chaoss/augur.svg?branch=master)](https://travis-ci.com/chaoss/augur)
   dev | [![Build Status](https://travis-ci.com/chaoss/augur.svg?branch=dev)](https://travis-ci.com/chaoss/augur)


[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/2788/badge)](https://bestpractices.coreinfrastructure.org/projects/2788)

## What is Augur?

Augur is a software suite for collecting and measuring structured data
about [free](https://www.fsf.org/about/) and [open source](https://opensource.org/docs/osd) software (FOSS) communities.

We gather trace data for a group of repositories, normalize
it into our data model, and provide a variety of metrics about said
data. The structure of our data model enables us to synthesize data
across various platforms to provide meaningful context for meaningful
questions about the way these communities evolve.

We are a [CHAOSS](https://chaoss.community>) project, and many of our
metrics are implementations of the metrics defined by our awesome community. You
can find more information about [how to get involved on the CHAOSS website](https://chaoss.community/participate/).

## Collecting Data

One of Augur's core tenets is a desire to openly gather data that people can trust, and then provide useful and well-defined metrics that help give important context to the larger stories being told by that data. We do this in a variety of ways, one of which is doing all our own data collection in house. We currently collect data from a few main sources:

1. Raw Git commit logs (commits, contributors)
2. GitHub's API (issues, pull requests, contributors, releases, repository metadata)
3. The Linux Foundation's [Core Infrastructure Initiative](https://www.coreinfrastructure.org/) API (repository metadata)
4. [Succinct Code Counter](https://github.com/boyter/scc), a blazingly fast Sloc, Cloc, and Code tool that also performs COCOMO calculations

This data is collected by dedicated data collection workers controlled by Augur, each of which is responsible for some querying some subset of these data sources. We are also hard at work building workers for new data sources. If you have an idea for a new one, [please tell us](https://github.com/chaoss/augur/issues/new?template=feature_request.md) - we'd love your input!


## Getting Started

If you're interested in collecting data with our tool, the Augur team has worked hard to develop a detailed guide to get started with our project which can be found [in our documentation](https://oss-augur.readthedocs.io/en/master/getting-started/toc.html).

If you're looking to contribute to Augur's code, you can find installation instructions, development guides, architecture references (coming soon), best practices and more in our [developer documentation](https://oss-augur.readthedocs.io/en/master/development-guide/toc.html). Please know that while it's still rather sparse right now,
but we are actively adding to it all the time. If you get stuck, please feel free to [ask for help](https://github.com/chaoss/augur/issues/new)!

## Contributing

To contribute to Augur, please follow the guidelines found in our [CONTRIBUTING.md](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md). Augur is a welcoming community that is open to all, regardless if you're working on your 1000th contribution to open source or your 1st. We strongly believe that much of what makes open source so great is the incredible communitites it brings together, so we invite you to join ours!

## License, Copyright, and Funding

Copyright © 2020 University of Nebraska at Omaha, University of Missouri and CHAOSS Project at the Linux Foundation

Augur is free software: you can redistribute it and/or modify it under the terms of the MIT License as published by the Open Source Initiative. See the [LICENSE](LICENSE) file for more details.

This work has been funded through the Alfred P. Sloan Foundation, Mozilla, The Reynolds Journalism Institute, and 9 Google Summer of Code Students.
