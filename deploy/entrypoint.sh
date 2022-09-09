#!/bin/sh

set -eu

export GITHUB="true"

/bin/drone-ssh --username ubuntu --password QAYxupCRSqkf --host 51.255.173.25 --script "cd T-DEV-800-T-DEV-800_msc2023_group-15/ &&
                                                                                        git pull origin master &&
                                                                                        docker-compose down &&
                                                                                        docker-compose build &&
                                                                                        docker-compose up -d"