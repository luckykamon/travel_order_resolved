#!/bin/sh

# This script is used to start, restart, stop the application and run the tests

detached_text="-d "
if [ "$2" = "--dev" ]; then
    echo "Using the development environment"
    
    detached_text=""
fi

if [ "$1" = "start" ]; then
    echo "Starting the application"

    # Start the application
    docker-compose --env-file .env up $detached_text --build 
elif [ "$1" = "stop" ]; then
    echo "Stopping the application"

    # Stop the application
    docker-compose --env-file .env down
elif [ "$1" = "restart" ]; then
    echo "Restarting the application"

    # Restart the application
    ./app.sh stop $2

    sleep 1

    ./app.sh start $2
elif [ "$1" = "test" ]; then
    if [ "$(docker ps -q -f name=bdd_api)" ]; then
        echo "Running the tests"

        # Run the tests
        docker exec -it -w /app bdd_api pytest
    else
        echo "Run the application before running the tests"
    fi
else
    echo "Usage: $0 {start|stop|restart|test} [--dev]"
fi