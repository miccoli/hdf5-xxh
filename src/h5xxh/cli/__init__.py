# SPDX-FileCopyrightText: 2024-present S. Miccoli <stefano.miccoli@polimi.it>
#
# SPDX-License-Identifier: MIT
import click

from h5xxh.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="h5xxh")
def h5xxh():
    click.echo("Hello world!")
