from common.data import SHM
from eval.lang.common import create_lang_script


def create_bash_script(ct_name: str, sh_file: str) -> str:
    filename = f'{SHM}/{ct_name}.outer.sh'
    real_filename = f'{SHM}/{ct_name}/{ct_name}.outer.sh'
    return create_lang_script(
        ct_name=ct_name,
        code_file=sh_file,
        lang_executor='sh',
        filename=filename,
        real_filename=real_filename,
    )
