# -*- coding: utf-8 -*-
"""Admin module for wastd.observations."""
from __future__ import absolute_import, unicode_literals

# from leaflet.admin import LeafletGeoAdmin
from leaflet.forms.widgets import LeafletWidget

# from django import forms as django_forms
import floppyforms as ff
from django.contrib import admin
# from django.contrib.gis import forms
from django.contrib.gis.db import models as geo_models

from django.utils.translation import ugettext_lazy as _
from easy_select2 import select2_modelform  # select2_modelform_meta
# from easy_select2.widgets import Select2
from fsm_admin.mixins import FSMTransitionMixin
from reversion.admin import VersionAdmin

from wastd.observations.models import (
    Encounter, TurtleNestEncounter, AnimalEncounter,
    MediaAttachment, TagObservation, ManagementAction, TrackTallyObservation,
    TurtleMorphometricObservation, TurtleNestObservation,
    TurtleDamageObservation, )

from wastd.observations.filters import ObservationTypeListFilter


class ImageThumbnailFileInput(ff.ClearableFileInput):
    template_name = 'floppyforms/image_thumbnail.html'


class MediaAttachmentInline(admin.TabularInline):
    """TabularInlineAdmin for MediaAttachment."""

    extra = 0
    model = MediaAttachment
    classes = ('grp-collapse grp-open',)
    widgets = {'attachment': ImageThumbnailFileInput}  # seems inactive


class TagObservationInline(admin.TabularInline):
    """TabularInlineAdmin for TagObservation."""

    extra = 0
    model = TagObservation
    classes = ('grp-collapse grp-open',)


class TurtleMorphometricObservationInline(admin.StackedInline):
    """Admin for TurtleMorphometricObservation."""

    extra = 0
    model = TurtleMorphometricObservation
    classes = ('grp-collapse grp-open',)


class ManagementActionInline(admin.TabularInline):
    """TabularInlineAdmin for ManagementAction."""

    extra = 0
    model = ManagementAction
    classes = ('grp-collapse grp-open',)


class TurtleNestObservationInline(admin.StackedInline):
    """Admin for TurtleNestObservation."""

    extra = 0
    model = TurtleNestObservation
    classes = ('grp-collapse grp-open',)


class TurtleDamageObservationInline(admin.TabularInline):
    """Admin for TurtleDamageObservation."""

    extra = 0
    model = TurtleDamageObservation
    classes = ('grp-collapse grp-open',)


class TrackTallyObservationInline(admin.TabularInline):
    """Admin for TrackTallyObservation."""

    extra = 0
    model = TrackTallyObservation
    classes = ('grp-collapse grp-open',)


@admin.register(TagObservation)
class TagObservationAdmin(VersionAdmin, admin.ModelAdmin):
    """Admin for TagObservation"""

    save_on_top = True
    # date_hierarchy = 'datetime'
    list_display = ('datetime', 'latitude', 'longitude',
                    'type_display', 'name', 'tag_location_display',
                    'status_display', 'encounter_link', 'comments')
    list_filter = ('tag_type', 'tag_location', 'status')
    search_fields = ('name', 'comments')
    autocomplete_lookup_fields = {'fk': ['handler', 'recorder', ], }

    def type_display(self, obj):
        """Make tag type human readable."""
        return obj.get_tag_type_display()
    type_display.short_description = 'Tag Type'

    def tag_location_display(self, obj):
        """Make tag side human readable."""
        return obj.get_tag_location_display()
    tag_location_display.short_description = 'Tag Location'

    def status_display(self, obj):
        """Make health status human readable."""
        return obj.get_status_display()
    status_display.short_description = 'Status'

    def animal_name(self, obj):
        """Animal name."""
        return obj.encounter.name
    animal_name.short_description = 'Animal Name'

    def encounter_link(self, obj):
        """A link to the encounter."""
        return '<a href="{0}">{1}</a>'.format(obj.encounter.absolute_admin_url,
                                              obj.encounter.__str__())
    encounter_link.short_description = 'Encounter'
    encounter_link.allow_tags = True


