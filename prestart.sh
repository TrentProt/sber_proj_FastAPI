#!/usr/bin/env bash

set -e

echo "Run migration"
alembic upgrade head
echo "Migration applied"

exec "$@"