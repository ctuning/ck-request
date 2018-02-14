[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-powered-by-ck.png)](https://github.com/ctuning/ck)
[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-validated-by-the-community-simple.png)](http://cTuning.org)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

<!-------------------------------------------------------------------------------------->
# Introduction

See [ReQuEST website](http://cKnowledge.org/request) 
and [arXiv report](https://arxiv.org/pdf/1801.06378.pdf) 
for more details about our open and reproducible tournaments
on Pareto-efficient co-design of the whole software and hardware
stack for AI, deep learning and other emerging workloads.

<!-------------------------------------------------------------------------------------->
# Validated results from tournaments in the [CK format](https://github.com/ctuning/ck)

* [ASPLOS'18: multi-objective image classification](https://github.com/ctuning/ck-request-asplos18-results)

<!-------------------------------------------------------------------------------------->
# Prerequisites

* Collective Knowledge Framework: see [minimal installation guidelines](https://github.com/ctuning/ck#minimal-installation)

<!-------------------------------------------------------------------------------------->
# Installation

Note that *#* means *sudo* on Linux and can be skipped on Windows.


```
# pip install ck
$ ck pull repo:ck-request
```

<!-------------------------------------------------------------------------------------->
# Preparing submission for evaluation

Since the long-term ReQuEST goal is to develop a common experimental framework
as well as to encourage the community to share artifacts as reusable, 
portable and customizable components, we convert all submissions 
to the open [Collective Knowledge format (CK)](http://cKnowledge.org).

We suggest you to check at least 
a few [getting started guides](https://github.com/ctuning/ck/wiki) 
to understand CK concepts. 
CK helps users add and share unified Python wrappers 
([CK modules](https://github.com/ctuning/ck/wiki/Shared-modules)) 
with a common JSON API and meta information for groups of similar objects. 
Rather than writing their own ad-hoc scripts, researchers can then 
reuse and extend such shared modules or share new objects with the same API.
CK also includes a [cross-platform package manager](https://github.com/ctuning/ck/wiki/Portable-workflows) 
which can detect and set up required tools or install missing ones while allowing
easy co-existence of multiple versions.
Finally, CK allows to assemble portable experimental workflows
from shared components, unify collection of statistics, 
reproduce results and even [crowdsource experiments](http://cKnowledge.org/repo) 
across devices and data sets provided by volunteers.

We will use the following public ReQuEST@ASPLOS'18 submission to explain conversion to the CK format: 
https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl .

<!-------------------------------------------------------------------------------------->
## Creating dummy CK repository

First, we need to create a dummy CK repository which will later 
contain CK wrappers with your artifacts and workflows.

For simplicity, we create a dummy repository at GitHub 
with some user-friendly name of your workflow while prefixing 
it with *ck-request-{name of competition}-{your workflow name}*,
i.e. https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl .

You can see other public CK repositories prepared for ASPLOS'18 tournament here:
https://github.com/ctuning/ck-request-asplos18-results .

We then pull it via CK to create a local copy as following:

```
 $ ck pull repo --url=https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl
```
CK will create a local copy of this repository in *$HOME/CK* 
while adding *.ckr.json* file there. This file describes 
CK repository including unique ID and dependencies on other repositories
(in case you would like to reuse already existing modules and artifacts). 

You can find this file on Linux as following:
```
 $ cat `ck find repo:request-asplos18-my-workflow`/.ckr.json
```

## Reusing existing artifacts

The idea of CK is to help researchers reuse artifacts and build upon them.
Please, check [shared CK repositories](https://github.com/ctuning/ck/wiki/Shared-repos) 
and their [modules](https://github.com/ctuning/ck/wiki/Shared-modules).

To participate in ReQuEST tournaments you will need to add at least
one dependency on a *ck-crowdtuning* repository to be able to reuse
a common program compilation and execution pipeline
with a [cross-platform package manager](https://github.com/ctuning/ck/wiki/Portable-workflows) 
and [customizable crowd-tuner](https://github.com/ctuning/ck/wiki/Compiler-autotuning).

You can add it by editing the *.ckr.json* file:
```
{
 ...

 "dict": {
    ...
    "repo_deps": [
      {"repo_uoa": "ck-crowdtuning"}
    ]
 ...
}

```

## Checking/adding software dependencies

[software descriptions]() and [packages]().


# Questions and comments

Feel free to contact [ReQuEST organizers](http://cKnowledge.org/request), 
send your questions and comments to the [CK mailing list](http://groups.google.com/group/collective-knowledge)
or join our [LinkedIn group on reproducible R&D](https://www.linkedin.com/groups?home=&gid=7433414&trk=my_groups-tile-grp).
