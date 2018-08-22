import sys

import click


class Kubeb(object):

    def log(self, msg, *args):
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

pass_kubeb = click.make_pass_decorator(Kubeb)