#!/usr/bin/env python3

import aws_cdk as cdk

from demo.demo_stack import DemoStack


app = cdk.App()
DemoStack(app, "DemoStack")

app.synth()
