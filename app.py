#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk.cdk_stack import APIdataStack


app = cdk.App()
APIdataStack(app, "APIdataStack",)

app.synth()