EncounterAdminForm = select2_modelform(Encounter, attrs={'width': '350px'})


@admin.register(Encounter)
class EncounterAdmin(FSMTransitionMixin, VersionAdmin, admin.ModelAdmin):
    """Admin for Encounter with inline for MediaAttachment."""

    # Grappelli User lookup overrides select2 select widget
    raw_id_fields = ('observer', 'reporter', )
    autocomplete_lookup_fields = {'fk': ['observer', 'reporter', ], }

    # select2 widgets for searchable dropdowns
    form = EncounterAdminForm

    date_hierarchy = 'when'
    formfield_overrides = {
        geo_models.PointField: {'widget': LeafletWidget(
            attrs={
                'map_height': '400px',
                'map_width': '100%',
                'display_raw': 'true',
                'map_srid': 4326,
                }
            )},
        }
    list_filter = ('status', 'observer', 'reporter', 'location_accuracy', )
    list_display = ('when', 'latitude', 'longitude', 'location_accuracy',
                    'name', 'observer', 'reporter',
                    'status', 'source_display', 'source_id')
    list_select_related = True
    save_on_top = True
    search_fields = ('observer__name', 'observer__username', 'name',
                     'reporter__name', 'reporter__username', 'source_id',)
    fsm_field = ['status', ]
    fieldsets = (('Encounter', {'fields': (
        'where', 'location_accuracy', 'when',
        'observer', 'reporter', 'source', 'source_id', )}),)
    inlines = [
        MediaAttachmentInline,
        TagObservationInline,
        TurtleDamageObservationInline,
        TurtleMorphometricObservationInline,
        TurtleNestObservationInline,
        TrackTallyObservationInline,
        ManagementActionInline,
        ]

    def source_display(self, obj):
        """Make data source readable."""
        return obj.get_source_display()
    source_display.short_description = 'Data Source'

    def latitude(self, obj):
        """Make data source readable."""
        return obj.where.get_y()
    latitude.short_description = 'Latitude'

    def longitude(self, obj):
        """Make data source readable."""
        return obj.where.get_x()
    longitude.short_description = 'Longitude'


TurtleNestEncounterAdminForm = select2_modelform(
    TurtleNestEncounter, attrs={'width': '350px', })


@admin.register(TurtleNestEncounter)
class TurtleNestEncounterAdmin(FSMTransitionMixin,
                               VersionAdmin,
                               admin.ModelAdmin):
    """Admin for TurtleNestEncounter."""

    raw_id_fields = ('observer', 'reporter', )
    autocomplete_lookup_fields = {'fk': ['observer', 'reporter', ], }
    form = TurtleNestEncounterAdminForm
    date_hierarchy = 'when'
    formfield_overrides = {
        geo_models.PointField: {'widget': LeafletWidget(
            attrs={
                'map_height': '400px',
                'map_width': '100%',
                'display_raw': 'true',
                'map_srid': 4326,
                }
            )},
        }
    list_display = ('when', 'latitude', 'longitude', 'location_accuracy',
                    'name', 'species', 'age_display', 'habitat_display',
                    'status', 'source_display', 'source_id', 'observer', 'reporter',)
    list_filter = ('species', 'nest_age', 'habitat', 'status',
                   'observer', 'reporter', 'location_accuracy', )
    list_select_related = True
    save_on_top = True
    fsm_field = ['status', ]
    search_fields = ('observer__name', 'observer__username',
                     'reporter__name', 'reporter__username', 'name', )
    fieldsets = EncounterAdmin.fieldsets + (
        ('Nest',
         {'fields': ('nest_age', 'species', 'habitat', )}),
        )
    inlines = [
        MediaAttachmentInline,
        TagObservationInline,
        TurtleNestObservationInline,
        ]

    def habitat_display(self, obj):
        """Make habitat human readable."""
        return obj.get_habitat_display()
    habitat_display.short_description = 'Habitat'

    def age_display(self, obj):
        """Make nest age human readable."""
        return obj.get_nest_age_display()
    age_display.short_description = 'Nest age'

    def source_display(self, obj):
        """Make data source readable."""
        return obj.get_source_display()
    source_display.short_description = 'Data Source'

    def latitude(self, obj):
        """Make data source readable."""
        return obj.where.get_y()
    latitude.short_description = 'Latitude'

    def longitude(self, obj):
        """Make data source readable."""
        return obj.where.get_x()
    longitude.short_description = 'Longitude'


