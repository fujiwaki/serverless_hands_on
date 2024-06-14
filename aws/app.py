"""AWS Resources for Chat App."""  # noqa: INP001

import aws_cdk as cdk
from stacks.api_stack import APIStack
from stacks.db_stack import DBStack

app = cdk.App()
db_stack = DBStack(app, "DBStack")
api_stack = APIStack(app, "APIStack", db_stack.table)

app.synth()
