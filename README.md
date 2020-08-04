# FakerServer [in progress]

Python package to serve Faker package as a HTTP server

Please refer to https://faker.readthedocs.io/en/master/ for available fields to generate

It provides simple API to generate random data to consume by other services.

The most important endpoint is /api/v1/query (POST method).

For more please refer to auto-generated docs on how to generate the data (in root directory)

Currently FakerServer supports two environment variables:

FAKER_SERVER_HOST = "0.0.0.0"
FAKER_SERVER_PORT = 3000
