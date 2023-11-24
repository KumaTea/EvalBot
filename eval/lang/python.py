from common.data import *
from eval.docker import get_output_files


def create_bash_script(ct_name: str, python_file: str) -> str:
    out, err, stat, exit_sign = get_output_files(ct_name, real_path=False)
    command = (
        '/usr/bin/time -v '
        f'-o {stat} '
        f'python3 {python_file} '
        f'1>{out} '
        f'2>{err}'
        f'\n'
        f'touch {exit_sign}'
    )
    filename = f'{SHM}/{ct_name}.sh'
    real_filename = f'{SHM}/{ct_name}/{ct_name}.sh'
    with open(real_filename, 'w', encoding='utf-8') as f:
        f.write(command)
    return filename
