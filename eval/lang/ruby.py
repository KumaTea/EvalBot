from eval.lang.common import create_lang_script


def create_bash_script(ct_name: str, ruby_file: str) -> str:
    return create_lang_script(
        ct_name=ct_name,
        code_file=ruby_file,
        lang_executor='ruby',
    )
