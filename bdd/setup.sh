#!/bin/sh

echo "Setting up the environment for the BDD tests"

if [ -f ".env" ]; then
    echo "Create environnement file"
    cp .env.example .env
elif 
    echo "Environnement file already exists"
fi