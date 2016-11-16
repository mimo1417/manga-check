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
import traceback

DEBUG=True


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
            click.echo("[{}] New chapter: {}-{}".format(manga['id'],
                                                        manga['name'], manga['latest']))
            if ctx.obj['web']:
                webbrowser.open(manga['url'])
    else:
        click.echo("There is no new chapter")


@commands.command()
def clean():
    """Remove local data file"""
    try:
        os.remove(DATA_FILE)
        click.echo("File {} deleted".format(DATA_FILE))
    except OSError as e:
        click.echo("Cannot delete file {}".format(DATA_FILE))
        if DEBUG: click.echo(traceback.format_exc())


@commands.command()
def show():
    """Show local data"""
    with open(DATA_FILE) as csvfile:
        reader = csv.reader(csvfile)
        click.echo("Showing file {}:".format(DATA_FILE))
        for row in reader:
            id = int(row[0])
            click.echo("[{}] {}: {}".format(
                MANGAS[id]['id'], MANGAS[id]['name'], row[1]))

@commands.command()
@click.argument('id')
def web(id):
    """Open web with ID provided"""
    try:
        id = int(id)
        if not id in MANGAS:
            raise ValueError
        manga = MANGAS[id]
        with open(DATA_FILE) as csvfile:
            file_data = csv.reader(csvfile)
            latest_data = dict((int(row[0]), int(row[1])) for row in file_data)
        click.echo("Opening {} at {}".format(manga['name'],manga['url']))
        webbrowser.open("{}/{}".format(manga['url'], latest_data[id]))
    except ValueError as e:
        click.echo("ID not invalid: {}, need to be a number in config. see show command".format(id))
    except:
        click.echo("Something wrong")
        if DEBUG: click.echo(traceback.format_exc())

if __name__ == '__main__':
    commands(obj={})
