from subprocess import check_output, CalledProcessError, STDOUT
import re

def version():
    try:
        tag_version = check_output(['git', 'describe'], stderr=STDOUT)
        return tag_version.decode().strip()
    except CalledProcessError:
        summary = check_output(['git', 'show', '-s'])
        version = re.search(r'^commit ([\da-f]+)', summary.decode())
        return version.group(1)

if __name__ == '__main__':
    print(version())
