FROM postgres:13.3-alpine

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=MoonStorm1
ENV POSTGRES_DB=proxy_checker

COPY create_database.sql /docker-entrypoint-initdb.d/
COPY create_table.sql /docker-entrypoint-initdb.d/
COPY create_users.sql /docker-entrypoint-initdb.d/
