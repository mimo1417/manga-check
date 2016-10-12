#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: vietvu
# @Date:   2016-10-11 17:55:03
# @Last Modified by:   Viet Vu
# @Last Modified time: 2016-10-12 11:04:31
from manga_check.crawler import MangaCrawler
from manga_check.config import DATA_FILE, MANGAS
import webbrowser
import click
import os
import csv


@click.group(invoke_without_command=True)
@click.option('--web/--no-web', default=False, help='Open web browser on updated chapter')
@click.pass_context
def commands(ctx, web):
    ctx.obj['web'] = web
    if ctx.invoked_subcommand is None:
        ctx.invoke(check)
    else:
        pass


@commands.command()
@click.pass_context
def check(ctx):
    """Check for latest manga chapter!"""
    crawler = MangaCrawler()
    updated_chapter = crawler.check()
    if updated_chapter:
        for manga in updated_chapter:
            click.echo("New chapter: {}-{}".format(manga['name'], manga['latest']))
            if ctx.obj['web']: webbrowser.open(manga['url'])
    else:
        click.echo("There are no new chapter")

@commands.command()
def clean():
    """Remove local data file"""
    try:
        os.remove(DATA_FILE)
        click.echo("File {} deleted".format(DATA_FILE))
    except OSError as e:
        click.echo("Cannot delete file {}".format(DATA_FILE))

@commands.command()
def show():
    """Show local data"""
    try:
        reader = csv.reader(open(DATA_FILE, 'rb'))
        click.echo("File {}:".format(DATA_FILE))
        for row in reader:
            click.echo("{}: {}".format(MANGAS[int(row[0])]['name'], row[1]))
    except IOError:
        click.echo("File {} not exist".format(DATA_FILE))

if __name__ == '__main__':
    commands(obj={})
