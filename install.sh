#!/bin/bash

MYDIR=$(realpath $(dirname $0))
cd "${MYDIR}"

if [ ! -e ./.env ]; then
  echo "Installing .env file"
cat  <<EOT > ./.env
ZONEID=ABC1234567890
RECORD=mydnsrecord.mydomain.com.
AWS_ACCESS_KEY=AK1234567890
AWS_SECRET_KEY=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
EOT
  chmod 0600 ./.env
else
  echo "Not overwriting existing .env file"
fi

if [ ! -e ./venv ]; then
  echo "Creating virtual python env"
  virtualenv ./venv
  ./venv/bin/pip install -r requirements.txt
else
  echo "virtual python env already exists"
fi

if [ -d /etc/cron.d ]; then
  if [ ! -e /etc/cron.d/update-ddns ]; then
    echo "Creating cron job"
    echo "*/15 * * * * root ${MYDIR}/venv/bin/python install.sh" > /etc/cron.d/update-ddns
  else
    echo "Cron job already exists."
  fi
else
  echo "No /etc/cron.d directory. Not creating cron job."
fi