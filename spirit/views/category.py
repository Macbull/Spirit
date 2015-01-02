# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404

from spirit.models.topic import Topic

from spirit.models.category import Category


def category_detail(request, pk, slug):
    category = get_object_or_404(Category.objects.visible(),
                                 pk=pk)

    if category.slug != slug:
        return HttpResponsePermanentRedirect(category.get_absolute_url())

    subcategories = Category.objects.visible().children(parent=category)
    topics = Topic.objects.unremoved().for_category(category=category)\
        .order_by('-is_globally_pinned', '-is_pinned', '-last_active')\
        .select_related('category')

    return render(request, 'spirit/category/category_detail.html', {'category': category,
                                                                    'subcategories': subcategories,
                                                                    'topics': topics})


class CategoryList(ListView):

    template_name = 'spirit/category/category_list.html'
    context_object_name = "categories"
    queryset = Category.objects.visible().parents()
