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
# Preparing submission

We use the following public submission for ReQuEST@ASPLOS'18 as example: 
https://github.com/dividiti/request-asplos18-mobilenets-armcl-opencl

<!-------------------------------------------------------------------------------------->
## Creating dummy CK repository

For simplicity, we expect that you have your research workflow 
and all related artifacts available at GitHub (or any other similar service). 
Let’s call it *my-workflow*: https://github.com/my-organization/my-workflow .

You need to create a new dummy repository at GitHub (or similar service), 
say “request-asplos18-my-workflow”, and pull it using CK:

```
 $ ck pull repo --url=https://github.com/my-organization/request-asplos18-my-workflow
```
We strongly suggest to create a meaningful name 
related to a given ReQuEST submission such as 
*request-asplos18-mobilenets-armcl-opencl*

CK will create a local copy of this repository in *$HOME/CK* 
and will add a *.ckr.json* file there. This file describes CK repository 
including unique ID and dependencies on other repositories. 
You can see it on Linux as following:
```
 $ cat `ck find repo:request-asplos18-my-workflow`/.ckr.json
```






<!-------------------------------------------------------------------------------------->
# References
 