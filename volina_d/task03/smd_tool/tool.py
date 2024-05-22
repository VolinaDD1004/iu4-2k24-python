from .parse import parseSMD
from argparse import ArgumentParser, BooleanOptionalAction
from os import path, chdir, listdir
import pickle

BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'

def runTests():
    test_num = 1
    chdir('./animset_t_anims')
    entries = listdir()

    for entry in entries:
        with open(entry, 'r') as f:
            txt = f.read().split()

        with open(entry, 'r') as f:
            smd = str(parseSMD(f)).split()

        print(f'Test {test_num} from {entry}: ', end='')
        if not list(set(smd).difference(txt)):
            print(f'{BOLD}{GREEN}Passing{ENDC}')
        else:
            print(f'{BOLD}{RED}Failing{ENDC}')
        test_num += 1

def main():
    parser = ArgumentParser(description='dumps SMD-files into python objects')

    parser.add_argument('-o', '--output',
                        type=str,
                        default='',
                        help='path to the output file')
    
    parser.add_argument('path',
                        type=str,
                        help="path to the SMD-file")
    
    parser.add_argument('--testing',
                        action=BooleanOptionalAction,
                        help="finds 'animset_t_anims' dir in the current dir and runs tests")

    args = parser.parse_args()

    test_mode = args.testing

    if test_mode:
        if not path.isdir('./animset_t_anims'):
            parser.error("testing dir does not exist the in current dir.")
        else:
            runTests()
        exit(0)

    path_to_smd = args.path

    if not path.isfile(path_to_smd):
        parser.error("file provided does not exist.")
    
    path_to_output = path.abspath(args.output) if len(args.output) else path.abspath(f'./{path.splitext(path.basename(path_to_smd))[0]}.pickle')

    with open(path_to_smd, 'r') as f:
        smd = parseSMD(f)

    with open(path_to_output, 'wb') as f:
        pickle.dump(smd, f)

    print(f'Binary data written to {path_to_output}')

if __name__ == '__main__':
    main()