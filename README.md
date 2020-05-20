# AMQP Content Router

## Synopsis

As Rabbit doensn't support content-based routing natively, this service can be used to use content-based routing.
The service connects to a queue and parses the incoming messages. 
Based on the root-tag in the message, the message gets published with a new routing key.
Currently only XML messages are supported and only the root tag gets parsed.

## Prerequisites

- Git
- Docker
- Python 3.6+
- Access to the [meemoo PyPi](http://do-prd-mvn-01.do.viaa.be:8081)

## Usage

1. Clone this repository with:

   `$ git clone https://github.com/viaacode/amqp-content-router.git`

2. Change into the new directory.

### Running locally

**Note**: As per the aforementioned requirements, this is a Python3
application. Check your Python version with `python --version`. You may want to
substitute the `python` command below with `python3` and if your Python version
is < 3.

1. Start by creating a virtual environment:

    `$ python -m venv env`

2. Activate the virtual environment:

    `$ source env/bin/activate`

3. Install the external modules:

    ```
    $ pip install -r requirements.txt \
        --extra-index-url http://do-prd-mvn-01.do.viaa.be:8081/repository/pypi-all/simple \
        --trusted-host do-prd-mvn-01.do.viaa.be
    ```
4. Set the needed config and environment variables:

    Included in this repository is a `config.yml.example` file. 
    All values in the config have to be set in order for the application to function correctly.
    You can use `!ENV ${EXAMPLE}` as a config value to make the application get the `EXAMPLE` environment variable.

5. Run the tests with:

    `$ pytest -v`

6. Run the application:

    `$ python main.py`


### Running using Docker

1. Build the container:

   `$ docker build -t amqp-content-router .`

2. Run the container (with specified `.env` file):

   `$ docker run --env-file .env amqp-content-router:latest`

