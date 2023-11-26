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


def create_compile_script(
        ct_name: str,
        code_file: str,
        lang_compiler: str,
        arg_input: str = '',
        arg_output: str = '',
        output_file: str = 'out',
        filename: str = None,
        real_filename: str = None,
        shell_executor: str = '/bin/bash',
) -> str:
    out, err, stat, exit_sign = get_output_files(ct_name, real_path=False)
    command = (
        '/usr/bin/time -v '
        f'-o {stat} '
        f'{shell_executor} -c '
        f'" '
        f'{lang_compiler} {arg_input} {code_file} {arg_output} {output_file} '
        f'1>>{out} 2>>{err} '
        f'&& '
        f'./{output_file} '
        f'1>>{out} 2>>{err} '
        f'"'
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
