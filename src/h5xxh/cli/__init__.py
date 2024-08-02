# SPDX-FileCopyrightText: 2024-present S. Miccoli <stefano.miccoli@polimi.it>
#
# SPDX-License-Identifier: MIT
import sys

import click
import h5py

from h5xxh import Walker
from h5xxh.__about__ import __version__


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="h5xxh")
@click.argument("h5", nargs=-1)
def h5xxh(h5):
    for pth in h5:
        try:
            msg = data_hash(pth)
        except FileNotFoundError:
            click.secho(f"{pth}: not found", file=sys.stderr, fg="red")
        except OSError as err:
            click.secho(f"{pth}: {err}", file=sys.stderr, fg="red")
        else:
            click.echo(f"{msg}  {pth}")


def data_hash(pth):
    callback = Walker()
    with h5py.File(pth, "r") as h5:
        h5.visititems(callback)
    return callback.hexdigest
