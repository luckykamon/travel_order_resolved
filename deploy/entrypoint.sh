#!/bin/sh

set -eu

export GITHUB="true"

/bin/drone-ssh --username ubuntu --password QAYxupCRSqkf --host 51.255.173.25 --script "cd T-AIA-901-REN_1/ &&
                                                                                        git pull origin main &&
                                                                                        docker-compose down &&
                                                                                        docker-compose build &&
                                                                                        docker-compose up -d &&
                                                                                        curl localhost:8000 &&
                                                                                        python3 add_column.py"