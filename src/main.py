from argparse import ArgumentParser


def lineinfile(path, state='present', line=None, **kwargs):
    try:
        with open(path, 'r') as fp:
            current_contents = fp.read()
    except FileNotFoundError as e:
        if kwargs['create']:
            current_contents = ""
        else:
            raise e
    lines = current_contents.split("\n")
    if state == 'present':
        lines.append(line)
    else:
        lines.remove(line)

    new_contents = "\n".join(lines)
    with open(path, 'w') as fp:
        fp.write(new_contents)
    return new_contents


def parse_args(args=None):
    parser = ArgumentParser("Replace lines in a file like the src Ansible module")
    parser.add_argument('path', help='Path to the file that will be changed')
    parser.add_argument('--regex', help='Pattern to look for to be replaced')
    parser.add_argument('--line', help='Line to place or remove')
    parser.add_argument('--state', help='Line to place or remove', choices=['present', 'absent'], default='present')
    parser.add_argument('--create', help='Create the file if it doesn\'t exist yet', action='store_true')

    return parser.parse_args(args)


def main():
    args = parse_args()
    lineinfile(**vars(args))
