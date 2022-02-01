import os

from pytest import raises
from ubw.main import ubwTest

def test_ubw():
    # test ubw without any subcommands or arguments
    with ubwTest() as app:
        app.run()
        assert app.exit_code == 0


def test_ubw_debug():
    # test that debug mode is functional
    os.chdir(r'C:\Users\Wcy34\Documents\GitHub\ubw_project\rtthread')
    argv = ['debug', 'attach']
    with ubwTest(argv=argv) as app:
        app.run()
        assert app.debug is True


def test_command1():
    # test command1 without arguments
    argv = ['command1']
    with ubwTest(argv=argv) as app:
        app.run()
        data,output = app.last_rendered
        assert data['foo'] == 'bar'
        assert output.find('Foo => bar')


    # test command1 with arguments
    argv = ['command1', '--foo', 'not-bar']
    with ubwTest(argv=argv) as app:
        app.run()
        data,output = app.last_rendered
        assert data['foo'] == 'not-bar'
        assert output.find('Foo => not-bar')

def test_ubw_init():
    # test command1 without arguments
    argv = ['init']
    with ubwTest(argv=argv) as app:
        app.run()
        data,output = app.last_rendered
        # assert data['foo'] == 'bar'


    # test command1 with arguments
    argv = ['init', '-p', r'C:\Users\Wcy34\Documents\GitHub\rtthread']
    with ubwTest(argv=argv) as app:
        app.run()
        data,output = app.last_rendered
        # assert data['foo'] == 'not-bar'

def test_ubw_build():
    # test command1 without arguments
    argv = ['build','SConsCommand']
    with ubwTest(argv=argv) as app:
        app.run()
        data,output = app.last_rendered
        # assert data['foo'] == 'bar'