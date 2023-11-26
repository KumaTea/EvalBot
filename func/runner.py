import time
import asyncio
import logging
from common.data import *
from func.tools import gen_result
from bot.session import msg_store, eval_bot
from pyrogram.types import Message
from eval.docker import run_docker, container_exited, clean_container, read_output_files, clean_files


async def read_and_finish(
        name: str,
        code_file: str,
        inform: Message,
        user_msg_id: int = None,
        timeout=False
) -> Message:
    output, error, statistic = read_output_files(name)
    result_text, parse_mode = gen_result(output, error, statistic, code_file)
    # logging.info(f'[func.runner run]\t{chat_id=} {name=} {result_text=}')
    if timeout:
        text = f'{TIMEOUT}\n{result_text}'
    else:
        text = result_text
    inform, _ = await asyncio.gather(
        inform.edit_text(text, parse_mode=parse_mode),
        clean_container(name)
    )
    if user_msg_id:
        # since this operation finished, we can store this conversation's ids
        msg_store.add(chat_id=inform.chat.id, user_msg_id=user_msg_id, bot_msg_id=inform.id)
    clean_files(name)
    return inform


async def post_process(
        limits: dict,
        name: str,
        image: str,
        chat_id: int,
        code_file: str,
        inform: Message,
        user_msg_id: int = None,
) -> Message:
    t0 = time.time()
    creation_informed = False

    while time.time() - t0 < limits['timeout']:
        await asyncio.sleep(1)

        if container_exited(name):
            logging.info(f'[func.runner post_process]\t{chat_id=} {name=} exited')
            inform = await read_and_finish(name, code_file, inform, user_msg_id=user_msg_id)
            return inform
        else:
            if not creation_informed and time.time() - t0 > 5:
                creation_informed = True
                logging.info(f'[func.runner post_process]\t{chat_id=} {name=} creation_informed')
                await inform.edit_text(RUNNING.format(IMAGE=image))

    # timeout
    inform = await read_and_finish(name, code_file, inform, user_msg_id=user_msg_id, timeout=True)
    return inform


async def run(
        message: Message,
        command: str,
        name: str,
        image: str,
        code_file: str = None,
) -> Message:
    chat_id = message.chat.id
    trusted = chat_id in trusted_group
    limits = TRUSTED_LIMITS if trusted else DOCKER_LIMITS
    logging.info(f'[func.runner run]\t{chat_id=} {trusted=} {name=} {image=} {command=}')

    inform, _ = await asyncio.gather(
        message.reply_text(CREATING.format(IMAGE=image), quote=False),
        run_docker(
            name=name,
            image=image,
            cmd=command,
            cpu=limits['cpu'],
            memory=limits['memory'],
            shm_size=limits['shm_size'],
            read_only=limits['read_only'],
            disk_quota=limits['disk_quota'],
            no_net=limits['no_net'],
        )
    )

    return await post_process(
        limits=limits,
        name=name,
        image=image,
        chat_id=chat_id,
        code_file=code_file,
        inform=inform,
        user_msg_id=message.id,
    )


async def edit_run(
        message: Message,
        inform_id: int,
        command: str,
        name: str,
        image: str,
        code_file: str = None,
) -> Message:
    chat_id = message.chat.id
    trusted = chat_id in trusted_group
    limits = TRUSTED_LIMITS if trusted else DOCKER_LIMITS
    logging.info(f'[func.runner run]\t{chat_id=} {trusted=} {name=} {image=} {command=}')

    inform, _ = await asyncio.gather(
        eval_bot.edit_message_text(chat_id, inform_id, CREATING.format(IMAGE=image)),
        run_docker(
            name=name,
            image=image,
            cmd=command,
            cpu=limits['cpu'],
            memory=limits['memory'],
            shm_size=limits['shm_size'],
            read_only=limits['read_only'],
            disk_quota=limits['disk_quota'],
            no_net=limits['no_net'],
        )
    )

    return await post_process(
        limits=limits,
        name=name,
        image=image,
        chat_id=chat_id,
        code_file=code_file,
        inform=inform,
        user_msg_id=message.id,
    )
