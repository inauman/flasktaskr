from fabric.api import local, settings, abort
from fabric.contrib.console import confirm

def test():
    with settings(warn_only=True):
        #result = local("nosetests -V", capture=True)
        result = local("nosetests --with-coverage --cover-erase --cover-package=project")
    if result.failed and not confirm("Test failed. Continue?"):
        abort("Aborted at user request")
def commit():
    message = input("Enter a git commit message: ")
    local(f"git add . && git commit -am '{message}'")

def push():
    local("git push origin master")

def prepare():
    test()
    commit()
    push()

def pull():
    local("git pull origin master")

def heroku_stage():
    local("git push stage master")

def heroku_test():
    local("heroku run nosetests -v")

def deploy_stage():
    pull()
    test()
    commit()
    heroku_stage()
    heroku_test()