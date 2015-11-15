#!/usr/bin/env python
from __future__ import print_function

DESCRIP = 'clear outputs from notebook and resave'
EPILOG = \
"""
Opens notebook(s) and clears code outputs and prompts, saving to new
filename.
"""
import io

from os.path import basename, splitext

from argparse import ArgumentParser, RawDescriptionHelpFormatter

from nbformat import read as nb_read, write as nb_write
NB_VERSION = 4


def cellgen(nb, type=None):
    for cell in nb['cells']:
        if type is None:
            yield cell
        elif cell.cell_type == type:
            yield cell


def strip_after_comments(code_input):
    if code_input.startswith('# - '):
        return code_input
    out_lines = []
    for line in code_input.splitlines():
        if not line.startswith('#'):
            break
        if line.startswith('#: '):
            break
        out_lines.append(line)
    return '\n'.join(out_lines)


def main():
    parser = ArgumentParser(description=DESCRIP,
                            epilog=EPILOG,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('in_fname', type=str,
                        help='input notebook filename')
    parser.add_argument('out_fname', type=str,
                        help='output notebook filename')
    args = parser.parse_args()
    with io.open(args.in_fname, 'r') as f:
        nb = nb_read(f, NB_VERSION)
    for cell in cellgen(nb, 'code'):
        if 'execution_count' in cell:
            cell['execution_count'] = None
        cell['outputs'] = []
        if 'source' in cell:
            cell['source'] = strip_after_comments(cell['source'])
    with io.open(args.out_fname, 'w') as f:
        nb_write(nb, f, NB_VERSION)


if __name__ == '__main__':
    main()
