# -- coding: utf-8 --
import click
import socket
from extensions import EXTENSIONS

def check_availability(query, extension, **options):
    domain = "%s.%s" % (query, extension) if extension else query

    try:
        socket.gethostbyname(domain)
        return False
    except:
        return True


def search(query, **options):
    result = ""
    available_extensions = EXTENSIONS.split('|')

    # Loop only TLDs
    if options['tld']:
        available_extensions = "com|net|org".split('|')

    # Pass raw query to availability check
    if options['no_suggest']:
        status = check_availability(query, False)
        # Clean available extensions
        available_extensions = []
        message = "Available" if status else "Not Available"
        color = 'green' if status else 'red'
        click.echo(click.style(message, fg=color))


    for ext in available_extensions:
        status = check_availability(query, ext, **options)

        # Print only available and pass the unavailable domains
        if options['available'] and not status:
            continue

        # Async options
        new_line = "\n" if options['sync'] else "\r"

        # Color options
        color = "green" if status else "red"
        ascii_status = "+" if status else "x"

        # Color output
        ascii_output = "%s %s.%s%s" % (ascii_status, query, ext, new_line)
        color_output = "%s.%s%s" % (query, click.style(ext, fg=color), new_line)
        output = ascii_output if options['no_color'] else color_output

        # Async Output
        if not options['sync']:
            print output
        else:
            result += output

    if options['sync']:
        click.echo_via_pager(result)



@click.command()
@click.version_option()
@click.option(
    '--no-color',
    '-c',
    is_flag=True,
    help="Disable colorful output"
)
@click.option(
    '--available',
    '-a',
    is_flag=True,
    help="Show only available domains"
)
@click.option(
    '--no-suggest',
    '-n',
    is_flag=True,
    help="Search exact domain query."
)
@click.option(
    '--tld',
    '-t',
    is_flag=True,
    help="Show only top level domains. (.com, .net, .org)"
)
@click.option(
    '--sync',
    '-s',
    is_flag=True,
    help="Print domain names (with pager) once when query complete for each domain"
)
@click.argument('query')
def cli(no_color, available, no_suggest, tld, sync, query):
    "Domi - Terminal based quick domain search tool."
    options = {
        "no_color": no_color,
        "available": available,
        "no_suggest": no_suggest,
        "tld": tld,
        "sync": sync
    }
    click.echo(search(query, **options))


