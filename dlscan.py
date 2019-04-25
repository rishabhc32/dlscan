import argparse
import json

from dlinfo import ExtractInfo

parser = argparse.ArgumentParser()
parser.add_argument('dl_no', type=str,
                    help='Driving license number you want to use')
parser.add_argument('dob', type=str, help='Date of birth for driving license')

parser.add_argument('-o', '--output-file', type=str,
                    help='Store the details in a file')

if __name__ == '__main__':
    arguments = parser.parse_args()

    details = ExtractInfo(arguments.dl_no, arguments.dob)
    result = details.extract()

    if result == None:
        exit()

    result = json.dumps(result, indent=4)

    if arguments.output_file == None:
        print(result)

    else:
        file_name = arguments.output_file

        with open(file_name, "a") as file:
            file.write(result)
            file.write('\n')

        print('Details written to file:', file_name)
