from pyrogram.enums.parse_mode import ParseMode


def gen_output(output: str, limit: int = 2000):
    if len(output) > limit:
        notify = f'(too long! Last {limit} chars are shown)'
        count = len(notify) + 1
        out = []
        for line in reversed(output.splitlines()):
            if count + len(line) + 1 < limit:
                out.insert(0, line)
                count += len(line) + 1
            else:
                break
        out.insert(0, notify)
        output = '\n'.join(out)
    return output


def wrap_code(text: str, long=True):
    if long:
        if '```' in text:
            result = f'<pre language="log">\n{text}\n</pre>'
            parse_mode = ParseMode.HTML
        else:
            result = f'```log\n{text}\n```'
            parse_mode = ParseMode.MARKDOWN
    else:
        if '`' in text:
            result = f'<code>{text}</code>'
            parse_mode = ParseMode.HTML
        else:
            result = f'`{text}`'
            parse_mode = ParseMode.MARKDOWN
    return result, parse_mode


def gen_result(output, error, statistic, code_file=None):
    result_text = ''
    output_parse_mode = None
    error_parse_mode = None
    if output:
        text = gen_output(output)
        is_long = len(output.splitlines()) > 3
        code, output_parse_mode = wrap_code(text, long=is_long)
        result_text += code
    if error:
        result_text += '\nERROR:\n'
        if code_file:
            error = error.replace(code_file, '[code]')
        text = gen_output(error)
        is_long = len(error.splitlines()) > 3
        code, error_parse_mode = wrap_code(text, long=is_long)
        result_text += code

    if not result_text:
        result_text = '`(no output)`'
        parse_mode = ParseMode.MARKDOWN
    else:
        if output and error:
            parse_mode = output_parse_mode if output_parse_mode == error_parse_mode else ParseMode.DISABLED
        else:
            parse_mode = output_parse_mode or error_parse_mode or ParseMode.DEFAULT

    # fix stat later
    return result_text, parse_mode
