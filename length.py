"""
Written by Dan Ngo
Python script to calculate the length of string(s)
"""
# Import libraries
import argparse

# Define Arugments so user can input a file instead of a string at command line
def parse_arguments():
    parser = argparse.ArgumentParser(description="Go through lines in a list and output the length of the string")
    parser.add_argument('string', nargs="?")
    parser.add_argument('-f', '--file', nargs='?', required=False, action='store', dest='fileinput', help='Absolute path to file to input', type=argparse.FileType('r'))
    parser.add_argument('-o', '--output', nargs='?', required=False, action='store', dest='fileoutput', help='Absolute path to output results', type=argparse.FileType('wb'))
    args = parser.parse_args()
    return args

def main():
    # Take the arguments and parse them out
    args = parse_arguments()
    # Check if the string field is empty and if so, look for the other arugments
    if args.string is None:
        x = args.fileinput.read().splitlines()
        for l in x:
            # Check if the file output arugment is inputted. If not, print the lengths out to the screen
            if args.fileoutput is None:
                print len(l)
            else:
                # Write out the lengths of the strings into the file. Enter a new line for each length count
                args.fileoutput.write('{}\n'.format(len(l)))
    else:
        # If a string value is present, print the length of that string on the screen
        print len(args.string)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
