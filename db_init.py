import typer
from db.base import init_models
import asyncio
from db.models import *



# db init
cli = typer.Typer()
@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")
if __name__ == "__main__":
    cli()