AnimalEncounterForm = select2_modelform(AnimalEncounter,
                                        attrs={'width': '350px'})


@admin.register(AnimalEncounter)
class AnimalEncounterAdmin(FSMTransitionMixin,
                           VersionAdmin,
                           admin.ModelAdmin):
    """Admin for AnimalEncounter."""

    raw_id_fields = ('observer', 'reporter', )
    autocomplete_lookup_fields = {'fk': ['observer', 'reporter', ], }
    form = AnimalEncounterForm
    date_hierarchy = 'when'
    formfield_overrides = {
        geo_models.PointField: {'widget': LeafletWidget(
            attrs={
                'map_height': '400px',
                'map_width': '100%',
                'display_raw': 'true',
                'map_srid': 4326,
                }
            )},
        }

    list_display = ('when', 'latitude', 'longitude', 'location_accuracy',
                    'name',
                    'species', 'health_display',
                    'cause_of_death', 'cause_of_death_confidence',
                    'maturity_display', 'sex_display', 'behaviour',
                    'habitat_display',
                    'checked_for_injuries',
                    'scanned_for_pit_tags',
                    'checked_for_flipper_tags',
                    'status', 'source_display', 'source_id', 'observer', 'reporter', )
    list_filter = (ObservationTypeListFilter,
                   'taxon', 'species',
                   'health', 'cause_of_death', 'cause_of_death_confidence',
                   'maturity', 'sex', 'habitat', 'checked_for_injuries',
                   'scanned_for_pit_tags', 'checked_for_flipper_tags',
                   'status', 'location_accuracy',
                   'observer', 'reporter', )
    list_select_related = True
    save_on_top = True
    fsm_field = ['status', ]
    search_fields = ('observer__name', 'observer__username',
                     'reporter__name', 'reporter__username', 'name', )
    fieldsets = EncounterAdmin.fieldsets + (
        ('Animal',
         {'fields': ('taxon', 'species', 'maturity', 'sex',
                     'activity', 'behaviour', 'habitat',
                     'health', 'cause_of_death', 'cause_of_death_confidence',
                     'checked_for_injuries',
                     'scanned_for_pit_tags', 'checked_for_flipper_tags',)}),
        )
    inlines = [
        MediaAttachmentInline,
        TagObservationInline,
        TurtleDamageObservationInline,
        TurtleMorphometricObservationInline,
        TurtleNestObservationInline,
        ManagementActionInline,
        ]

    def health_display(self, obj):
        """Make health status human readable."""
        return obj.get_health_display()
    health_display.short_description = 'Health'

    def maturity_display(self, obj):
        """Make maturity human readable."""
        return obj.get_maturity_display()
    maturity_display.short_description = 'Maturity'

    def sex_display(self, obj):
        """Make sex human readable."""
        return obj.get_sex_display()
    sex_display.short_description = 'Sex'

    def status_display(self, obj):
        """Make QA status human readable."""
        return obj.get_status_display()
    status_display.short_description = 'QA Status'

    def habitat_display(self, obj):
        """Make habitat human readable."""
        return obj.get_habitat_display()
    habitat_display.short_description = 'Habitat'

    def source_display(self, obj):
        """Make data source readable."""
        return obj.get_source_display()
    source_display.short_description = 'Data Source'

    def latitude(self, obj):
        """Make data source readable."""
        return obj.where.get_y()
    latitude.short_description = 'Latitude'

    def longitude(self, obj):
        """Make data source readable."""
        return obj.where.get_x()
    longitude.short_description = 'Longitude'
