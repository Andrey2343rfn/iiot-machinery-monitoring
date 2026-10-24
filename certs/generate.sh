#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

openssl req -new -x509 -days 365 -nodes -out ca.crt -keyout ca.key -subj "/CN=IoT-CA"

openssl genrsa -out broker.key 2048
openssl req -new -key broker.key -out broker.csr -subj "/CN=mosquitto"
openssl x509 -req -in broker.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out broker.crt -days 365

chmod 644 ca.crt broker.crt
chmod 600 ca.key broker.key