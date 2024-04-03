from argparse import ArgumentParser

#Main project file
def main():
    print("hello world")
    print("added this code")
main()

#Parse command-line arguments.
def parse_args(arglist):
    parser = ArgumentParser()
    return parser.parse_args(argslist)
