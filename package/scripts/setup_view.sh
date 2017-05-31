#!/bin/bash

set -e

export INSTALL_DIR=$1
export MIST_HOST=$2
export MIST_PORT=$3
export SETUP_VIEW=$4
export PACKAGE_DIR=$5
export java64_home=$6

SETUP_VIEW=${SETUP_VIEW,,}
echo "SETUP_VIEW is $SETUP_VIEW"

SetupMist () {

    echo "Setting up Snapshot at $INSTALL_DIR"
    cd $INSTALL_DIR
        if [[ $SETUP_VIEW == "true" ]]
        then
            cp $PACKAGE_DIR/scripts/ambari-proxied-mist-view-0.0.1.jar .
            $java64_home/bin/jar xf ambari-proxied-mist-view-0.0.1.jar view.xml

            sed -i "s/http:\/\/127.0.0.1:2004/http:\/\/$MIST_HOST:$MIST_PORT/g" view.xml
            $java64_home/bin/jar uf ambari-proxied-mist-view-0.0.1.jar view.xml
        else
            echo "Skipping setup of Ambari view"
        fi
        echo "Skipping setup of Ambari view"

    }

SetupMist
echo "Setup complete"
