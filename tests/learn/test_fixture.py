import pytest


@pytest.fixture()
def postcode():
    return "010"

def test_postcode(postcode):
    assert postcode == "010"
    

@pytest.fixture()
def db():
    print("connect successful.")
    yield
    print("connect closed")

def seach_user(user_id):
    d = {
        '001': 'xiaoming'
    }
    return d[user_id]
    
def test_search(db):
    assert seach_user("001") == "xiaoming"