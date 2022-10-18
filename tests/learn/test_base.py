import pytest
import sys
import pandas as pd

# @pytest.mark.finished
def test_pass():
    assert (1,2,3) == (1,2,3)
    

# @pytest.mark.unfinished
@pytest.mark.skip(reason="skip")
def test_fail():
    assert (1, 2, 3) == (3, 2, 1)


class Foo:
    def __init__(self, name):
        self.name = name
    
    def run(self):
        raise RuntimeError(f"can't run {self.__class__.__name__} run method.")


# @pytest.mark.finished
def test_raises():
    # test raise exception whether as expect.
    with pytest.raises(RuntimeError) as e:
        Foo("hello").run()
    exec_msg = e.value.args[0]
    assert exec_msg == "can't run Foo run method."


@pytest.mark.skip(reason="unfinished")
def test_skip():
    print("unfinish develop.")
    pass


@pytest.mark.skipif(sys.version.split(" ")[0] >= "3.8.0", reason="the lastest version can run.")
def test_if_skip():
    print(sys.version.split(" ")[0])
    assert "hello" > "world"
    

@pytest.mark.xfail(pd.__version__ <= '1.2.4', reason='not supported until v1.2.4')
def test_xfail():
    assert pd.__version__ >= "1.2.4"


@pytest.mark.parametrize('passwd',['123456','abcdefdfs','as52345fasdf4'])
def test_passwd_length(passwd):
    assert len(passwd) >= 8
    

@pytest.mark.parametrize('user, passwd',[('jack', 'abcdefgh'),('tom', 'a123456a')])
def test_passwd_md5(user, passwd):
    db = {
        'jack': 'e8dc4081b13434b45189a720b77b6818',
        'tom': '1702a132e769a623c1adb78353fc9503'
    }

    import hashlib
    assert hashlib.md5(passwd.encode()).hexdigest() == db[user]