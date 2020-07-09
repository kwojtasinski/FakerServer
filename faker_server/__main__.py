""" main module to run server """
import click
import dotenv
import uvicorn

dotenv.load_dotenv()


@click.command()
@click.option(
    "--host", type=str, envvar="FAKER_SERVER_HOST", help="Host for the server"
)
@click.option(
    "--port", type=int, envvar="FAKER_SERVER_PORT", help="Port for the server"
)
def run(host: str, port: int):
    """ function to run server
        :param host: host for the server
        :type host: str
        :param port: port for the server
        :type port: int
    """
    uvicorn.run("server:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    run()
