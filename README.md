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

We use the following public ReQuEST@ASPLOS'18 submission as example: 
https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl

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

<!-------------------------------------------------------------------------------------->
## Creating dummy CK repository

First, we need to create a dummy CK repository which will later 
contain CK wrappers with your artifacts and workflows.

For simplicity, we create a dummy repository at GitHub 
with some user-friendly name of your workflow while prefixing 
it with *ck-request-{name of competition}-{your workflow name}*,
i.e. https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl

See various CK repositories created for ASPLOS'18 tournament 
[here](https://github.com/ctuning/ck-request-asplos18-results).

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






 