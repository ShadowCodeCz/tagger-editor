import os

import taggereditor
import argparse

taggereditor.app.ApplicationCLI.run(argparse.Namespace(**{
    "configuration": "./debug.configuration.json",
    "path": "./.tagger"
}))

