# coding: utf-8

# Copyright (c) 2019-2020 Latona. All rights reserved.

import os
import subprocess

from aion.microservice import main_decorator, Options
from aion.kanban import Kanban
from aion.logger import lprint, initialize_logger


SERVICE_NAME = os.environ.get("SERVICE", "restore-mongo-kanban-backup")
initialize_logger(SERVICE_NAME)


@main_decorator(SERVICE_NAME)
def main_with_kanban(opt: Options):
    lprint("start main_with_kanban()")
    # get cache kanban
    conn = opt.get_conn()
    num = opt.get_number()
    kanban = conn.get_one_kanban(SERVICE_NAME, num)

    # get output file_list
    metadata = kanban.get_metadata()
    file_name = metadata.get("file_name")
    data_path = kanban.get_data_path()
    backup_file = '/var/lib/aion/Data/restore-mongo-kanban-backup_1/'+file_name
    lprint(backup_file)

    ######### main function #############
    subprocess.run(['mongoimport', '-h', 'mongo', '--db', 'AionCore', 
        '--collection', 'kanban', '--file', backup_file])

    # output after kanban
    conn.output_kanban(
        result=True,
        connection_key="default"
    )

