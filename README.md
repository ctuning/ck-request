[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-powered-by-ck.png)](https://github.com/ctuning/ck)
[![logo](https://github.com/ctuning/ck-guide-images/blob/master/logo-validated-by-the-community-simple.png)](http://cTuning.org)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

<!-------------------------------------------------------------------------------------->
# Introduction

See [ReQuEST website](http://cKnowledge.org/request) 
and [arXiv report](https://arxiv.org/pdf/1801.06378.pdf) 
for more details about our open and reproducible tournaments
on Pareto-efficient co-design of the whole software and hardware
stack for AI, deep learning and other emerging workloads
in terms of speed, throughput, accuracy, energy, costs, etc.

<!-------------------------------------------------------------------------------------->
# Validated workflows, artifacts and results from tournaments in the [CK format](https://github.com/ctuning/ck)

* [ASPLOS'18: multi-objective SW/HW optimization and co-design of image classification](https://github.com/ctuning/ck-request-asplos18-results)

<!-------------------------------------------------------------------------------------->
# Preparing submissions for evaluation

The long-term ReQuEST goal is to develop a common platform 
with "plug&play" components for collaborative benchmarking, 
optimization and co-design of emerging workloads. 

That's why we encourage the community to share artifacts (code and data) 
as reusable, portable and customizable components, and help them 
convert their submissions to the open [Collective Knowledge format (CK)](http://cKnowledge.org).

We suggest you to check [CK documentation](https://github.com/ctuning/ck/wiki) for further details.

We will use the following public ReQuEST@ASPLOS'18 submissions to explain conversion to the CK format: 
* https://github.com/ctuning/ck-request-asplos18-caffe-intel
* https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl

These notes are provided especially for next ReQuEST organizers.

<!-------------------------------------------------------------------------------------->

# Prerequisites

* Collective Knowledge Framework: see [minimal installation guidelines](https://github.com/ctuning/ck#minimal-installation)

## Minimal CK installation

The minimal installation requires:

* Python 2.7 or 3.3+ (limitation is mainly due to unitests)
* Git command line client.

### Linux/MacOS

You can install CK in your local user space as follows:

```
$ git clone http://github.com/ctuning/ck
$ export PATH=$PWD/ck/bin:$PATH
$ export PYTHONPATH=$PWD/ck:$PYTHONPATH
```

You can also install CK via PIP with sudo to avoid setting up environment variables yourself:

```
$ sudo pip install ck
```

### Windows

First you need to download and install a few dependencies from the following sites:

* Git: https://git-for-windows.github.io
* Minimal Python: https://www.python.org/downloads/windows

You can then install CK as follows:
```
 $ pip install ck
```

or


```
 $ git clone https://github.com/ctuning/ck.git ck-master
 $ set PATH={CURRENT PATH}\ck-master\bin;%PATH%
 $ set PYTHONPATH={CURRENT PATH}\ck-master;%PYTHONPATH%
```

# CK ReQuEST workflow installation

```
$ ck pull repo:ck-request
```

<!-------------------------------------------------------------------------------------->
## Creating dummy CK repository

First, we need to create a dummy CK repository which will 
contain CK wrappers with a unified API for your artifacts and workflows.

For simplicity, we create a dummy repository at GitHub 
with some user-friendly name of your workflow while prefixing 
it with *ck-request-{name of competition}-{your workflow name}*,
i.e. https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl .

You can see other public CK repositories prepared for ASPLOS'18 tournament 
at https://github.com/ctuning/ck-request-asplos18-results .

We then pull it via CK to create a local copy as follows:

```
 $ ck pull repo --url=https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl
```

CK will create a local copy of this repository in *$HOME/CK* 
while adding *.ckr.json* file there. This file describes 
CK repository including unique ID and dependencies on other repositories
in case you would like to [reuse](https://github.com/ctuning/ck/wiki#user-content-reusable-ck-components) 
already existing artifacts in the CK format.

You can find this file on Linux as follows:
```
 $ cat `ck find repo:request-asplos18-my-workflow`/.ckr.json
```

You can use this [.ckr.json](https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl/blob/master/.ckr.json) as example.

## Reusing existing artifacts

The idea behind CK is to help researchers reuse and extend existing artifacts (code and data).
That's why we suggest you to first check [shared components](https://github.com/ctuning/ck/wiki#user-content-reusable-ck-components) 
([workflows](http://cKnowledge.org/shared-programs.html), 
[modules](http://cKnowledge.org/shared-modules.html), 
[packages](http://cKnowledge.org/shared-packages.html), 
[software detection plugins](http://cKnowledge.org/shared-soft-detection-plugins.html), etc.)
before implementing your own ones.

To participate in the ReQuEST tournaments you usually need to add at least
one dependency on the *ck-autotuning* repository to be able to reuse
a common program compilation and execution pipeline
with a [cross-platform package manager](https://github.com/ctuning/ck/wiki/Portable-workflows) 
and [customizable and multi-objective auto-/crowd-tuner](http://cKnowledge.org/rpi-crowd-tuning).

You can add it by editing the *.ckr.json* file:
```
{
 ...

 "dict": {
    ...
    "repo_deps": [
      {"repo_uoa": "ck-autotuning"}
    ]
 ...
}

```

You then just need to manually install it in the CK. Later it will be automatically pulled with all other sub-dependencies for your CK repository:
```
$ ck pull repo:ck-crowdtuning
```

## Checking software dependencies

Next you need to determine all explicit software dependencies 
such as MXNet, Caffe, TensorFlow, BLAS, LLVM, GCC, CUDA, OpenCL and others
which you need for your experimental workflow (pipeline).

Please, check if CK [already has modules](http://cKnowledge.org/http://cKnowledge.org/shared-soft-detection-plugins.html) 
to detect your software dependencies.
Most of these modules are available in the [ck-env](https://github.com/ctuning/ck-env/tree/master/soft) repository.
Basically, they allow one to automatically detect all installed versions of required software including models and data sets 
on a given machine, prepare their virtual environments in such a way that their multiple versions can co-exist on your system
without interfering, and register all versions in the CK.

For example, you can detect GCC and LLVM on your machine and register them as CK virtual environment as follows:
```
$ ck detect soft:compiler.gcc
$ ck detect soft --tags=compiler,llvm

$ ck show env

$ ck show env --tags=compiler
```

You can then select a given environment or a set of environments and use them similar to Python virtual env via CK:
```
$ ck virtual env:{above UID}
 or
$ ck virtual env:{above UID1},{above UID2},{above UID3}...
```

However, if a CK module for a given software doesn't exist, you need to add one yourself
as briefly described in [this document](https://github.com/ctuning/ck/wiki/Portable-workflows), 
and then share it with the community either via *ck-env* or your own repository.

## Adding cross-platform packages

If a CK module is available for required software, but a given version is not detected on a host platform,
there are two possibilities.

The simplest one is when CK software detection plugin just prints notes about how to obtain and install
a required software, then let user download and install it, and then attempt to detect and register it again.

However, a more convenient way is to provide a related [CK package](http://cKnowledge.org/shared-packages.html) 
which will automatically download, install and even build required software including code, models and data sets
with all sub-dependencies and version ranges for a given platform. Note that CK is customizable enough 
to support a variety of OS including Linux, Android, Windows and MacOS.

This allows us to automate a very complex process of building [Caffe (AI framework)](https://github.com/dividiti/ck-caffe/wiki/Installation) 
or [TensoFlow](https://github.com/ctuning/ck-tensorflow/wiki/Installation) in a unified way with nearly all sub-dependencies 
(OpenBLAS, CLBlast, ArmCL ...), programming models (OpenMP, CUDA, OpenCL ...), targets (CPU, GPU ...)
and OS (Linux, Windows, MacOS, Android ...).

You can check and reuse already [shared packages](http://cKnowledge.org/shared-packages.html)
or add new ones to [*ck-env repository*](https://github.com/ctuning/ck-env/tree/master/package), 
[*ck-math*](https://github.com/ctuning/ck-math/tree/master/package),
[*ck-caffe*](https://github.com/dividiti/ck-caffe/tree/master/package),
[*ck-tensorflow*](https://github.com/ctuning/ck-tensorflow/tree/master/package),
[*ck-mxnet*](https://github.com/ctuning/ck-mxnet/tree/master/package)
or other related repositories.

You can even tell CK to install packages inside CK env entries to make a proper virtual environment for all tools and their versions:
```
$ ck set kernel var.install_to_env=yes
```

Feel free to get in touch with the [the CK community](http://cKnowledge.org/contacts.html) 
if you have questions or suggestions about CK software and packages!

## Detecting platform properties in a unified way

Having unified information about diverse platforms is very
important for collaborative benchmarking, optimization and co-design
of any system.

That is why we developed and shared a number of CK modules with a common API
to automate and unify collection of different platform properties 
needed for portable experimental workflows:

```
$ ck search module:platform*
```

You can detect all properties of your platform as follows:

```
$ ck detect platform
```

You can detect properties of different target platforms 
including Android devices as follows:

```
$ ck ls platform.os | sort
$ ck detect platform --target_os={one of above CK entries}
```

You can also share information about your platform 
to be reused by the community as follows:
```
$ ck detect platform --share
```

You can see already shared information about platforms participated
in our collaborative optimization here:
* [Platforms](http://cknowledge.org/repo/web.php?action=index&module_uoa=wfe&native_action=show&native_module_uoa=platform)
* [OS](http://cknowledge.org/repo/web.php?action=index&module_uoa=wfe&native_action=show&native_module_uoa=platform.os)
* [CPU](http://cknowledge.org/repo/web.php?action=index&module_uoa=wfe&native_action=show&native_module_uoa=platform.cpu)
* [GPU](http://cknowledge.org/repo/web.php?action=index&module_uoa=wfe&native_action=show&native_module_uoa=platform.gpu)
* [GPGPU](http://cknowledge.org/repo/web.php?action=index&module_uoa=wfe&native_action=show&native_module_uoa=platform.gpgpu)
* [NN](http://cknowledge.org/repo/web.php?action=index&module_uoa=wfe&native_action=show&native_module_uoa=platform.nn)
* [NPU](http://cknowledge.org/repo/web.php?action=index&module_uoa=wfe&native_action=show&native_module_uoa=platform.npu)

You can even reuse this info as CK components by connecting the following CK repository:
https://github.com/ctuning/ck-crowdtuning-platforms

Note that when you run CK for the very first time, you may be asked 
to select the most close CK platform description to yours.

CK workflows will then use various platform-specific scripts 
from the selected entry (for example *platform.init:generic-linux* 
such as monitoring or setting up CPU and GPU frequency:

```
$ ls `ck find platform.init:generic-linux`
```

You can later change it as follows:
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
and adding a new *program* entry:

```
$ ck pull repo:ck-autotuning
$ ck add request-asplos18-my-workflow:program:request-asplos18-my-program
```

CK will ask you to select the most close template and will create a working program workflow 
which you can compile (if needed) and run on your platform as follows:
```
$ ck compile program:request-asplos18-my-program --speed
$ ck run program:request-asplos18-my-program
```

You can also find a CK entry with the most similar program shared by the community,
copy it to your repository and then customize its JSON meta and scripts.
For example, you can reuse Caffe-based image classification program as follows:

```
$ ck pull repo --url=https://github.com/dividiti/ck-caffe
$ ck ls ck-caffe:program:
$ ck cp program:caffe-classification request-asplos18-my-workflow:program:request-asplos18-my-program
  or
$ ck cp program:caffe-classification-cuda request-asplos18-my-workflow::request-asplos18-my-program
  or
$ ck cp program:caffe-classification-opencl request-asplos18-my-workflow::request-asplos18-my-program
```

Then you can edit CK JSON meta description of your new program entry 
to specify software dependencies described in the previous section, 
and provide unified scripts to build and run your program depending 
on the target platform (Linux, Windows, MacOS, Android) as briefly described 
in this [wiki](https://github.com/ctuning/ck/wiki/Portable-workflows#implementing-portable-and-customizable-workload-template-example-of-a-universal-workload-characterization)
and this [tech. report](http://cknowledge.org/repo/web.php?wcid=report:rpi3-crowd-tuning-2017-interactive):

```
$ ck edit program:request-asplos18-my-program
or
$ vim `ck find program:request-asplos18-my-program`/.cm/meta.json
```

Since CK uses DevOps and Wikipedia concepts for collaborative R&D, you can just look at 
some [program meta](http://cKnowledge.org/shared-workflows.html) 
from the community and then adapt yours accordingly!

CK also allows you to record various reference outputs using *program.output* module
and then validate correctness of results across different software, compilers, run-time systems 
and platforms.

For example, it is possible to check that there are no distorted images, wrong predications
or that numerical accuracy is within specific thresholds. 

This, in turn, helps the community to crowdsource bug detection across different
environments using CK (crowd-fuzzing) as described in this [tech. report](https://arxiv.org/abs/1801.08024).

It is then possible to run *program* workflow (pipeline of CK modules chained together) 
while collecting different run-time statistics in a unified way as follows:
```
$ ck pipeline program --help
$ ck pipeline program:request-asplos18-my-program
or
$ ck benchmark program:request-asplos18-my-program

```

You can obtain the output characteristics from another CK module or your own Python script as follows:
```
import ck.kernel as ck

r=ck.access({'action':'pipeline',
             'module_uoa':'program',
             'data_uoa':'request-asplos18-my-program',
             'out':'con'})
if r['return']>0: ck.err(r)

print (r)
```          

There are multiple ways to customize your pipeline but the most obvious 
is via environment variables specified via *--env.NAME=VALUE*
as shown in [this use-case](https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl#make-a-sample-run).

## Adding sources of your paper to CK to automate paper generation and sharing with Digital Libraries including ACM and ArXiv.

You can now add a dummy paper which will contain your publication associated with the shared workflow and artifacts as follows:

```
$ ck add request-asplos18-my-workflow:dissemination.publication:
```

Remember unique ID (UID) which will be assigned by the CK to your paper  - you will need to provide it in the next step when preparing artifact description for sharing with ACM DL.

You can then add paper sources and scripts in a similar way as in this paper: 
https://github.com/ctuning/ck-request-asplos18-caffe-intel/tree/master/dissemination.publication/e7cc77d72f13441e

You can also update the self-explanatory meta information for your paper using the same example: 
https://github.com/ctuning/ck-request-asplos18-caffe-intel/blob/master/dissemination.publication/e7cc77d72f13441e/.cm/meta.json

Note that "name" UID is taken from the [Artifact Evaluation repository](https://github.com/ctuning/ck-artifact-evaluation/tree/master/person).
If your name is not there, add it via CK and send a PR, or get in touch with [ReQuEST organizers](mailto:Grigori.Fursin@cTuning.org):

```
$ ck add ck-artifact-evaluation::{my name}
```
 
## Saving results from your workflow

You can run your experiment and save results in a unified and reproducible way as follows:
```
$ ck benchmark program:request-asplos18-my-program  \
       --record \
       --record_uoa={some-experiment-name} \
       --tags=request,request-asplos18,{some other tags}
```

You can see recorded results as follows:
```
$ ck search experiment
 or
$ ck search experiment --tags=request-asplos18
```

You can then replay such experiment as follows:

```
$ ck replay experiment:some-experiment-name
```

Finally, you can  pack all experimental results to share with colleagues as follows:
```
$ ck zip local:experiment:*
```

CK will create a "ckr-local.zip" file with CK entries containing raw experimental results.

You can unzip it to the local (or other) repository on another machine via CK as follows:
```
$ ck unzip repo:local --zip=ckr-local.zip
```

You can then replay a given experiment on another machine as follows:
```
$ ck search experiment:* --tags=request-asplos18
$ ck replay experiment:{above names}
```

You can see more complex experimental workflows here:
* https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl/tree/master/script/mobilenets-armcl-opencl
* https://github.com/dividiti/ck-request-asplos18-mobilenets-armcl-opencl

## Visualizing results on scoreboard for different optimization categories

You can run a local ReQuEST dashboard/scoreboard as follows:
```
$ ck dashboard request.apslos18
```

## Describing your paper/artifact

Now you can describe your artifact to automate ACM and other proceedings.
You need to contact ReQuEST organizers to get information about pre-assigned
DOI for your paper, artifact(s) and information about proceedings.

First, you need to add a description of your artifact which has the same UID as your paper (dissemination.publication):
```
$ ck add artifact:{UID of your paper from above}
```

Then you should edit it using this [artifact as example](https://github.com/ctuning/ck-request-asplos18-caffe-intel/blob/master/artifact/e7cc77d72f13441e/.cm/meta.json)
to provide information about your artifact including ACM badges, license, etc.

## Creating interactive report

CK also has a possibility to create interactive articles such as this [CK report](http://cKnowledge.org/rpi-crowd-tuning), 
however it is not fully automated at the moment and requires many manual steps. However, CK API allow to fully automate this
process too and we plan to do it in the future.

## Automatically preparing ACM proceedings (on Linux, MacOS or Windows)

If you are a ReQuEST proceedings chair, you can now automatically generate ACM proceedings (all necessary PDF, XML, CSV) as follows:

Install minimal dependencies:
```
$ sudo apt-get install python python-pip git
$ sudo pip install ck
``` 

Install Latex with deps

```
$ sudo apt-get install texlive-full
$ sudo apt-get install texlive-generic-extra
$ sudo apt-get install texlive-science
```

Install Python XML support (for ACM DL DTD):
```
$ sudo pip install lxml
```

Temporally set new directory with CK repositories to avoid polluting your own CK installation:

```
$ export CK_REPOS=$PWD/CK_REQUEST_REPOS
```

Pull all ReQuEST repositories with CK workflows, papers and artifacts:

```
$ ck pull repo:ck-request-asplos18-results
$ ck pull repo:ck-request-asplos18-results-caffe-intel
$ ck pull repo:ck-request-asplos18-results-iot-farm
$ ck pull repo:ck-request-asplos18-results-mobilenets-armcl-opencl
$ ck pull repo:ck-request-asplos18-results-mobilenets-tvm-arm
$ ck pull repo:ck-request-asplos18-results-resnet-tvm-fpga

```

Create CK proceedings description using the [following example](https://github.com/ctuning/ck-request/blob/master/proceedings.acm/request.asplos18/.cm/meta.json)
```
$ ck add proceedings.acm:request.apslos18
```

Generate proceedings and ACM meta (paper, CK workflow snapshot, CK results snapshot and zip of the original repository):

```
$ ck generate proceedings.acm:request.asplos18
```

Send all generated info to ACM.

You can later see the proceedings in the ACM DL, such as the ones of the 1st ReQuEST tournament at ASPLOS'18: https://doi.org/10.1145/3229762

# Next steps

After a successful proof-of-concept of our approach during the 1st ReQuEST tournament at ACM ASPLOS'18,
we now work with the community, our advisory board and ACM 
to continue improving CK framework and documentation, adding more tutorials, 
standardizing API and meta descriptions, unifying co-design methodology
and automating [Artifact Evaluation](http://cTuning.org/ae) 
at existing conferences and journals.

# Questions and comments

Feel free to contact [ReQuEST organizers](http://cKnowledge.org/request), 
communicate with the community via [CK mailing list](http://groups.google.com/group/collective-knowledge),
discuss [Artifact Evaluation](http://groups.google.com/group/artifact-evaluation), 
or join our [LinkedIn group on reproducible R&D](https://www.linkedin.com/groups?home=&gid=7433414&trk=my_groups-tile-grp).
