import argparse
from dlinfo import ExtractInfo

parser = argparse.ArgumentParser()
parser.add_argument('dl_no', type=str, help='Driving license number you want to use')
parser.add_argument('dob', type=str, help='Date of birth for driving license')

parser.add_argument('-o', '--output-file', type=str, help='Store the details in a file')

if __name__ == '__main__':
    #arguments = parser.parse_args()
    
    #details = ExtractInfo(arguments.dl_no, arguments.dob)
    details = ExtractInfo('DL-0420110149646', '09-02-1976')
    
    print(details.extract()) 
    