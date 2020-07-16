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
    local(f"git push origin master") #GitLab

    # As TravisCI is integrated with GitHub
    # Ask: Feature Branch vs. Master (Ideally Feature)
    local("git branch")
    branch = input("Which branch do you want to push to? ")
    local(f"git push github {branch}") #GitHub

def prepare():
    test()
    commit()
    push()

def pull():
    local("git pull origin master")

def heroku_stage():
    local("git push stage master")

def heroku_test():
    local("heroku run nosetests -v --app nflask-stage")

def deploy_stage():
    prepare()
    heroku_stage()
    heroku_test()

def rollback():
    local("heroku rollback --app nflask-stage")

 