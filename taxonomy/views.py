# -*- coding: utf-8 -*-
"""Taxonomy views."""
from __future__ import absolute_import, unicode_literals

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from taxonomy.filters import CommunityFilter, TaxonFilter
from taxonomy.models import Community, Taxon
from taxonomy.tables import CommunityAreaEncounterTable, TaxonAreaEncounterTable
from taxonomy.utils import update_taxon as update_taxon_util


@csrf_exempt
def update_taxon(request):
    """Update Taxon."""
    msg = update_taxon_util()
    messages.success(request, msg)
    return HttpResponseRedirect("/")


# ---------------------------------------------------------------------------#
# List Views
#
class TaxonListView(ListView):
    """A ListView for Taxon."""

    model = Taxon
    template_name = "taxonomy/taxon_list.html"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        """Add extra items to context."""
        context = super(TaxonListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['taxon_filter'] = TaxonFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        """Queryset: filter by name_id if in pars.

        There are two mutually exclusive ways of filtering data:

        * Taxon card > explore: GET name_id = show this taxon, its parents
          and all children. Do not process the other filter fields.
        * Search filter: name (icontains), rank, is current, publication status.

        DO NOT use taxon_filter.qs in template: https://github.com/django-mptt/django-mptt/issues/632
        """
        queryset = Taxon.objects.order_by('-rank', '-current')

        # name_id is mutually exclusive to other parameters
        if self.request.GET.get('name_id'):
            # t = queryset.filter(name_id=self.request.GET.get('name_id'))
            # return list(chain(t.first().get_ancestors(), t, t.first().get_children()))
            return queryset.filter(name_id=self.request.GET.get('name_id')).get().get_family()

        return TaxonFilter(self.request.GET, queryset=queryset).qs


class CommunityListView(ListView):
    """A ListView for Community."""

    model = Community
    paginate_by = 12

    def get_context_data(self, **kwargs):
        """Add extra items to context."""
        context = super(CommunityListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['community_filter'] = CommunityFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        """Queryset."""
        queryset = Community.objects.all()
        return CommunityFilter(self.request.GET, queryset=queryset).qs


# ---------------------------------------------------------------------------#
# Detail Views
#
class TaxonDetailView(DetailView):
    """DetailView for Taxon."""

    model = Taxon
    context_object_name = "original"

    def get_object(self):
        """Get Object by name_id."""
        object = Taxon.objects.get(name_id=self.kwargs.get("name_id"))
        return object

    def get_context_data(self, **kwargs):
        """Custom context."""
        context = super(TaxonDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        occ = obj.taxon_occurrences
        ma = obj.conservationaction_set.all()
        context['occurrence_table'] = TaxonAreaEncounterTable(occ.all()[:100])
        context['occurrences'] = occ.all()[:1000]
        context['occurrence_shown'] = occ.all()[:100].count()
        context['occurrence_total'] = occ.count()
        context['conservationactions_general'] = ma.filter(document=None, occurrence_area_code=None)
        context['conservationactions_area'] = ma.exclude(occurrence_area_code=None)
        return context


class CommunityDetailView(DetailView):
    """DetailView for Community."""

    model = Community
    context_object_name = "original"

    def get_context_data(self, **kwargs):
        """Custom context."""
        context = super(CommunityDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        occ = obj.community_occurrences
        ma = obj.conservationaction_set.all()
        context['occurrence_table'] = CommunityAreaEncounterTable(occ.all()[:100])
        context['occurrences'] = occ.all()[:1000]
        context['occurrence_shown'] = occ.all()[:100].count()
        context['occurrence_total'] = occ.count()
        context['conservationactions_general'] = ma.filter(document=None, occurrence_area_code=None)
        context['conservationactions_area'] = ma.exclude(occurrence_area_code=None)
        return context
