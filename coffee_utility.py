# coding=UTF-8
import argparse
import logging
import os
import sys
import yaml

from six.moves import input

BEVERAGES = ['Coffee', 'Juice', 'Tea', 'Water']
ADDITIONAL_INGREDIENTS = ['Cream', 'Cinnamon', 'Milk', 'Sugar']
USER_POSITIONS = ['Manager', 'Salesman']


class UserCommon(object):
    """
    Main User object
    """

    def __init__(self, name):
        self.name = name


class Manager(UserCommon):
    def __init__(self, name):
        super(Manager, self).__init__(name)

    def generate_sales_report(self):
        """
        Method for generating report about all salesman's.
        :return: file
        """
        # TODO: implement
        pass


class Salesman(UserCommon):
    def __init__(self, name):
        super(Salesman, self).__init__(name)
        self.beverage_counter = _init_counter(name)

    def add_beverage(self, beverage_type, add_ingrdts, price, sale_details_file):
        """
        Method to add beverage records
        :param beverage_type: str
        :param add_ingrdts: str
        :param price: float
        :param sale_details_file: file_path
        """
        beverage_record = {self.beverage_counter: {'SoldBy': str(self.name).lower(),
                                                   'BeverageDetails': {'Type': beverage_type,
                                                                       'Ingredients': add_ingrdts, 'Price': price}}}

        logger.info('Adding beverage with the following params: {}'.format(str(beverage_record)))
        with open('./records.yml', 'a') as records_file:
            yaml.dump(beverage_record, records_file, default_flow_style=False)

        if sale_details_file:
            try:
                dir = os.path.dirname(sale_details_file)
                if not os.path.exists(dir) and dir:
                    os.makedirs(dir)
                with open(sale_details_file, 'w') as sale_file:
                    sale_file.write(
                        'Sold by {0}:\r\n Beverage: {1}, Additional Ingredients: {2}, Price: {3}'.format(self.name,
                                                                                                         beverage_type,
                                                                                                         add_ingrdts,
                                                                                                         price))
                success_msg = 'Sale details have been saved to {}'.format(sale_details_file)
                print(success_msg)
                logger.info(success_msg)
            except IOError as err:
                logger.critical(
                    'Could not write sale details to a file {}. Error: {}'.format(sale_details_file, str(err)))

        logger.info('Adding was successful!')
        print('Your beverage with price {} was successfully saved!'.format(price))

    def export_salesman_details(self, file_path):
        """
        Method for generating report about particular Salesman sales into defined file_path.
        :param file_path: file_path
        """
        all_records = _get_all_records()
        if len(all_records) == 0:
            logger.info('No records is available. Skipping export salesman details.')
            return

        salesman_records = []
        for record in all_records.values():
            if record['SoldBy'] == str(self.name).lower():
                salesman_records.append(record)

        if len(salesman_records) == 0:
            logger.info('No records is available for Salesman {}. Skipping export salesman details.'.format(self.name))
            return

        try:
            dir = os.path.dirname(file_path)
            if not os.path.exists(dir) and dir:
                os.makedirs(dir)
            with open(file_path, 'w') as salesman_file:
                output = ['Salesman {} sold the following:'.format(self.name)]
                for sale in salesman_records:
                    output.append(str(sale['BeverageDetails']))
                salesman_file.write('\n'.join(output))
            success_msg = 'Salesman {} sales details have been saved to {}'.format(self.name, file_path)
            print(success_msg)
            logger.info(success_msg)
        except IOError as err:
            logger.critical(
                'Could not write sales details to a file {}. Error: {}'.format(file_path, str(err)))


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

    parser.add_argument('-sd', '--sale-details',
                        default=None,
                        help='Save the sale details in separate file')

    parser.add_argument('-ds', '--details-salesman',
                        default=None,
                        help='Folder to export the sales details per salesman')

    return parser.parse_args()


def interactive_workflow():
    name = input('Provide your Name, please: ')
    _display_position_selector()
    option = _get_position_choice()
    if option == 1:
        _display_salesman_menu()
        option_salesman = _get_salesman_choice()
        if option_salesman == 1:
            pass
            # TODO: Collect beverage detail and go with:
            # Salesman(name).add_beverage()
        elif option_salesman == 2:
            # TODO: Collect path and go with:
            Salesman(name).export_salesman_details('path_for_details_collected.txt')
        _terminate()
    elif option == 2:
        _display_manager_menu()
        option_manager = _get_manager_choice()
        if option_manager == 1:
            Manager(name).generate_sales_report()
        _terminate()
    elif option == 0:
        _terminate()


