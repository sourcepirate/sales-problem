#!/usr/bin/python
from __future__ import print_function

import os
import sys
import argparse
from tax import Cart

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Prints recipts of billing.")
    parser.add_argument('-f', "--file", required=True, help="Input csv file")

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.file:
        abs_path = os.path.join(os.getcwd(), args.file)
        with open(abs_path) as f:
            cart = Cart.parse_input(f)
            print(str(cart))
    