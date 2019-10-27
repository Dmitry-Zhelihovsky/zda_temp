# coding=UTF-8
import argparse


class Manager():
    pass


class Salesman(Manager):
    pass


def get_args():
    parser = argparse.ArgumentParser('Parsing CoffeeTool arguments')

    parser.add_argument('-I', '--interactive',
                        default=True,
                        help='Enter Interactive mode')

    # args for non interactive

    return parser.parse_args()

def adding_beverage(str):
    pass

def interactive_workflow():
    pass


def _logger(message):
    pass


if __name__ == '__main__':
    print('Hello to CoffeeForMe Tool for handling your beverages!')
    args = get_args()

    if args.interactive:
        _logger('Entering interactive mode')
        interactive_workflow()
    else:
        adding_beverage('put args here')
