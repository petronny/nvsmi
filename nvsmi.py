#!/bin/python3
import re
from cmd import run_cmd

class NVSMI_LOG(dict):

    __indent_re__ = re.compile('^ *')
    __tailing_spaces_re__ = re.compile(' *$')

    def __init__(self):
        super().__init__()

        lines = run_cmd(['nvidia-smi', '-q'], silent=True)
        lines = lines.split('\n')
        while '' in lines:
            lines.remove('')

        path = [self]
        for line in lines[1:]:
            indent = NVSMI_LOG.__get_indent__(line)
            line = NVSMI_LOG.__parse_key_value_pair__(line)
            while indent < len(path) * 4 - 4:
                path.pop()
            cursor = path[-1]
            if len(line) == 1:
                cursor[line[0]] = {}
                cursor = cursor[line[0]]
                path.append(cursor)
            elif len(line) == 2:
                cursor[line[0]] = line[1]

    @staticmethod
    def __get_indent__(line):
        return len(NVSMI_LOG.__indent_re__.match(line).group())

    @staticmethod
    def __parse_key_value_pair__(line):
        result = line.split(' : ')
        result[0] = NVSMI_LOG.__indent_re__.sub('', result[0])
        result[0] = NVSMI_LOG.__tailing_spaces_re__.sub('', result[0])
        try:
            result[1] = int(result[1])
        except:
            pass
        return result

if __name__ == '__main__':
    import json
    log = NVSMI_LOG()
    print(json.dumps(log, indent=2))
