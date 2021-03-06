#!/bin/python3
import os
import re
import psutil
from cmd import run_cmd

class NVLog(dict):

    __indent_re__ = re.compile('^ *')
    __version_re__ = re.compile(r'v([0-9.]+)$')

    def __init__(self):
        super().__init__()

        lines = run_cmd(['nvidia-smi', '-q'], silent=True)
        lines = lines.split('\n')
        while '' in lines:
            lines.remove('')

        path = [self]
        self['version'] = self.__version__()
        for line in lines[1:]:
            indent = NVLog.__get_indent__(line)
            line = NVLog.__parse_key_value_pair__(line)
            while indent < len(path) * 4 - 4:
                path.pop()
            cursor = path[-1]
            if len(line) == 1:
                if line[0] == 'Processes':
                    cursor[line[0]] = []
                else:
                    cursor[line[0]] = {}
                cursor = cursor[line[0]]
                path.append(cursor)
            elif len(line) == 2:
                if line[0] == 'Process ID':
                    cursor.append({})
                    cursor = cursor[-1]
                    path.append(cursor)
                cursor[line[0]] = line[1]

        self['Attached GPUs'] = {}
        keys = list(self.keys())
        for i in keys:
            if i.startswith('GPU '):
                self['Attached GPUs'][i] = self[i]
                del self[i]

    @staticmethod
    def __get_indent__(line):
        return len(NVLog.__indent_re__.match(line).group())

    @staticmethod
    def __parse_key_value_pair__(line):
        result = line.split(' : ')
        result[0] = result[0].strip()
        if len(result) > 1:
            try:
                result[1] = int(result[1])
            except:
                pass
            if result[1] in ['N/A', 'None']:
                result[1] = None
            if result[1] in ['Disabled', 'No']:
                result[1] = False
        return result

    def __get_processes__(self):
        processes = []
        for i, gpu in enumerate(self['Attached GPUs']):
            gpu = self['Attached GPUs'][gpu]
            if gpu['Processes']:
                for j in gpu['Processes']:
                    processes.append((i, j))
        return processes

    def __version__(self):
        lines = run_cmd(['nvidia-smi', '-h'], silent=True)
        lines = lines.split('\n')
        result = NVLog.__version_re__.search(lines[0]).group(1)
        return result

    def gpu_table(self):
        output = []
        output.append(self['Timestamp'])
        output.append('+-----------------------------------------------------------------------------+')
        values = []
        values.append(self['version'])
        values.append(self['Driver Version'])
        if 'CUDA Version' in self:
            values.append(self['CUDA Version'])
        else:
            values.append('N/A')
        output.append('| NVIDIA-SMI %s       Driver Version: %s       CUDA Version: %-5s    |' % tuple(values))
        output.append('|-------------------------------+----------------------+----------------------+')
        output.append('| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |')
        output.append('| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |')
        output.append('|===============================+======================+======================|')
        for i, gpu in enumerate(self['Attached GPUs']):
            gpu = self['Attached GPUs'][gpu]
            values = []
            values.append(i)
            values.append(gpu['Product Name'])
            values.append('On' if gpu['Persistence Mode'] else 'Off')
            values.append(gpu['PCI']['Bus Id'])
            values.append('On' if gpu['Display Active'] else 'Off')
            output.append('|   %d  %-19s %3s  | %s %3s |                  N/A |' % tuple(values))
            values = []
            values.append(gpu['Fan Speed'].replace(' ', ''))
            values.append(gpu['Temperature']['GPU Current Temp'].replace(' ', ''))
            values.append(gpu['Performance State'])
            values.append(int(float(gpu['Power Readings']['Power Draw'][:-2])))
            values.append(int(float(gpu['Power Readings']['Power Limit'][:-2])))
            values.append(gpu['FB Memory Usage']['Used'].replace(' ', ''))
            values.append(gpu['FB Memory Usage']['Total'].replace(' ', ''))
            values.append(gpu['Utilization']['Gpu'].replace(' ', ''))
            values.append(gpu['Compute Mode'])
            output.append('| %3s   %3s    %s   %3dW / %3dW |  %8s / %8s |    %4s     %8s |' % tuple(values))
            output.append('+-----------------------------------------------------------------------------+')
        return '\n'.join(output)

    def processes_table(self):
        output = []
        output.append('+-----------------------------------------------------------------------------+')
        output.append('| Processes:                                                       GPU Memory |')
        output.append('|  GPU       PID   Type   Process name                             Usage      |')
        output.append('|=============================================================================|')
        processes = self.__get_processes__()
        if len(processes) == 0:
            output.append('|  No running processes found                                                 |')
        for i, process in processes:
            values = []
            values.append(i)
            values.append(process['Process ID'])
            values.append(process['Type'])
            if len(process['Name']) > 42:
                values.append(process['Name'][:39] + '...')
            else:
                values.append(process['Name'])
            values.append(process['Used GPU Memory'].replace(' ', ''))
            output.append('|   %2d     %5d %6s   %-42s %8s |' % tuple(values))
        output.append('+-----------------------------------------------------------------------------+')
        return '\n'.join(output)

    def as_table(self):
        output = []
        output.append(self.gpu_table())
        output.append('')
        output.append(self.processes_table())
        return '\n'.join(output)

class NVLogPlus(NVLog):

    def processes_table(self):
        output = []
        output.append('+-----------------------------------------------------------------------------+')
        output.append('| Processes:                                                       GPU Memory |')
        output.append('|  GPU       PID   User   Process name                             Usage      |')
        output.append('|=============================================================================|')
        processes = self.__get_processes__()
        if len(processes) == 0:
            output.append('|  No running processes found                                                 |')
        for i, process in processes:
            values = []
            values.append(i)
            values.append(process['Process ID'])
            p = psutil.Process(process['Process ID'])
            with p.oneshot():
                values.append(p.username()[:8].center(8))
                command = p.cmdline()
                command[0] = os.path.basename(command[0])
                command = ' '.join(command)
                if len(command) > 42:
                    values.append(command[:39] + '...')
                else:
                    values.append(command)
            values.append(process['Used GPU Memory'].replace(' ', ''))
            output.append('|   %2d     %5d %8s %-42s %8s |' % tuple(values))
        output.append('+-----------------------------------------------------------------------------+')
        return '\n'.join(output)

if __name__ == '__main__':
    import json
    log = NVLogPlus()
    #print(json.dumps(log, indent=2))
    print(log.as_table())
