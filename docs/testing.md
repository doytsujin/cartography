## How to test Cartography as a developer

### Running from source

1. **Install**

    Follow steps 1 and 2 in [Installation](https://github.com/lyft/cartography/blob/master/README.md#installation).  Ensure that Neo4j Community is running on your local machine.
2. **Clone the source code**

    Run `cd {path-where-you-want-your-source-code}`.  Get the source code with `git clone git://github.com/lyft/cartography.git`
    
3. **Install from source**

    Run `cd cartography` and then `pip install -e .` (yes, actually type the period into the command line) to install Cartography from source.  
 
    ℹ️You may find it beneficial to use Python [virtualenvs](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/) (or the  [virutalenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html#managing-environments)) so that packages installed via `pip` are easier to manage.

4. **Run from source** 

    After this finishes you should be able to run Cartography from source with `cartography --neo4j-uri <uri for your neo4j instance; usually bolt://localhost:7687>`.  Any changes to the source code in `{path-where-you-want-your-source-code}/cartography` are now locally testable by running `cartography` from the command line.

### Manually testing individual intel modules

After completing the section above, you are now able to manually test intel modules.
   
1. **If needed, comment out unnecessary lines** 

    See `cartography.intel.aws._sync_one_account()`[here](https://github.com/lyft/cartography/blob/master/cartography/intel/aws/__init__.py).  This function syncs different AWS objects with your Neo4j instance.  Comment out the lines that you don't want to test for.
  
    For example, IAM can take a long time to ingest so if you're testing an intel module that doesn't require IAM nodes to already exist in the graph, then you can comment out all of the `iam.sync_*` lines.
  
2. Save your changes and run `cartography` from a terminal as you normally would.

### Automated testing

1. **Install test requirements**

    `pip install -r test-requirements.txt`
   
2. **(OPTIONAL) Setup environment variables for integration tests**

    The integration tests expect Neo4j to be running locally, listening on default ports, with auth disabled. To run the integration tests on a specific Neo4j instance, add the following environment variable:

    `export "NEO4J_URL=<your_neo4j_instance_url:your_neo4j_instance_port>"`
    
3. **Run tests using `make`**️

    - `make test_lint` can be used to run flake8 linting against the codebase.
    - `make test_unit` can be used to run the (currently non-existent) unit test suite.
    
    ⚠️ Important!  The below commands will **DELETE ALL NODES** on your local Neo4j instance as part of our testing procedure.  Only run any of the below commands if you are ok with this. ⚠️
    
    - `make test_integration` can be used to run the integration test suite.
    - `make test` can be used to run all of the above.
