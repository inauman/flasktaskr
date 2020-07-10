from fabric.api import local

def test(): 
    local("nosetests --with-coverage --cover-erase --cover-package=project")

def commit():
    message = input("Enter a git commit message: ")
    local(f"git add . && git commit -am '{message}'")

def push():
    local("git push origin master")

def prepare():
    test()
    commit()
    push()