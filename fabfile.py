from fabric import Connection

with Connection('localhost') as c:
    c.local("echo 'Hi there'")
    #c.local("exec zsh")
    #c.local("nosetests -v")
    message = input("Enter a git commit message: ")
    c.local(f"git add . && git commit -am '{message}'")
    c.local("git push origin master")
    def test():
        c.local("nosetests -v")

    def commit():
        message = input("Enter a git commit message: ")
        c.local(f"git add . && git commit -am '{message}'")

    def push():
        c.local("git push origin master")

    def prepare():
        test()
        commit()
        push()