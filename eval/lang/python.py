from common.data import *
from eval.docker import get_output_files


def create_bash_script(ct_name: str, python_file: str) -> str:
    out, err, stat = get_output_files(ct_name)
    command = (
        '/usr/bin/time -v '
        f'-o {stat} '
        f'python {python_file} '
        f'1>{out} '
        f'2>{err}'
    )
    filename = f'{SHM}/{ct_name}.sh'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(command)
    return filename
