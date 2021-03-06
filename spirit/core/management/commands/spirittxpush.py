# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from subprocess import call
import os

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Pushes all the local files listed in ./.tx/config to transifex'

    requires_system_checks = False

    def handle(self, *args, **options):
        # todo: test or not to test?
        # Requir python27 and "pip install transifex-client==0.11b3"
        root = os.path.split(settings.ST_BASE_DIR)[0]
        tx_dir = os.path.join(root, '.tx')

        if not os.path.isdir(tx_dir):
            raise CommandError('Can\'t find the .tx folder in %s' % (root, ))

        os.chdir(root)
        call(["tx", "push", "-s", "-t", "--skip"])
        self.stdout.write('ok')
