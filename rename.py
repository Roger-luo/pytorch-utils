import fire
import os
import re
from tempfile import mktemp
import shutil


def rename(filename):
    temp = mktemp(suffix='.temp')
    with open(temp, "w+") as file_temp:
        with open(filename, "r+") as file:
            for line in file:
                line = re.sub(r'(?<!\.)(real)(?=[ ,\)*>;\.\n])', 'num', line)
                line = re.sub(r'(real)(?=\(&\))', 'num ', line)
                # enable types etc. for num
                line = re.sub(r'(real)(?=\')', 'num', line)
                line = re.sub(r'cnum', 'creal', line)
                line = re.sub(r'cnumf', 'crealf', line)
                line = re.sub(r'TH_MATH_NAME\(num\)',
                              'TH_MATH_NAME(real)', line)
                # replace REAL
                line = re.sub(r'TH_REAL_IS_REAL', 'TH_NUM_IS_REAL', line)
                line = re.sub(r'TH_CONVERT_REAL_TO_ACCREAL',
                              'TH_CONVERT_NUM_TO_ACCNUM', line)
                line = re.sub(r'TH_CONVERT_ACCREAL_TO_REAL',
                              'TH_CONVERT_ACCNUM_TO_NUM', line)
                line = re.sub(r'REAL_', 'NUM_', line)
                # replace Real
                line = re.sub(r'(Real)(?=[A-Z]*)', "Num", line)
                line = re.sub(r'NumTypes', 'RealTypes', line)
                line = re.sub(
                    r'(?<!\.)(accreal)(?=[ ,\)*>;\.\n])', 'accnum', line)
                line = re.sub(r'(accreal)(?=\(&\))', 'accnum', line)
                line = re.sub(r'(accreal)(?=\')', 'accnum', line)
                file_temp.write(line)
    os.remove(filename)
    shutil.copy(temp, filename)
    os.remove(temp)


def rename_files(root, files):
    for file in files:
        if re.search(r'.*.py|.*\.c|.*\.cc|.*\.h|.*\.hpp|.*\.cpp', file) \
                is not None:
            print(root + '/' + file)
            rename(root + '/' + file)


def rename_all(dirname):
    for root, dirs, files in os.walk(dirname):
        if re.search(r'\..*', root) is not None:
            pass
        elif re.search(r'build', root) is not None:
            pass
        elif re.search(r'__pycache__', root) is not None:
            pass
        else:
            rename_files(root, files)


if __name__ == '__main__':
    fire.Fire(rename_all)
