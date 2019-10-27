# coding=UTF-8
import argparse
import logging
import sys


class UserCommon(object):
    pass


class Manager(UserCommon):
    pass


class Salesman(UserCommon):
    pass


def get_args():
    parser = argparse.ArgumentParser('Available CoffeeTool arguments:')

    parser.add_argument('-I', '--interactive',
                        default=False,
                        action='store_true',
                        help='Enter Interactive mode')

    parser.add_argument('-un', '--user-name',
                        default=None,
                        help='User name')

    parser.add_argument('-up', '--user-position',
                        default=None,
                        help='User position. (Salesman or Manager)')

    parser.add_argument('-bt', '--beverage-type',
                        default=None,
                        help='Beverage type')

    parser.add_argument('-ai', '--additional-ingredients',
                        default=None,
                        help='Additional beverage ingredients (sugar, cream, cinnamon, etc.)')

    parser.add_argument('-bp', '--beverage-price',
                        default=None,
                        help='Set beverage price')

    parser.add_argument('-sf', '--separate-file',
                        default=None,
                        help='Save the sale details in separate file')

    parser.add_argument('-ds', '--details-salesman',
                        default=None,
                        help='Folder to export the sales details per salesman')

    return parser.parse_args()


def adding_beverage(str):
    pass


def interactive_workflow():
    print('You\'ve entered Interactive mode.')


def logging_init(file_path):
    global logger
    logger = logging.getLogger('CoffeeTool log')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(file_path)
    formatter = logging.Formatter('%(asctime)s [%(module)s]/[%(funcName)s] %(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)


if __name__ == '__main__':
    logging_init('main.log')
    logger.info('Entering main...')
    args = get_args()

    if not len(sys.argv) > 1:
        print(
            'You haven\'t specified any arguments! \r\n'
            'Please use -I for interactive mode or run CoffeeForMe Tool with command line arguments. \r\n'
            'Use -h arg for more info.')
        logger.info('No args specified. Shutting down.')

    elif args.interactive:
        print('Welcome to CoffeeForMe Tool for handling your beverages!')
        logger.info('Running interactive mode')
        interactive_workflow()

    else:
        logger.info('Got the following args: {}. Processing...'.format(vars(args)))
        adding_beverage(args)
