#!/usr/python/env python
from fabric import Connection, task

with Connection('localhost') as ctx:
    # c.local("echo 'Hi there'")
    # #c.local("exec ~/.zshrc")
    # c.local("nosetests -v")
    # message = input("Enter a git commit message: ")
    # c.local(f"git add . && git commit -am '{message}'")
    # c.local("git push origin master")

    @task
    def test(ctx):
        ctx.run("nosetests -v")
    @task
    def commit(ctx):
        message = input("Enter a git commit message: ")
        ctx.run(f"git add . && git commit -am '{message}'")
    @task
    def push(ctx):
        ctx.run("git push origin master")

    @task
    def prepare(ctx):
        test(ctx)
        commit(ctx)
        push(ctx)