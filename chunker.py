#!/usr/bin/python

import os
import getopt
import sys
import math
from shutil import copyfile


def show_help():
    print('Author: Bilal ATLI')
    print('chunker.py - Seperate files into chunk directories')
    print('Arguments:')
    print('  -s, --source : Source directory')
    print('  -o, --output : Output directory')
    print('  -c, --chunk : Chunk size [Default: 100]')
    print('  -e, --extension : File extension')
    print('  -v, --verbose : Verbose console output')


def is_integer(var):
    try:
        int(var)
        return True
    except ValueError:
        return False


def merge_dictionaries(dict1, dict2):
    dict3 = dict1.copy()
    dict3.update(dict2)
    return dict3


def list_of_files(directory, extension, verbose):
    if verbose:
        print('Scanning `' + directory + '`...')
    file_list = os.listdir(directory)
    all_files = {}
    for entry in file_list:
        full_path = os.path.join(directory, entry)
        if os.path.isdir(full_path):
            all_files = merge_dictionaries(all_files, list_of_files(full_path, extension, verbose))
        else:
            if os.path.splitext(entry)[1] == '.' + extension:
                all_files.update({os.path.splitext(entry)[0]: full_path})

    return all_files


def main(argv):
    source_directory = ''
    output_directory = ''
    chunk_size = 100
    extension = ''
    verbose = False
    try:
        opts, args = getopt.getopt(argv, "hs:o:c:e:v", ["source=", "output=", "chunk=", "verbose", "extension="])
    except getopt.GetoptError:
        show_help()
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            show_help()
            sys.exit()
        elif opt in ("-s", "--source"):
            source_directory = arg
        elif opt in ("-o", "--output"):
            output_directory = arg
        elif opt in ("-e", "--extension"):
            extension = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
        elif opt in ("-c", "--chunk"):
            if not is_integer(arg):
                print('Chunk size argument must be numeric value')
                sys.exit(1)
            chunk_size = int(arg)
    if source_directory == '' or output_directory == '':
        print('Source & output directory is required')
        sys.exit(1)
    if extension == '':
        print('File extension is required')
        sys.exit(1)

    files_list = list_of_files(source_directory, extension, verbose)
    sorted_list = sorted(files_list.items(), key = lambda x: int(x[0]))
    file_count = len(sorted_list)
    max_chunk = int(math.floor(file_count / chunk_size) + 1)
    print('--------------------------------------------------------')
    print('> Total ' + str(file_count) + ' files found in directory')
    print('> Total ' + str(max_chunk) + ' chunk creatable with ' + str(chunk_size) + ' chunk size')

    index = 0
    for key, path in sorted_list:
        file_chunk_index = int(math.floor(float(index) / float(chunk_size)) + 1)
        chunk_name = str(file_chunk_index * chunk_size)
        chunk_directory = os.path.join(output_directory, chunk_name)
        if not os.path.exists(chunk_directory):
            os.mkdir(chunk_directory)
            print('Chunk folder created `' + chunk_name + '`')
        copyfile(path, os.path.join(chunk_directory, os.path.basename(path)))
        index += 1


if __name__ == '__main__':
    main(sys.argv[1:])
