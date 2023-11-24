from common.data import *
from eval.docker import get_output_files


def create_lang_script(
        ct_name: str,
        code_file: str,
        lang_executor: str,
        filename: str = None,
        real_filename: str = None,
) -> str:
    out, err, stat, exit_sign = get_output_files(ct_name, real_path=False)
    command = (
        '/usr/bin/time -v '
        f'-o {stat} '
        f'{lang_executor} {code_file} '
        f'1>{out} '
        f'2>{err}'
        f'\n'
        f'touch {exit_sign}'
    )
    if not filename:
        filename = f'{SHM}/{ct_name}.sh'
    if not real_filename:
        real_filename = f'{SHM}/{ct_name}/{ct_name}.sh'
    with open(real_filename, 'w', encoding='utf-8') as f:
        f.write(command)
    return filename
