#!/bin/sh

set -eu

export GITHUB="true"

/bin/drone-ssh --username ubuntu --command.timeout 100m0s --password QAYxupCRSqkf --host 51.255.173.25 --script "cd T-AIA-901-REN_1/ &&
                                                                                                                 git pull origin main &&
                                                                                                                 docker-compose down &&
                                                                                                                 docker-compose build &&
                                                                                                                 docker-compose up -d &&
                                                                                                                 sleep 2 &&
                                                                                                                 curl localhost:8000/build &&
                                                                                                                 python3 add_column.py"