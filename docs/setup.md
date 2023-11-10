# Setup and Deployment Steps
## Required Env Variables
To run the server, these env variables needs to be set.
<details>
    <summary>.env file sample</summary>
    <figure class="highlight">
    <pre>
    COIN_GECKO="xx-xxxxxxxxxxxxxxxxxxxxxxxx"
    PORT=8080
    GOERLI_INFURA_KEY="https://goerli.infura.io/v3/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    MAINNET_INFURA_KEY="https://mainnet.infura.io/v3/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_1="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_2="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_3="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_4="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_5="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_6="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_7="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_8="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_9="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_10="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_11="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_12="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_13="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_14="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_15="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_16="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_17="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_18="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ARBITRUM_INFURA_KEY_19="https://arb-goerli.g.alchemy.com/v2/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    CHAIN_0X1_ACCOUNT_1="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CHAIN_0X1_ACCOUNT_2="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CHAIN_0X1_ACCOUNT_WOLKS="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CHAIN_0X1_ACCOUNT_MIYUKI="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CHAIN_0X1_ACCOUNT_12="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CHAIN_0X5_ACCOUNT_1="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CHAIN_0X5_ACCOUNT_2="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CHAIN_0X5_ACCOUNT_WOLKS="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CHAIN_0X5_ACCOUNT_MIYUKI="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CHAIN_0X5_ACCOUNT_12="0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    FLASK_DEBUG=True|False
    FLASK_THREADED=True|False
    FLASK_PROECESSES=8
    FLASK_SHOW_TRACEBACK=True|False
    MAX_CPU=80
    MIN_RAM=10
    </pre>
</figure>
</details>

#
For the infura keys, go to [infura.io](https://www.infura.io/) and create a free account. That will let you populate the xxx portion of the x_INFURA_KEY above.

FLASK_THREADED will allow you to set if the server will run in a threaded way, Note that a True value will make FLASK_PROECESSES invalid and thus be ignored. 

FLASK_PROECESSES allows you to set the amount of processes the Flask Server should spawn, it should not exceed the amount of cores your system has. FLASK_THREADED must be False for this to have any effect.

MAX_CPU and MIN_RAM are percentages, and allow the server to delay incoming requests if one of the two conditions are met.

## Running Server locally
To run server locally, you will need to clone the github repository to your computer, then you can either build the code yourself and run the server via CLI, or alternatively you can run the server via Docker.
### Clone code from Github repository
1. You can clone the repository by doing `git clone git@github.com:hyplabs/crocswap_audit_tools.git`
2. Add .env file to root directory

### Run server via Terminal
1. Install the required Python dependencies. You'll need the itsdangerous package and the packages listed in your requirements.txt file:
```
pip3 install itsdangerous==2.0.1
pip3 install -r requirements.txt
```
2. Install Node.js v16.x and npm. Here is how to do this using [NVM](https://github.com/nvm-sh/nvm), but other methods work as well so long as the two are installed. Use these commands to install NVM and select Node 16:
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
nvm use 16
```
3. Install the n package globally using npm and use it to install the stable version of Node.js. Also, install the newman package globally:
```
npm cache clean -f
npm install -g n
n stable
npm install -g newman
```
4. You can now run the service via CLI by entering the service command. You can find examples of the CLI command in `example.sh` file
5. You can also start the server manually in your terminal to make API request to get the analytics or validation results. You can do so by running the following command:
```
python3 run_server.py
```

### Run server via Docker scripts
1. Give permission for shell scripts:
```
chmod +x ./docker/build.sh
chmod +x ./docker/run.sh
chmod +x ./docker/connect.sh
```
2. Run script to build and run docker:
To build the docker container
```
./docker/build.sh
```
3. To run the docker container
```
./docker/run.sh
```
4. To use the Docker CLI
```
./docker/connect.sh
```
5. After connecting to the docker CLI, you can run the server to access the API by doing: `python3 run_server.py`
6. Or you can call the services via CLI, you can find examples cmd in the `example.sh` file

### Docker Issues
1. The first time you run the docker container it may fail, go into docker, stop the container and rerun the command.
2. If you get an issue with docker where on running the container the container is failed to be removed, its because it is most likely runing, power the container down and try again.
3. The container starts with the run_server.py already running, to run it manualy, use `top` to see what process number it has and then run `kill n` where n is the process number of Python3.

## Deployment steps to GCP
The repository has Github Actions that are setup to deploy to GCP when code is pushed into a `staging` or `main` branch. The Github Actions will also push a new image to Docker Hub when new code is pushed into a `main` branch.

Currently there are 4 Github Actions file:
1. `deploy-audit-main.yml`: Deploy the audit server code to the GCP production server and Docker hub when there is a new code in the `main` branch. 
2. `deploy-analytics-main.yml`: Deploy the Analytics server code to the GCP production server and Docker hub when there is a new code in the `main` branch. 
3.  `deploy-audit-staing.yml`: Deploy the audit server code to the GCP staging server when there is a new code in the `staging` branch. 
4. `deploy-analytics-staging.yml`: Deploy the Analytics server code to the GCP staging server when there is a new code in the `staging` branch. 

To customize the Github Actions to deploy to different GCP Server , follow these steps:
1. Add your GCP credentials to GitHub Secrets in the repository. Currently the Github Actions assumed that the credentials is saved under `GCP_SA_KEY`, if you want to use a different key in your secrets, you need to change the Github Actions accordingly.
2. Add Docker credentials to Github Secrets in the repository. They are currently saved under `DOCKER_PASSWORD` and `DOCKER_USERNAME`. If you want to use a different key in your secrets, you need to change the Github Actions accordingly.
3. Configure the GitHub Actions YAML file for GCP Deployment. What needs to be configured:
- Path of the Google artifact repository
- Name of the GCP Cloud run service
- Path of the Docker repository

With all the steps above done, anytime a new commit is pushed to `staging` or `main`, the Github actions will be triggered automatically.

## Deploying Docker hub image to GCP via Terminal
To deploy the server docker hub image to GCP, you can follow these steps:
1. Authenticate gcloud cli. `gcloud auth login`
2. To set the default project run `gcloud config set project PROJECT_ID`. Replace PROJECT_ID with your GCP project id.
3. To deploy docker hub image, run 
```
gcloud run deploy YOUR_SERVICE_NAME \
--image docker.io/chhypotenuse/crocswap-analytics:latest \
--platform managed \
--region us-central1`
```
Replace YOUR_SERVICE_NAME with the name you want to give to your Cloud Run service. If `YOUR_SERVICE_NAME` doesn’t exist yet, it will automatically create a new one.
When asked whether you want to `Allow unauthenticated invocations to [YOUR_SERVICE_NAME] (y/N)`, press Y so the server can accept request from unauthorized users
You can also replace the `--image` name with your docker hub image path

4. After the docker is deployed, set the required environment variables by clicking `Edit & Deploy New Revisions`. The required environment are the one listed at the top of this page.
Non required env variables:
```
FLASK_DEBUG: default true
FLASK_SHOW_TRACEBACK: default true
PORT: default 8080. GCP set this automatically, so no need to set it for GCP, unless you want a custom PORT
```
Then click `Deploy`
5. The docker image should now be deployed to GCP. To get the service URL, go to the service page in the GCP console



