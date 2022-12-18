#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
     
    CREATE TABLE IF NOT EXISTS transactions (
     id uuid PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
     price decimal,
     status text NOT NULL,
     create_time TIMESTAMPTZ NOT NULL DEFAULT now()
   );
   
    CREATE TABLE IF NOT EXISTS events (
     id uuid PRIMARY KEY NOT NULL DEFAULT uuid_generate_v4(),
     event_type text,
     payload bytea,
     create_time TIMESTAMPTZ NOT NULL DEFAULT now()
   );

    SELECT pg_create_logical_replication_slot('transaction_cdc', 'pgoutput');
EOSQL
