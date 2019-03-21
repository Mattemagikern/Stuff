import pytest
from common import comms as c

"""
Conftest.py is a global fixture base for the entire framework. any fixture that
needs to be shared between test files is placed here. 

@pytest.fixture(scope="session")
@pytest.fixture(scope="package") 
@pytest.fixture(scope="module")
#Do not recomend building testcases in classes.
#It will bite you in the arse later..  Just showing that it is possible
@pytest.fixture(scope="class") 
@pytest.fixture(scope="function") #default value
"""

@pytest.fixture(scope="session")
def comms():
    #create comms by ex. serial
    return c.setup_comms("ya","no","no")

