#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from manga_check.crawler import MangaCrawler
from manga_check.config import  MANGAS
from manga_check.storage import Storage

import webbrowser
import click
import os
import csv
import traceback

DEBUG = True


@click.group(invoke_without_command=True)
@click.option('--web/--no-web', default=False,
              help='Open web browser on updated chapter')
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
    crawler = MangaCrawler(logger=lambda msg: click.echo(msg))
    updated_chapter = crawler.check()
    if updated_chapter:
        for manga in updated_chapter:
            click.echo("[{}] New chapter: {}-{}".format(manga['id'],
                                                        manga['name'],
                                                        manga['latest']))
            if ctx.obj['web']:
                webbrowser.open("{}/{}".format(manga['url'], manga['latest']))
    else:
        click.echo("There is no new chapter")


@commands.command()
def clean():
    """Remove local data file"""
    storage = Storage()
    storage.clean()


@commands.command()
def show():
    """Show local data"""
    storage = Storage()

    data = storage.get()
    for row in data:
        id = int(row['id'])
        is_read_str = '[_]' if int(row['is_read']) == 0 else '[x]'
        click.echo("[{}] {} {}: {}".format(
            MANGAS[id]['id'], is_read_str, MANGAS[id]['name'], row['chapter']))


@commands.command()
@click.argument('id')
def web(id):
    """Open web with ID provided"""
    try:
        storage = Storage()
        id = int(id)
        if id not in MANGAS:
            raise ValueError
        manga = MANGAS[id]
        latest_data = dict((int(row['id']), int(row['chapter'])) for row in storage.get())
        click.echo("Opening {} at {}".format(manga['name'], manga['url']))
        webbrowser.open("{}/{}".format(manga['url'], latest_data[id]))
        crawler = MangaCrawler(logger=lambda msg: click.echo(msg))
        crawler.update_view_manga(id)
    except ValueError:
        click.echo(
            "ID not invalid: {}, need to be a number in config. \
            see show command".format(id))
    except Exception as e:
        click.echo("Something wrong: {}".format(e.messsage))
        if DEBUG:
            click.echo(traceback.format_exc())


@commands.command()
@click.argument('id')
def reddit(id):
    """Open reddit thread with ID provided"""
    try:
        id = int(id)
        if id not in MANGAS:
            raise ValueError
        manga = MANGAS[id]
        if 'reddit' not in manga:
            raise KeyError
        click.echo("Opening {} at {}".format(manga['name'], manga['reddit']))
        webbrowser.open("{}".format(manga['reddit']))
    except ValueError:
        click.echo(
            "ID not invalid: {}, need to be a number in config. \
            see show command".format(id))
    except KeyError:
        click.echo("Manga id={}, name={} don't have reddit page".format(
            manga['id'], manga['name']))
    except Exception as e:
        click.echo("Something wrong: {}".format(e.messsage))
        if DEBUG:
            click.echo(traceback.format_exc())


if __name__ == '__main__':
    commands(obj={})
