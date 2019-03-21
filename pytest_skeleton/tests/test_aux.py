import pytest



@pytest.fixture()
def data():
    return range(100)

##data maps to the fixture above, comms to the fixture in conftest.py
def test_MyTest(comms, data):
    print(comms)
    print(data)
    assert data == range(100)
    print("just to show that it is possible" )
    print("one test multiple asserts!")
    assert False

