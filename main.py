#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: vietvu
# @Date:   2016-10-11 17:55:03
# @Last Modified by:   vietvu
# @Last Modified time: 2016-10-11 23:26:10
from manga_check.crawler import MangaCrawler
from manga_check.config import DATA_FILE
import webbrowser
import click
import os


@click.group(invoke_without_command=True)
@click.pass_context
def commands(ctx):
    if ctx.invoked_subcommand is None:
        check()
    else:
        pass


@commands.command()
def check():
    """Check for latest manga chapter!"""
    crawler = MangaCrawler()
    for manga in crawler.check():
        print("New chapter {}-{}".format(manga['name'], manga['latest']))
        # webbrowser.open(manga['url'])


@commands.command()
def clean():
    """Remove local data file"""
    try:
        os.remove(DATA_FILE)
        click.echo("File {} deleted".format(DATA_FILE))
    except OSError as e:
        click.echo("Cannot delete file {}".format(DATA_FILE))

# cli = click.CommandCollection(sources=[commands])

if __name__ == '__main__':
    commands()
