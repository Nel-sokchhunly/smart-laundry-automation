import os

import tabula
from tabulate import tabulate

import re


def is_start_with_number(line):
    return re.match(r'^\d', line)


def read_file(pdf_path):
    result = []

    tabula.convert_into(pdf_path, 'output.csv', output_format='csv', pages='all')

    # read the csv file
    with open('output.csv', 'r') as f:
        data = f.read()

        # split the data into lines
        lines = data.split('\n')

        for line in lines:
            # regex to check if string begins with a number
            if is_start_with_number(line):
                item = line.split(',')
                result.append(item)
            else:
                pass

    # delete the csv file
    os.remove('output.csv')

    return result


def split_users_into_groups(users):
    to_be_inactive = []
    to_be_active = []

    for user in users:
        user_code = user[1]
        username = user[2]
        origin_location = user[3]
        destination_location = user[4]

        if user_code == '':
            continue

        will_be_active = origin_location == 'Phnom Penh' and destination_location == 'Kirirom'
        will_be_inactive = origin_location == 'Kirirom' and destination_location == 'Phnom Penh'

        if will_be_active:
            to_be_active.append(username)
        elif will_be_inactive:
            to_be_inactive.append(username)

    return {
        'to_be_inactive': to_be_inactive,
        'to_be_active': to_be_active
    }


def read_pdf_file(pdf_path):
    # read the pdf file
    data = read_file(pdf_path)

    # split the users into groups
    result = split_users_into_groups(data)

    return result
