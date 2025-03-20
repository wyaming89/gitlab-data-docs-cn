

# dbt Guide

data build tool (dbt) Guide

## Quick Links

  * [Primary Project](https://gitlab.com/gitlab-data/analytics/)
  * [dbt docs](https://dbt.gitlabdata.com/)



## What and why

dbt, short for [data build tool](https://www.getdbt.com/), is an [open source project](https://github.com/dbt-labs/dbt-core) for managing data transformations in a data warehouse. Once data is loaded into a warehouse, dbt enables teams to manage all data transformations required for driving analytics. It also comes with built in testing and documentation so we can have a high level of confidence in the tables we’re generating and analyzing.

The following links will give you an excellent overview of what dbt is:

  * [What, exactly, is dbt?](https://www.getdbt.com/blog/what-exactly-is-dbt) \- This is a less technical overview for understanding the tool
  * [What is dbt?](https://docs.getdbt.com/docs/introduction) \- This is a bit more technical and comes straight from the docs



But why do we use dbt? There are several reasons.

First is that it is an open source tool with a vibrant community. Choosing an open source tool enables us to collaborate with the larger data community and solve problems faster than had we gone with a proprietary solution.

Second, it was built with version control in mind. For GitLab, this is essential since we use the product for building and running the company.

Third, it speaks the language of analysts - SQL. This increases the number of people that can contribute since SQL is becoming such a critical part of many people’s jobs.

Finally, it enables teams to move faster by integrating [testing and documentation](https://docs.getdbt.com/docs/build/sql-models#testing-and-documenting-models) from the start.

For even more information about the basics of dbt, see our [data analyst onboarding issue template](https://gitlab.com/gitlab-data/analytics/blob/master/.gitlab/issue_templates/Team%3A%20Data%20Onboarding.md)

At times, we rely on dbt packages for some data transformation. [Package management](https://docs.getdbt.com/docs/build/packages) is built-in to dbt. A full list of packages available are on the [dbt Hub site](https://hub.getdbt.com).

## Running dbt

If you’re interested in using dbt, the [dbt documentation has a great tutorial](https://docs.getdbt.com/docs/get-started-dbt) on getting setup to work on data from a fictional business called Jaffle Shop.

If you wish to use dbt and contribute to the data team project, you’ll need to gain access to our Snowflake instance, which can be done via an [access request](https://handbook.gitlab.com/handbook/it/end-user-services/onboarding-access-requests/access-requests/).

### Local environment

We use user-dedicated development databases and [virtual environments](https://handbook.gitlab.com/handbook/enterprise-data/platform/dbt-guide/#venv-workflow) via [make](https://www.gnu.org/software/make/manual/make.html) recipes in order to facilitate a ’local’ development environment for GitLab team members contributing to our dbt project(s)

#### ‘Local’ User-Dedicated Development Databases

When needed for team members we create local development databases corresponding to the snowflake user with `_PREP` and `_PROD` suffixes, corresponding to the `PREP` and `PROD` databases in snowflake. These will be targeted by our main dbt project when run within the local environment so that contributors can develop and test changes to our dbt project. More detail on our development process within our dbt project can be found on the [dbt Change Workflow page](https://handbook.gitlab.com/handbook/enterprise-data/how-we-work/dbt-change-workflow/).

Any data built within these development databases should be considered ephemeral as they’re only to be used for local development. To ensure the optimal use of dbt, as well as appropriate security and compliace, these databases should be cleaned by the owning user regularly. [This Runbook](https://gitlab.com/gitlab-data/runbooks/-/blob/main/Snowflake/snowflake_dev_clean_up.md) can be used to make that process quick and easy, and it’s suggested to be run at the end or beginning of each development cycle. Additionaly, in order to ensure compliance with our data retention policies and procedures we will automatically drop all tables in development environments after **80 days** without alteration. This retention period is set within the dbt project with the `dev_db_object_expiration` variable and tables are deleted each weekend.

Note: Development databases are dropped as soon as the corresponding Team Member is deprovisioned access to Snowflake (i.e. in case of offboarding or [inactive usage](https://handbook.gitlab.com/handbook/enterprise-data/data-management/#snowflake-1). There is not [backup]/handbook/enterprise-data/platform/#backups) process for development databases.

#### Configuration

  * Ensure you have access to our Snowflake instance and dedicated development databases for your snowflake user
  * Ensure you have [Make](https://en.wikipedia.org/wiki/Make_%28software%29) installed (should be installed on new Macs and with XCode)
  * Create a folder in your home directory called `.dbt`
  * In the `~/.dbt/` folder there should be a `profiles.yml`file that looks like this [sample profile](https://gitlab.com/gitlab-data/analytics/blob/master/admin/sample_profiles.yml)
  * The smallest possible warehouse should be stored as an environment variable. Our dbt jobs use `SNOWFLAKE_TRANSFORM_WAREHOUSE` as the variable name to identify the warehouse. The environment variable can be set in the `.bashrc` or `.zshrc` file as follows: 
    * `export SNOWFLAKE_TRANSFORM_WAREHOUSE="DEV_XS"`
    * In cases where more compute is required, this variable can be overwritten at run. We will cover how to do this in the [next section](https://handbook.gitlab.com/handbook/enterprise-data/platform/dbt-guide/#choosing-the-right-snowflake-warehouse-when-running-dbt).
  * Clone the [analytics project](https://gitlab.com/gitlab-data/analytics/)
  * If running on Linux: 
    * Ensure you have [Rancher Desktop Installed](https://rancherdesktop.io/)



Note that many of these steps are done in the [onboarding script](https://gitlab.com/gitlab-data/analytics/-/blob/master/admin/onboarding_script.zsh) we recommend new analysts run.

#### Choosing the right Snowflake warehouse when running dbt

Our Snowflake instance contains [warehouses of multiple sizes](https://docs.snowflake.com/en/user-guide/warehouses-overview), which allow for dbt developers to allocate differing levels of compute resources to the queries they run. The larger a warehouse is and the longer it runs, the more the query costs. For example, it costs [8 times](https://docs.snowflake.com/en/user-guide/warehouses-overview#warehouse-size) more to run a Large warehouse for an hour than it costs to run an X-Small warehouse for an hour.

If you have access to multiple warehouses, you can create an entry for each warehouse in your `profiles.yml` file. Having done this, you will be able to specify which warehouse should run when you call `dbt run`. This should be done carefully; using a larger warehouse increases performance but will greatly increase cost! Err on the side of using smaller warehouses. If you find that the smaller warehouse’s performance is not adequate, investigate the cause before you try again with a larger warehouse. Running an inefficient model against a larger warehouse not only increases cost during development, it also increases cost every time the model runs in production, resulting in unintentional ongoing increase in Snowflake costs.

#### Example

Imagine that you are a Data Team member who needs to make a change to a dbt model. You have access to both an X-Small warehouse and a Large warehouse, and your `profiles.yml` file is set up like so:
    
    
    gitlab-snowflake:
      target: dev
      outputs:
        dev:
          type: snowflake
          threads: 8
          account: gitlab
          user: {username}
          role: {rolename}
          database: {databasename}
          warehouse: DEV_XS
          schema: preparation
          authenticator: externalbrowser
        dev_l:
          type: snowflake
          threads: 16
          account: gitlab
          user: {username}
          role: {rolename}
          database: {databasename}
          warehouse: DEV_L
          schema: preparation
          authenticator: externalbrowser
    

You open up your terminal and code editor, create a new branch, make an adjustment to a dbt model, and save your changes. You are ready to run dbt locally to test your changes, so you enter in the following command: `dbt run --models @{model_name}`. dbt starts building the models, and by default it builds them using the `ANALYST_XS` warehouse. After a while, the build fails due to a timeout error. Apparently the model tree you are building includes some large or complex models. In order for the queries to complete, you’ll need to use a larger warehouse. You want to retry the build, but this time you want dbt to use the `ANALYST_L` warehouse instead of `ANALYST_XS`. So you enter in `dbt run --models @{model_name} --target dev_l`, which tells dbt to use the warehouse you specified in the `dev_l` target in your `profiles.yml` file. After a few minutes, the build completes and you start checking your work.

#### Venv Workflow

Recommended workflow for anyone running a Mac system.

#### Using dbt

  * Ensure you have the `DBT_PROFILE_PATH` environment variable set. This should be set if you’ve used the [onboarding_script.zsh](https://gitlab.com/gitlab-data/analytics/-/blob/master/admin/onboarding_script.zsh) (recommened to use this as this latest and updated regularly), but if not, you can set it in your `.bashrc` or `.zshrc` by adding `export DBT_PROFILE_PATH="/<your_root_dir/.dbt/"` to the file or simply running the same command in your local terminal session
  * Ensure that you have updated your `.dbt/profiles.yml` with your specific user configuration
  * Ensure your SSH configuration is setup according to the [GitLab directions](https://gitlab.com/help/ssh/README). Your keys should be in `~/.ssh/` and the keys should have been generated with no password. 
    * You will also need access to [this project](https://gitlab.com/gitlab-data/data-tests) to run `dbt deps` for our main project.
  * **NB** : Ensure your default browser is set to chrome. The built-in SSO login only works with chrome
  * **NB** : Ensure you are in the folder where your `/analytics` repo is located. If you installed everything properly `jump analytics` will land you where it is needed in order to run `dbt` commands successfully.
  * **NB** : Before running dbt for the first time run `make prepare-dbt`. This will ensure you have venv installed. 
    * This will run a [series of commands](https://gitlab.com/gitlab-data/analytics/-/blob/master/Makefile#L111-114) including downloading and running a `poetry` install script.
    * If you get a certificate error like this `urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1124)>`, follow these [StackOverflow instructions](https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org/53310545#53310545).
  * To start a `dbt` container and run commands from a shell inside it, use `make run-dbt`. This command will install or update the dependencies required for running dbt.
  * To start a `dbt` container without the dependency update use `make run-dbt-no-deps`. This command assumes you already have the dbt dependencies installed. When using this command, if you make changes in any of the dependency packages (e.g. data-tests), you will need to run either `dbt deps` (from within the shell) or `make run-dbt` again for these changes to show up in your repository.
  * This will automatically import everything `dbt` needs to run, including your local `profiles.yml` and repo files
  * To see the docs for your current branch, run `make run-dbt-docs` and then visit `localhost:8081` in a web-browser. Note that this requires the `docs` profile to be configured in your `profiles.yml`



#### Why do we use a virtual environment for local dbt development?

We use virtual environments for local dbt development because it ensures that each developer is running exactly the same dbt version with exactly the same dependencies. This minimizes the risk that developers will have different development experiences due to different software versions, and makes it easy to upgrade everyone’s software simultaneously. Additionally, because our staging and production environments are containerized, this approach ensures that the same piece of code will execute as predictably as possible across all of our environments.

#### Build Changes Locally

To clone and build all of the changed models in the local development space the same `build_changes` process can be used that is used in the [CI Job](https://handbook.gitlab.com/handbook/enterprise-data/platform/ci-jobs/#build_changes). The primary difference is that instead of a `WAREHOUSE` variable the developer can pass a `TARGET` variable to use a target configured with a different warehouse size. To run the process, run the `make build-changes` command from within the virtual environment.
    
    
     ~/repos/analytics/transform/snowflake-dbt
    ╰─$ make build-changes DOWNSTREAM="+1" FULL_REFRESH="True" TARGET="dev_xl" VARS="key":"value" EXCLUDE="test_model"
    

[Video Introduction](https://youtu.be/0WiljW6Bihw)

#### SQLFluff linter

We use SQLFluff to enforce [SQL style guide](https://handbook.gitlab.com/handbook/enterprise-data/platform/sql-style-guide/) on our code. In addition to the methods for executing the linter found in the documentation, when in the dbt virtual environment the `make lint-models` can be used. By default the `lint-models` process will lint all changed sql files, but the `MODEL` variable can be used to lint a specif sql file and the `FIX` variable can be used to run the linters fix command that will make changes to the sql file.
    
    
    ~/repos/analytics/transform/snowflake-dbt
    ╰─$ make lint-models
    sqlfluff lint models/workspaces/workspace_data/mock/data_type_mock_table.sql
    
    ~/repos/analytics/transform/snowflake-dbt
    ╰─$ make lint-models FIX="True" MODEL="dim_date"
    sqlfluff fix ./models/common/dimensions_shared/dim_date.sql
    

[Video Introduction](https://youtu.be/MwVJHf7XvrI)

#### SAFE Check Locally

To test for SAFE coverage in model the same `safe_model_script` process can be used that is used in the [CI Job](https://handbook.gitlab.com/handbook/enterprise-data/platform/ci-jobs/#safe_model_script). To run the process, run the `make safe-check` command from within the virtual environment.
    
    
     ~/repos/analytics/transform/snowflake-dbt
    ╰─$ make safe-check
    

#### Cloning models locally

This command enables zero copy cloning using dbt selections syntax to clone entire lineages. This is far faster and more cost-effective than running the models using dbt but do not run any dbt validations. As such, all dbt users are encouraged to use this command to set up your environment.

**Prerequisites:**

  * Ensure you have dbt setup and are able to run models
  * These local commands run using the SnowFlake user configured in `/.dbt/profiles.yml`, and will skip any table which your user does not have permissions to.
  * These commands run using the same logic as the dbt CI pipelines, using the `DBT_MODELS` as a variable to select a given lineage.
  * You need to be in the `/analytics` directory to run these commands.



**Usage:**

To use the new `clone-dbt-select-local-user-noscript` command, you have to specify a `DBT_MODELS` variable. For example, to clone only the `dim_subscription` model, you would execute the following command:
    
    
    make DBT_MODELS="dim_subscription" clone-dbt-select-local-user-noscript
    

This will clone the dbt model from the `prod` branch into your local user database (i.e., `{user_name}_PROD`). You can use dbt selectors: @, +, etc to select the entire lineage that you want to copy over your local database.

**Tips:**

  * If you encounter an error as below:
    
        Compilation Error
      dbt found 7 package(s) specified in packages.yml, but only 0 package(s)
      installed in dbt_packages. Run "dbt deps" to install package dependencies.
    

  * Run `make dbt-deps` from the root of the analytics folder and retry the command.




**Transition Note:**

We are actively transitioning to the new `clone-dbt-select-local-user-noscript` command. The old `clone-dbt-select-local-user` command will still be available for a limited time, but we encourage you to start using the new command as soon as possible.

##### Cloning into local user DB (python scripts - pre-`dbt clone`)

  * This clones the given dbt model lineage into the active branch DB (ie. `{user_name}_PROD`) 
    * `make DBT_MODELS="<dbt_selector>" clone-dbt-select-local-user`
    * eg. `make DBT_MODELS="+dim_subscription" clone-dbt-select-local-user`



##### Cloning into branch DB

  * This clones the given dbt model lineage into the active branch DB (ie. `{branch_name}_PROD`), this is equivalent to running the CI pipelines clone step.
  * It does not work on Master. 
    * `make DBT_MODELS="<dbt_selector>" clone-dbt-select-local-branch`
    * eg. `make DBT_MODELS="+dim_subscription" clone-dbt-select-local-branch`



### Docker Workflow

The below is the recommended workflow primarily for users running Linux as the venv workflow has fewer prerequisites and is considerably faster.

To abstract away some of the complexity around handling `dbt` and its dependencies locally, the main [analytics project](https://gitlab.com/gitlab-data/analytics/) supports using `dbt` from within a `Docker` container. We build the container from the [`data-image`](https://gitlab.com/gitlab-data/data-image) project. There are commands within the `Makefile` to facilitate this, and if at any time you have questions about the various `make` commands and what they do, use `make help` to get a list of the commands and what each of them does.

Before your initial run (and whenever the containers get updated) make sure to run the following commands:

  1. `make update-containers`
  2. `make cleanup`



These commands will ensure you get the newest versions of the containers and generally clean up your local `Docker` environment.

#### Using dbt

  * Ensure you have the `DBT_PROFILE_PATH` environment variable set. This should be set if you’ve used the [onboarding_script.zsh](https://gitlab.com/gitlab-data/analytics/-/blob/master/admin/onboarding_script.zsh) (recommened to use this as this latest and updated regularly) or [onboarding_script.sh](https://gitlab.com/gitlab-data/analytics/blob/master/admin/onboarding_script.sh), but if not, you can set it in your `.bashrc` or `.zshrc` by adding `export DBT_PROFILE_PATH="/<your_root_dir/.dbt/"` to the file or simply running the same command in your local terminal session
  * Ensure that you have updated your `.dbt/profiles.yml` with your specific user configuration
  * Ensure your SSH configuration is setup according to the [GitLab directions](https://gitlab.com/help/ssh/README). Your keys should be in `~/.ssh/` and the keys should have been generated with no password. 
    * You will also need access to [this project](https://gitlab.com/gitlab-data/data-tests) to run `dbt deps` for our main project.
  * To start a `dbt` container and run commands from a shell inside of it, use `make dbt-image`
  * This will automatically import everything `dbt` needs to run, including your local `profiles.yml` and repo files 
    * You may see some WARNINGS about missing variables (`GIT_BRANCH`, `KUBECONFIG`, `GOOGLE_APPLICATION_CREDENTIALS`, etc.). Unless you are developing on Airflow this is ok and expected.
  * To see the docs for your current branch, run `make dbt-docs` and then visit `localhost:8081` in a web-browser. Note that this requires the `docs` profile to be configured in your `profiles.yml`
  * Once inside of the `dbt` container, run any `dbt` commands as you normally would
  * Changes that are made to any files in the repo will automatically be updated within the container. There is no need to restart the container when you change a file through your editor!



#### Command line cheat sheet

This is a simplified version of the [primary command reference](https://docs.getdbt.com/reference/dbt-commands).

dbt specific:

  * [`dbt clean`](https://docs.getdbt.com/reference/commands/clean) \- this will remove the `/dbt_modules` (populated when you run deps) and `/target` folder (populated when models are run)

  * [`dbt run`](https://docs.getdbt.com/reference/commands/run) \- regular run

  * Model selection syntax ([source](https://docs.getdbt.com/reference/node-selection/syntax)). Specifying models can save you a lot of time by only running/testing the models that you think are relevant. However, there is a risk that you’ll forget to specify an important upstream dependency so it’s a good idea to understand the syntax thoroughly:

    * `dbt run --models modelname` \- will only run `modelname`
    * `dbt run --models +modelname` \- will run `modelname` and all parents
    * `dbt run --models modelname+` \- will run `modelname` and all children
    * `dbt run --models +modelname+` \- will run `modelname`, and all parents and children
    * `dbt run --models @modelname` \- will run `modelname`, all parents, all children, AND all parents of all children
    * `dbt run --exclude modelname` \- will run all models except `modelname`
    * Note that all of these work with folder selection syntax too: 
      * `dbt run --models folder` \- will run all models in a folder
      * `dbt run --models folder.subfolder` \- will run all models in the subfolder
      * `dbt run --models +folder.subfolder` \- will run all models in the subfolder and all parents
  * `dbt run --full-refresh` \- will refresh incremental models

  * [`dbt test`](https://docs.getdbt.com/reference/commands/test) \- will run custom data tests and schema tests; TIP: `dbt test` takes the same `--model` and `--exclude` syntax referenced for `dbt run`

  * [`dbt seed`](https://docs.getdbt.com/reference/commands/seed) \- will load csv files specified in the `data-paths` [directory](https://gitlab.com/gitlab-data/analytics/-/tree/master/transform/snowflake-dbt/data) into the data warehouse. Also see the [seeds section of this guide](https://handbook.gitlab.com/handbook/enterprise-data/platform/dbt-guide/#seeds)

  * [`dbt compile`](https://docs.getdbt.com/reference/commands/compile) \- compiles the templated code within the model(s) and outputs the result in the `target/` folder. This isn’t a command you will need to run regularly as dbt will compile the models automatically when you to ‘dbt run’. One common use-case is the compiled code can be run in Snowflake directly for debugging a model.

Works only if you’ve run the [onboarding script](https://gitlab.com/gitlab-data/analytics/-/blob/master/admin/onboarding_script.sh):

  * `dbt_run_changed` \- a function we’ve added to your computer that only runs models that have changed (this is accessible from within the docker container)

  * `cycle_logs` \- a function we’ve added to your computer to clear out the dbt logs (not accessible from within the docker container)

  * `make dbt-docs` \- a command that will spin up a local container to serve you the `dbt` docs in a web-browser, found at `localhost:8081`




### VSCode extension: dbt Power User

[dbt Power User](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user) makes VScode seamlessly work with dbt. The guide below will allow you to install dbt Power User if you followed the [Venv workflow](https://handbook.gitlab.com/handbook/enterprise-data/platform/dbt-guide/#Venv-workflow).

Before we start, there are some settings to adjust in your VScode:

  * Go in Code > Settings > Settings…

    * Search for ‘Python info visibility’ > Set this setting as ‘Always’
    * In a terminal, run `make run-dbt` as described in the [Using dbt](https://handbook.gitlab.com/handbook/enterprise-data/platform/dbt-guide/#using-dbt) section. Once it ran and the new shell spawned, run `echo $VIRTUAL_ENV`. Copy that value. 
      * Search for ‘venv path’ in VScode settings.
      * Set this setting to the path that you copied last step, which should look like `/Users/<username>/Library/Caches/pypoetry/virtualenvs/` if you followed a standard installation. Remove the last part of the path `analytics-*******-py3.10` at the time of writing.
  * Open VScode in /analytics (File > Open Folder… or Workspace…)

  * You now see a python interpreter selector at the bottom right of VScode, click on it

    * In the popup field, you should now see the analytics venv(s) shown as type `poetry`, and the one used for dbt. Select it.
  * Install extension `dbt-power-user`

  * Follow only step `How to setup the extension > Associate your .sql files the jinja-sql language` [here](https://marketplace.visualstudio.com/items?itemName=innoverio.vscode-dbt-power-user)

  * In VScode, go back to the File view and find the `analytics/.vscode/settings.json` file that was created when you opened `/analytics` with vscode (create `.vscode/settings.json` if you cannot find it). This file will define the settings of VScode when opened in `/analytics`

Add this in your `settings.json` file:
    
        {
    "terminal.integrated.env.osx": {
    "SHELL":"/bin/zsh",
    "DBT_PROFILES_DIR": "../../../.dbt/",
    "DATA_TEST_BRANCH":"main",
    "SNOWFLAKE_PROD_DATABASE":"PROD",
    "SNOWFLAKE_PREP_DATABASE":"PREP",
    "SNOWFLAKE_SNAPSHOT_DATABASE":"SNOWFLAKE",
    "SNOWFLAKE_LOAD_DATABASE":"RAW",
    "SNOWFLAKE_STATIC_DATABASE":"STATIC",
    "SNOWFLAKE_PREP_SCHEMA":"preparation",
    "SNOWFLAKE_TRANSFORM_WAREHOUSE":"ANALYST_XS",
    "SALT":"pizza",
    "SALT_IP":"pie",
    "SALT_NAME":"pepperoni",
    "SALT_EMAIL":"cheese",
    "SALT_PASSWORD":"416C736F4E6F745365637265FFFFFFAB"
    },
    "dbt.queryLimit": 500
    }
    

Note: If the code base is updated with new values for these environment variables, you will have to update them in your `settings.json` according to the values of variables located in the `Makefile` at the root of the analytics repository.

  * Edit `DBT_PROFILES_DIR` so that it points to your `~/.dbt/` folder (it seems that path must be relative and pointing to your `~/.dbt` folder, from the `/analytics` folder)

  * Restart VScode and re-open the analytics workspace

  * Check that dbt-power-user is running by navigating through models with Command+click (dbt needs some time to init). Ignore any warnings about dbt not up to date.

  * Open a random model, right click in the sql code, Click `run dbt model` and check for output.

If you are getting an error of the type:
    
        dbt.exceptions.RuntimeException: Runtime Error
      Database error while listing schemas in database ""PROD_PROD""
      Database Error
        002043 (02000): SQL compilation error:
        Object does not exist, or operation cannot be performed.
    

  * then change the target profile used by dbt: navigate to dbt-power-user extension settings (Extensions > dbt-power-user > cog > Extension settings) and edit the setting called `Dbt: Run Model Command Additional Params` (same for build)




**Note**

When running/building/testing a model from VS code UI, the terminal window popping is only a log output. Cmd+C does not stop the job(s), nor clicking the Trash icon in VS code. If you want to stop a job started via VScode, go through the Snowflake UI and your job list and kill the job(s) from there.
