#!/bin/sh

python3 -m restore_kanban_backup
/bin/sh -c "sleep 300"
curl -s -X POST localhost:10001/quitquitquit
