from argparse import ArgumentParser


import re


def lineinfile(path, state='present', line=None, regex=None, create=False, **kwargs):
    """
    Python version of the ansible lineinfile module.
    See https://docs.ansible.com/ansible/latest/modules/lineinfile_module.html
    :param str path: Name of the file that should be managed
    :param str state: State of the line in the file. Should be either 'present'
    or 'absent'
    :param str line: Line that should be managed in the file. Doesn't go together
    with the regex parameter.
    :param str regex: Pattern to look for in the file. Doesn't go together with
    the line parameter
    :param bool create: Whether or not to create the file if it doesn't exist yet
    :return str: New content of the file
    """
    validate_lineinfile_input(line=line, regex=regex, state=state)

    # Get all current lines
    try:
        with open(path, 'r') as fp:
            current_contents = fp.read()
    except FileNotFoundError as e:
        if create:
            current_contents = ""
        else:
            raise e
    lines = current_contents.split("\n")

    if regex and state is 'absent':
        newlines = remove_line(lines, regex=regex)
    elif line and state is 'absent':
        newlines = remove_line(lines, line=line)
    elif regex and state is 'present':
        newlines = replace_line(lines, regex=regex, line=line)
    elif not regex and state is 'present':
        newlines = add_line(lines, line=line)
    else:
        raise AssertionError("Undefined behaviour for lineinfile. Args: path={}, state={}, line={}, regex={}".
                             format(path, state, line, regex))

    new_filecontents = "\n".join(newlines)

    # Write new lines to file
    with open(path, 'w') as fp:
        fp.write(new_filecontents)

    return new_filecontents


def validate_lineinfile_input(line, regex, state):
    """
    Check if the given input is valid for the lineinfile function.
    Raise AssertionError if input is invalid.
    :param str line: Line that should be managed in the file. Doesn't go together
    with the regex parameter.
    :param str regex: Pattern to look for in the file. Doesn't go together with
    the line parameter
    :param str state: State of the line in the file. Should be either 'present'
    or 'absent'
    :rtype: None|AssertionError
    """
    if state not in ['present', 'absent']:
        raise AssertionError('State should be either present or absent')

    if not (line or regex):
        raise AssertionError("Need to have at least one of line or regex parameter in lineinfile")

    if regex and line and state is 'absent':
        raise AssertionError("Unclear behaviour for state absent on both regex and line")

    if not line and state is 'present':
        raise AssertionError("Line is required if state is present")


def remove_line(lines, line=None, regex=None):
    """
    Remove line from file.
    :param list[str, ..] lines: Lines that are currently in the file.
    :param str line: Line that should be managed in the file. Doesn't go together
    with the regex parameter.
    :param str regex: Pattern to look for in the file. Doesn't go together with
    the line parameter
    :return: Lines that remain in the file
    """
    if line:
        delete_line = line
    else:
        delete_line = find_matching_line(lines, regex)
    if delete_line in lines:
        lines.remove(delete_line)
    return lines


def add_line(lines, line=None, index=None):
    """
    Add line to the file at the specified index. If index is not specified,
    line will be appended at the end of the list.
    :param list[str, ..] lines: Lines that are currently in the file.
    :param str line: Line that should be added.
    :param int|None index: Add line to this specific index.
    :return: Lines with the newly added line.
    """
    if line not in lines:
        if index:
            lines.insert(index, line)
        else:
            lines.append(line)
    return lines


def replace_line(lines, line, regex):
    """
    Replace line that matches the regex with the given line. Will add the line
    at the end of the file if no line matches the regex pattern.
    :param list[str, ..] lines: Lines that are currently in the file.
    :param str line: Line that should be managed in the file. Doesn't go together
    with the regex parameter.
    :param str regex: Pattern to look for in the file. Doesn't go together with
    the line parameter
    :return: Lines with the replaced line.
    """
    delete_line = find_matching_line(lines, regex)
    index = None
    if delete_line:
        index = lines.index(delete_line)
        lines = remove_line(lines, line=delete_line)
    lines = add_line(lines, line=line, index=index)
    return lines


def find_matching_line(lines, regex):
    """
    Find the first line that matches the given pattern.
    Returns None if no strings match the line
    :param list[str, ..] lines: Lines that are currently in the file.
    :param str regex: Regex file that should match a line.
    :rtype: str|None
    """
    pattern = re.compile(regex)
    for l in lines:
        if pattern.search(l):
            return l


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
