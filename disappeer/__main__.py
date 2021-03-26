"""
disappeer.py

Main app run module for the disappeer app.

Copyright (C) 2021 Disappeer Labs
License: GPLv3
"""

import argparse
import sys 
from disappeer.root.rootapp import RootApp


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--home_dir', help='home directory')
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    app = RootApp(args)
    app.run()


if __name__ == '__main__':
    main()
