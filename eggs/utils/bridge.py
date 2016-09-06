# -*- coding: utf-8 -*-

import platform
import subprocess
import chardet


class Bridge(object):
    """
    The class especially handle to executing casperjs command with javascript file.
    Note to avoid echo content variable of python to javascript file that casperjs command executing,
    because programmer is hovered or could't continue to continuously run.
    """
    def __init__(self, cmd):
        self._command = cmd
        self._stdout_path = 'd:/temp/data/pipe/stdout.txt'
        self._stderr_path = 'd:/temp/data/pipe/stderr.txt'

    @property
    def value(self):
        return ''.join(self._command_run())

    def _command_run(self):
        """ Don't use some os commands like `cmd` to start `dos`, or it's infinite loop. """
        # `casperjs` used for base data that write temporary file from web page
        # which don't need to echo content, because of too much data

        # child = subprocess.Popen(self._command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # could use `communicate` function fetch `stdout` and `stderr` data to avoid pipe block
        # could use file descriptor instead of `subprocess.PIPE`
        fd_out, fd_err = open(self._stdout_path, 'w'), open(self._stderr_path, 'w')
        child = subprocess.Popen(self._command, shell=True, stdout=fd_out, stderr=fd_err)
        child.wait()  # program will continue until wait for sub process finished
        fd_out.close()

        with open(self._stdout_path) as fd_out_read:
            for each_echo in fd_out_read:
                yield each_echo
        fd_err.close()


if __name__ == '__main__':
    # print Bridge(r'casperjs D:\project\autumn\crawler\casperjs_test\block_trade_with_date.js '
    #              r'--st_date=2012-8-31 --ed_date=2012-8-31 --outfile=2012-8-31').value

    print Bridge('ping').value