def logging_init(file_path):
    global logger
    logger = logging.getLogger('CoffeeTool log')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(file_path)
    formatter = logging.Formatter('%(asctime)s [%(module)s]/[%(funcName)s] %(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def validate_args(args):
    if args.beverage_type not in BEVERAGES:
        raise TypeError(
            'Beverage value provided [{}] should be one of the following {}'.format(args.beverage_type, BEVERAGES))
    if args.additional_ingredients not in ADDITIONAL_INGREDIENTS:
        raise TypeError(
            'Ingredient provided [{}] should be one of the following {}'.format(args.additional_ingredients,
                                                                                ADDITIONAL_INGREDIENTS))
    if args.user_position not in USER_POSITIONS:
        raise TypeError(
            'User position provided [{}] should be one of the following {}'.format(args.user_position, USER_POSITIONS))

    try:
        args.beverage_price = float(args.beverage_price)
    except:
        raise TypeError(
            'Beverage price provided [{}] should have floating point value! For example - 11.23'.format(
                args.beverage_price))


def _display_position_selector():
    print('Select your User Position:\n'
          '1. Salesman\n'
          '2. Manager\n'
          'Press 0 for exit')


def _get_position_choice():
    is_valid = False
    while not is_valid:
        try:
            input_value = input('Option selected: ')
            choice = int(input_value)
            if 0 <= choice <= 2:
                is_valid = True
            else:
                print('{} is not a valid option. Please choose from 0 to 2'.format(input_value))
                logger.info('Interactive input on position selection: {}'.format(input_value))
        except Exception:
            print('{} is not a valid option. Please choose from 0 to 2'.format(input_value))
    return choice


def _display_salesman_menu():
    print('Select your action:\n'
          '1. Add beverage\n'
          '2. Get report about your sales\n'
          'Press 0 for exit')


def _get_salesman_choice():
    is_valid = False
    while not is_valid:
        try:
            input_value = input('Option selected: ')
            choice = int(input_value)
            if 0 <= choice <= 2:
                is_valid = True
            else:
                print('{} is not a valid option. Please choose from 0 to 2'.format(input_value))
                logger.info('Interactive input on salesman selection: {}'.format(input_value))
        except Exception:
            print('{} is not a valid option. Please choose from 0 to 2'.format(input_value))
    return choice


def _display_manager_menu():
    print('Select your action:\n'
          '1. Get report about all salesman\'s\n'
          '0. Exit\n'
          'Press 0 for exit')


def _get_manager_choice():
    is_valid = False
    while not is_valid:
        try:
            input_value = input('Option selected: ')
            choice = int(input_value)
            if 0 <= choice <= 1:
                is_valid = True
            else:
                print('{} is not a valid option. Please choose from 0 to 1'.format(input_value))
                logger.info('Interactive input on manager\'s option selection: {}'.format(input_value))
        except Exception:
            print('{} is not a valid option. Please choose from 0 to 1'.format(input_value))
    return choice


def _init_counter(name):
    try:
        with open('./records.yml', 'r') as records_file:
            data = [record for record in yaml.safe_load(records_file)]
        next_record_number = max(data) + 1
        return next_record_number
    except:
        return 1


def _get_all_records():
    try:
        with open('./records.yml', 'r') as records_file:
            data = [record for record in yaml.safe_load_all(records_file)]
        return data[0]
    except:
        return []


def _terminate():
    print('Thank you for using our CoffeeForMe Tool !')
    exit(0)


if __name__ == '__main__':
    logging_init('main.log')
    logger.info('Entering main...')
    args = get_args()

    if not len(sys.argv) > 1:
        print(
            'You haven\'t specified any arguments! \n'
            'Please use -I for interactive mode or run CoffeeForMe Tool with command line arguments. \n'
            'Use -h arg for more info.')
        logger.info('No args specified. Shutting down.')

    elif args.interactive:
        print('Welcome to CoffeeForMe Tool for handling your beverages!')
        logger.info('Running interactive mode')
        interactive_workflow()

    else:
        validate_args(args)
        logger.info('Got the following args: {}. Processing...'.format(vars(args)))
        if args.user_position == 'Salesman':
            Salesman(args.user_name).export_salesman_details(args.details_salesman) if args.details_salesman else None
            Salesman(args.user_name).add_beverage(args.beverage_type,
                                                  args.additional_ingredients,
                                                  args.beverage_price,
                                                  args.sale_details)
        elif args.user_position == 'Manager':
            Manager(args.user_name).generate_sales_report()
        logger.info('Processing finished.')
