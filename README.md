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

The idea of CK is to help researchers reuse and extend artifacts.
Please, check first [shared CK repositories](https://github.com/ctuning/ck/wiki/Shared-repos) 
and their [modules](https://github.com/ctuning/ck/wiki/Shared-modules) 
to build upon existing artifacts.

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

You then need to manually pull it once via CK (later it will be pulled automatically with all other sub-dependencies):
```
$ ck pull repo:ck-crowdtuning
```

## Checking software dependencies

Next you need to determine all explicit software dependencies 
such as MXNet, Caffe, TensorFlow, BLAS, LLVM, GCC, CUDA, OpenCL and others
which you need for your experimental workflow (pipeline).

Please, check if CK [already has modules to detect all your software dependencies](https://github.com/ctuning/ck/wiki/Shared-soft-descriptions).
Most of these modules are available in the [ck-env](https://github.com/ctuning/ck-env/tree/master/soft) repository.
Basically, they allow one to automatically detect all installed versions of required software on a given machine,
prepare their environments in such a way that they can co-exist, and register all versions in the CK.

For example, you can detect GCC and LLVM on your machine as following:
```
$ ck detect soft:compiler.gcc
$ ck detect soft --tags=compiler,llvm

$ ck show env

$ ck show env --tags=compiler
```

However, if a CK module for a given software doesn't exist, you need to add one yourself
as briefly described in [this wiki page](https://github.com/ctuning/ck/wiki/Portable-workflows) 
and then share it with the community via *ck-env* or your own repository.

## Adding cross-platform packages

If a CK module is available for required software, but a given version is not detected on a host platform,
there are two possibilities.

The simplest one is when CK module just prints notes about how to obtain and install
a required software, and then re-run its detection via CK.

However, a more convenient way is to provide a related CK package which will automatically
download, install and even build required software, models, data sets
with all sub-dependencies and version ranges 
for a given platform (CK currently supports Linux, Android, Windows and MacOS).

For example, it is possible to build [Caffe](https://github.com/dividiti/ck-caffe/wiki/Installation) 
or [TensoFlow](https://github.com/ctuning/ck-tensorflow/wiki/Installation) 
in a unified way via CK with various sub-dependencies 
(OpenBLAS, CLBlast, ArmCL ...), programming models (OpenMP, CUDA, OpenCL ...), targets (CPU, GPU ...)
and OS (Linux, Windows, MacOS, Android ...).

You can check and reuse already [shared packages](https://github.com/ctuning/ck/wiki/Shared-packages)
or add similar ones to [*ck-env*](https://github.com/ctuning/ck-env/tree/master/package), 
[*ck-math*](https://github.com/ctuning/ck-math/tree/master/package),
[*ck-caffe*](https://github.com/dividiti/ck-caffe),
[*ck-tensorflow*](https://github.com/ctuning/ck-tensorflow),
[*ck-mxnet*](https://github.com/ctuning/ck-mxnet)
or other related repositories.

Feel free to ask [the CK community](http://groups.google.com/group/collective-knowledge) 
for help or further details about CK software and packages!

## Detecting platform properties in a unified way

We shared various modules in the CK to automate 
and unify detection of various platform properties 
needed for portable experimental workflows:

```
$ ck search module:platform*
```

You can detect all properties of your platform as following:

```
$ ck detect platform
```

You can detect properties of different target platforms 
including Android devices as following:
```
$ ck ls platform.os | sort
$ ck detect platform --target_os={one of above CK entries}
```

You can also share information about your platform 
to be reused by the community as following:
```
$ ck detect platform --share
```

You can see already shared platform descriptions 
participated in collaborative CK experiments [here](https://cKnowledge.org/repo).

When you run CK for the very first time, you may be asked 
to select to most close CK platform description 
shared by CK users. 

CK workflows will then use various platform-specific scripts 
from the selected entry (for example *platform.init:generic-linux* 
such as monitoring or setting up CPU and GPU frequency:
```
$ ls `ck find platform.init:generic-linux`
```

You can later change it as following:
```
$ ck ls platform.init | sort
$ ck detect platform.os --update_platform_init \
  --platform_init_uoa={one of above CK entries}
```

You can find more details in this [wiki](https://github.com/ctuning/ck/wiki/Farms-of-CK-machines).

## Adding portable experimental workflow to build and run project

It is now possible to assemble basic experimental workflow to build and run 
a given ReQuEST application on any supported platform with any dependencies.

We already provided a CK workflow template to build, run and even autotune any application.
You can reuse it by pulling [ck-autotuning](https://github.com/ctuning/ck-autotuning) repository
and adding new *program* entry:

```
$ ck pull repo:ck-autotuning
$ ck add request-asplos18-my-workflow:program:request-asplos18-my-program
```

or you can find CK entry with the most close program shared by the community,
copy it to your repository and then customize its JSON meta and scripts.
For example, you can reuse Caffe-based image classification program as following:

```
$ ck pull repo --url=https://github.com/dividiti/ck-caffe
$ ck ls ck-caffe:program:
$ ck cp caffe-classification request-asplos18-my-workflow:program:request-asplos18-my-program
  or
$ ck cp caffe-classification-cuda request-asplos18-my-workflow:program:request-asplos18-my-program
  or
$ ck cp caffe-classification-opencl request-asplos18-my-workflow:program:request-asplos18-my-program
  or
$ ck cp  request-asplos18-my-workflow:program:request-asplos18-my-program
```

Then you can edit JSON meta of your new program entry to describe software dependencies
from the previous section and provide unified scripts to build and run 
your program depending on the target platform (Linux, Windows, MacOS, Android)
as briefly described in this [wiki](https://github.com/ctuning/ck/wiki/Portable-workflows#implementing-portable-and-customizable-workload-template-example-of-a-universal-workload-characterization)
and [tech. report](http://cknowledge.org/repo/web.php?wcid=report:rpi3-crowd-tuning-2017-interactive):

```
$ ck edit program:request-asplos18-my-program
or
$ vim `ck find program:request-asplos18-my-program`/.cm/meta.json
```

Since CK uses DevOps and Wikipedia concepts for R&D, you can see 
a [similar meta](https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl/blob/master/program/mobilenets-armcl-opencl/.cm/meta.json) 
from the community and then adapt yours accordingly!

CK also allows you to record various reference outputs using *program.output* module
and then validate correctness of results across different software, compilers, run-time systems 
and platforms.

For example, it is possible to check that there are no distorted images, wrong predications
or that numerical accuracy is within specific thresholds. 

This, in turn, helps the community to crowdsource bug detection across different
environments using CK (crowd-fuzzing) as described in this [tech. report](https://arxiv.org/abs/1801.08024).

It is then possible to run *program* pipeline while collecting various statistics 
in a unified way as following:
```
$ ck pipeline program --help
$ ck pipeline program:request-asplos18-my-program
or
$ ck benchmark program:request-asplos18-my-program

```

You can obtain output characteristics from another CK module or your own Python script as following:
```
import ck.kernel as ck

r=ck.access({'action':'pipeline',
             'module_uoa':'program',
             'data_uoa':'request-asplos18-my-program',
             'out':'con'})
if r['return']>0: ck.err(r)

print (r)
```          

There are various ways to customize your pipeline but the most obvious 
is via environment variables specified via *--env.NAME=VALUE*
as shown in [this use-case](https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl#make-a-sample-run).

## Preparing ReQuEST workflow to expose characteristics specific to a given tournament



## Validating results by external reviewers



## Recording validated results to ck-request-validated-results


## Visualizing results on scoreboard for different optimization categories


## Archiving stable version in a permanent repository with ACM badges



# Questions and comments

Feel free to contact [ReQuEST organizers](http://cKnowledge.org/request), 
send your questions and comments to the [CK mailing list](http://groups.google.com/group/collective-knowledge)
or join our [LinkedIn group on reproducible R&D](https://www.linkedin.com/groups?home=&gid=7433414&trk=my_groups-tile-grp).
