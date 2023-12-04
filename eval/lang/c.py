from eval.lang.common import create_compile_script


def create_bash_script(ct_name: str, c_file: str) -> str:
    return create_compile_script(
        ct_name=ct_name,
        code_file=c_file,
        lang_compiler='gcc',
        arg_input='-Wall -O2',
        arg_output='-o',
        output_file=c_file.split('.')[0] + '.out',
    )
