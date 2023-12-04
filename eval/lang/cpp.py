from eval.lang.common import create_compile_script


def create_bash_script(ct_name: str, cpp_file: str) -> str:
    return create_compile_script(
        ct_name=ct_name,
        code_file=cpp_file,
        lang_compiler='g++',
        arg_input='-Wall -O2',
        arg_output='-o',
        output_file=cpp_file.split('.')[0] + '.out',
    )
