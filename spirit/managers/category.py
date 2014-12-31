# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404


class CategoryQuerySet(models.QuerySet):

    def for_public(self):
        return self.filter(Q(parent=None) | Q(parent__is_removed=False),
                           is_removed=False,
                           is_private=False)

    def for_public_open(self):
        return self.for_public()\
            .filter(Q(parent=None) | Q(parent__is_closed=False),
                    is_closed=False)

    def for_parent(self, parent=None):
        if parent and parent.is_subcategory:
            return self.none()
        else:
            return self.filter(parent=parent,
                               is_removed=False,
                               is_private=False)

    def get_public_or_404(self, pk):
        return get_object_or_404(self.for_public(),
                                 pk=pk)
