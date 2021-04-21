import argparse

from shop import Shopping

parser = argparse.ArgumentParser(description='Process some shopping.')
parser.add_argument('shopping', metavar='list(str)', type=str, nargs='+',
                    help='a list of shopping items')

args = parser.parse_args()

shopping = Shopping(cart_list=args.shopping)
print(shopping)
