<h1> PDSP-Bench Workload Generator </h1>

PDSP-Bench workload generator is designed to generate parallel query plans for varying data stream and query parameters for under various resource configuration. It offers to generate parallel query plans for 14 real-world applications and 9 synthetic applications. We are describing 
This component work can be used with A. [Web app- pdsp-bench_wui:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_wui#readme) or B. command line interface (CLI) for workload generation.
Both scenario offers to collect and generate data which include paralle query execution under varying scenario and corresponding performance metric. These collected data can be further used for performance benchmarking and training of different learned component of DSP [pdsp-bench_ml_models:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_ml_models#readme) for performance prediction. Model training is not part of PDSP-Bench systems. Currently, we are using pre-trained model on benchmarking data for performance prediction and analyzing different learned components of DSP system such learned cost models.


## WUI: Workload Generation
The workload generation with WUI allows simple steps of setting up - [pdsp-bench_controller:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_controller#readme) 
and [pdsp-bench_wui:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_wui#readme) to generate different parallel query plans in different scenarios for both real-world and synthetic applications.

#### Visual representation of Data Generator in PDSP-Bench WUI
After creating resource nodes on CloudLab and starting the PDPS-Bench controller and have the hostnames, you can move ahead to the frontend on the browser and perform the following tasks :

  <img src="../reference_images/PDSP-Bench_WUI_screenshots/PQP_Cluster.PNG" alt="plot" width="600">

  <img src="../reference_images/PDSP-Bench_WUI_screenshots/PQP_Generator.PNG" alt="plot" width="600">


## CLI: Workload Generation

We are already explained how WUI part works in [pdsp-bench_wui:](https://github.com/pdspbench/PDSPBench/tree/master/pdsp-bench_wui#readme). Here we describe workload load generator applications and CLI process to generate data.

- pdspbench-management: The main instructions to setup is in pdspbench-management to generate high amount of workload using CLI. It consists collection of scripts that facilitate the seamless setup of both local and remote clusters. These clusters serve as the foundation for the parallel query plan generator and environment for learned component of DSP for training and test purpose.

- pdspbench-plan-generator: Apache flink client application which functions as an essential tool for generating synthetic and real-world benchmark parallel query plans. These plans are vital for the training and testing of data, a crucial aspect of our learning component of DSP.

- dsp_jobs: Apache flink client application consists of real-worlad benchmark parallel query plans.

- Flink-Observation: Modified the fork of Apache Flink for custom logging of observation of workload characteristics and loggin them in MongoDB database.

### PDSPBench - Parallel Query Plan Cluster Management</h1>

This repository contains several shell scripts to setup:
- physcial resources locally and remotely (a kubernetes cluster) for Parallel Query Plan Generator Flink (PlanGeneratorFlink)and Apache Flink (flink-observation)
- as well as environment for training and inference for our learned cost model.

#### Getting Started with Cluster Manager

1. [Prerequisite](#prerequisite)
1. [Manager](#manager)
1. [First time setup](#firstime)
    - [local cluster environment](#local)
    - [remote cluster environment](#remote)
1. [General steps](#general)
1. [Next steps: Generate data with plan generator](https://github.com/pdspbench/PDSPBench/tree/main/pdspbench-plan-generation)

#### Prerequisite<a name="prerequisite"></a>
All the necessary dependencies will be installed and setup by our scripts so you can easily start with new machine or VM. It is important to know few prerequisite for PDSPBench.
- `Ubuntu 20.04` - we used Ubuntu 20.04 for setting up our local and remote clusters for PlanGeneratorFlink, Flink and training our model.
- `Windows 10 or 11` - we used `Windows Subsystem for Linux (wsl)` for the same purpose. 
- `PlanGeneratorFlink` - we used `java (openjdk 11.0.19 and 11.0.20` for implementing plan generator in Flink.
- `CloudLab` - [CloudLab](https://www.cloudlab.us/) is well known to offer infrastructure of bare metal server to researcher. You can easily create your account for free and access all the available resource. However, PDSPBench is not limited to CloudLab. Researchers can use their onw infrastructure to setup and explore the capabilites of PDSPBench.
- `Docker` - We are using Docker to install and manage dependencies for plan generator flink. You can create your docker register from [hub.docker.com](https://hub.docker.com/).

#### Manager<a name="manager"></a>
`setupPlanGeneratorFlink.sh` - This is the entry script. You can start the script without parameters and you can select a number to start an action like building flink, spin up a local cluster or set up kubernetes remotely. This script delegates the work to its helper scripts which you could also use to do some more specific things. The helper scripts need parameters to work. Try `-h` on a script to know what is supported.

The scripts and their purpose:

- `build.sh` Builds PlanGeneratorFlink and Apache Flink and can be used for start/stop/clean a local cluster.
- `buildDocker.sh` Builds a docker image out of an existing Flink build and uploads it to a registry.
- `distributedUploadAndStart.sh` Installs and set up a remote kubernetes cluster on multiple nodes, upload and run existing builds (PlanGeneratorFlink & Flink) to it, set up mongoDB service on kubernetes and in addition can help with various tasks around managing the cluster (like start a ssh connection, clean mongoDB and the result folder, collect the results, ...)

#### First time setup<a name="manager"></a>
To setup the environment a linux system is recommended. Also Windows Subsystem for Linux (WSL) works quite fine. The system is tested on Ubuntu 20.04

1. Make sure clone `PDSPBench` in your home folder or Create a folder `PDSPBench` in your home folder directory unzip downloaded files
1. Make sure all four folder are there
    - `~/PDSPBench/pdspbench-management` 
    - `~/PDSPBench/pdspbench-plan-generation` 
    - `~/PDSPBench/dsp_jobs` 
    - `~/PDSPBench/flink-observation`
    - `~/PDSPBench/dsp_be`
    - `~/PDSPBench/dsp_fe`

1. Install necessary software (`maven`, `python3`, `nodejs@16.13.2`, `curl`, `uidmap`, `mongodb-clients`, `ansible`, `default-jdk`, `docker`, `docker-compose` and ansibles `kubernetes` plugin). It's important, that docker can be used without root privileges. You can use the following commands to install everything:  
    - `sudo apt update && sudo apt install -y maven curl uidmap python3 python3-pip default-jdk mongodb-clients && pip3 install ansible --user && export PATH=$PATH:~/.local/bin >> ~/.bashrc && source ~/.bashrc && curl -fsSL https://get.docker.com -o get-docker.sh && chmod +x get-docker.sh && sh get-docker.sh && dockerd-rootless-setuptool.sh install && sudo usermod -aG docker $USER && newgrp docker`

    - `sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose`  

    - `ansible-galaxy collection install kubernetes.core && ansible-galaxy collection install ansible.posix`

    - `curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash && source ~/.nvm/nvm.sh && nvm install 16.13.2`

1. Switch into `~/PDSPBench/pdspbench-management` directory and start `setupPlanGeneratorFlink.sh`.
![](../reference_images/PDSP-Bench_WUI_screenshots/Screenshot-setupPlanGeneratorFlink.png "Screenshot of setupPlanGeneratorFlink.sh")
1. Select `3) Build exclusively Flink (from scratch)` by entering `3` and pressing enter to initially build flink on your local machine. This can take 15-30min.

#### First time setup local cluster environment<a name="local"></a>
Be sure that you completed all the necessary steps from the chapter "First time setup".
1. Start `setupPlanGeneratorFlink.sh`. 
![](../reference_images/PDSP-Bench_WUI_screenshots/Screenshot-setupPlanGeneratorFlink.png "Screenshot of setupPlanGeneratorFlink.sh")
1. Select `5) Build Flink and PlanGeneratorFlink, (re)start MongoDB & clean log/db and run local cluster` by entering `5` and pressing enter. That's it, your local cluster is available on `http://localhost:8081`
1. To run PlanGeneratorFlink on the newly created local cluster just go into the root `PDSPBench` folder, create the result directory (`mkdir pgf-logs`) and run the command `./flink-observation/build-target/bin/flink run ./flink-observation/build-target/lib/plangeneratorflink-1.0-SNAPSHOT.jar --mode train --numTopos 3 --logdir ./pgf-logs --environment localCommandLine`. If necessary, adjust the parameters to your needs. You will find the graph-files in the `pgf-logs` directory.
1. Whenever you change something in the source code of PlanGeneratorFlink or flink-observation (here only in the most relevant modules) run option `5` again and your changes are applied and ready to test.

#### First time setup remote kubernetes cluster environment<a name="remote"></a>
Be sure that you completed all the necessary steps from the chapter "First time setup".
1. Register on `hub.docker.com` and create a private repository called `custom-flink` (or your prefered repository name).
1. `~/PDSPBench/pdspbench-management/remote_cluster.key` Contains a private key to connect without passphrase to all instances of the remote cluster. Make sure, that the permissions are correctly set by running `chmod 600 remote_cluster.key` (ssh will not accept keys that are accessible by others). 
    The file content looks like this:
    ```
    -----BEGIN OPENSSH PRIVATE KEY-----
    HaC1b3BlbEcUmlt5nNzOMHaUmC1r[...]
    -----END OPENSSH PRIVATE KEY-----
    ```
1. Create the config file `~/PDSPBench/pdspbench-management/pgf-env`. It contains access infos about the remote nodes, credentials of the used docker hub registry account and some more. It is structured like this:
    ```
    usernameNodes="<Insert your remote node username to access via ssh>"
    privateRegistryRepoName="<Name of your registry repository (e.g. custom-flink)>"
    privateRegistryUsername="<Username of your registry (docker hub)>"
    privateRegistryReadWriteKey="<Access key to read and write to your registry>"
    privateRegistryReadOnlyKey="<Access key to read from your registry (will be uploaded to remote nodes)>"
    githubUsername="<Username of your github account for git clone>"
    githubAccessToken="<access token to your github account for git clone>"
    ```

1. Create a remote environment, e.g. on CloudLab. So far the following profile was used:
    - Profile: small-lan
    - Number of Nodes: 4-8 (min: 3)
    - OS Image: Ubuntu 20.04
1. Start `setupPlanGeneratorFlink.sh` and select `12) Setup Kubernetes Cluster with MongoDB, build & build docker image & upload & run Flink and PlanGeneratorFlink on Kubernetes` by entering `12` and pressing enter.
1. It will ask for the master node. On this node Kubernetes gets installed and managed. Enter the first host of your remote cluster, e.g. on CloudLab something like `amd107.utah.cloudlab.us` and pressing enter. 
1. Next it will ask for all worker nodes. We want to define new ones, so we enter `2` and press enter to enter new worker hostnames.
1. Enter the worker nodes one by one. So insert e.g. `amd109.utah.cloudlab.us` and press enter. Then enter the next one. When you are done, just press enter on an empty input and the installation starts.
1. When the installation finishs you have a kubernetes cluster with a running flink environment. You can use the available options in `setupPlanGeneratorFlink.sh` to connect to the cluster (ssh, kubernetes dashboard, port forward flink web ui, download results).
1. To start the PlanGeneratorFlink job, you can `ssh` into the master node by calling `setupPlanGeneratorFlink.sh` and select `8) Connect to master node` by entering `8` and pressing enter. Open a window manager by calling `screen -R`. Now start PlanGeneratorFlink with the command `~/flink/bin/flink run --target kubernetes-session -Dkubernetes.cluster-id=plangeneratorflink-cluster -Dkubernetes.namespace=plangeneratorflink-namespace -Dkubernetes.rest-service.exposed.type=NodePort ~//flink/lib/plangeneratorflink-1.0-SNAPSHOT.jar --mode train --logdir ~/pgf-results --environment kubernetes --numTopos 3`. Now you can exit the window manager by calling `ctrl+a` and `d`. The application keeps running and you can get back to it by calling `screen -R` again. 

#### General steps to run an experiment<a name="general"></a>
- Acquire Cluster on Cloudlab.
    - small lan profile
    - Ubuntu 20.04
    - specify hardware type (e.g. m510)
- Setup Cluster like described above
- Start PlanGeneratorFlink via `screen`
- Download results with `setupPlanGeneratorFlink.sh` -> `13  Collect PlanGeneratorFlink results to local folder`
- Copy the files from `pdspbench-management/results` to the corresponding location in `pdspbench-experiments` (`evaluation`, `train_random` or `train_rulebased`), see `pdspbench-experiments` readme
- Prepare the experiment data and run the experiment using the learning implementation (see `pdspbench-learning` readme)
