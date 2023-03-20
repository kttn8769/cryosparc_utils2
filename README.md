# cryosparc_utils2
CryoSPARC utility scripts utilizing cryosparc-tools library

## Installation
1. Create a new virtual environment in Anaconda/Miniconda
```sh
conda create -n cryosparc_utils2 -c conda-forge python=3.10
conda activate cryosparc_utils2
```

2. Clone this repository
```sh
git clone https://github.com/kttn8769/cryosparc_utils2.git
cd cryosparc_utils2
```

3. Install dependencies and cryosparc_utils2
```sh
pip install .
```

## Configuration
* Create a file named ```.cryosparc_conf.json``` under your home directory.
```json
{                                                         
    "license" : "CRYOSPARC LICENSE ID",   
    "host" : "CRYOSPARC MASTER HOSTNAME",                                 
    "base_port" : "CRYOSPARC BASE PORT NUMBER (by default 39000)",                                  
    "email" : "CRYOSPARC ACCOUNT EMAIL ADDRESS",        
    "password" : "CRYOSPARC ACCOUNT PASSWORD"                                
}                                                         
```

## Usage
* Activate the virtual environment
```sh
conda activate cryosparc_utils2
```

* Check usage of each command with --help flag. For example,
```sh
cu2_compare_fsc --help
```

## Examples
### Compare FSC plot of different refinement jobs in a project
```sh
cu2_compare_fsc --project-uid P2 --job-uid-list J64 J66 J70 J72 --outfile fsc-p2-j64-j66-j70-j72.png
```

![fsc-p2-j64-j66-j70-j72](https://user-images.githubusercontent.com/49423083/226233769-d7806c15-e8c3-4626-8829-186c8db2e1c0.png)
