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
     aggregatetype varchar(255),
     aggregateid varchar(255),
     payload jsonb,
     create_time TIMESTAMPTZ NOT NULL DEFAULT now()
   );
    
    -- Drop existing slot if exists and recreate
    SELECT pg_drop_replication_slot('transaction_cdc') WHERE EXISTS (SELECT 1 FROM pg_replication_slots WHERE slot_name = 'transaction_cdc');
    SELECT pg_create_logical_replication_slot('transaction_cdc', 'pgoutput');
    
    -- Drop publication if exists and recreate
    DROP PUBLICATION IF EXISTS dbz_publication;
    CREATE PUBLICATION dbz_publication FOR TABLE events;
EOSQL
