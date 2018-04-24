# -*- coding: utf-8 -*-
"""Shared models."""
from __future__ import unicode_literals, absolute_import

# import itertools
import logging
# import urllib
# import slugify
# from datetime import timedelta
# from dateutil import tz

# from django.core.urlresolvers import reverse
from django.db import models
# from django.db.models.signals import pre_delete, pre_save, post_save
# from django.dispatch import receiver
# from django.contrib.gis.db import models as geo_models
# from django.contrib.gis.db.models.query import GeoQuerySet
# from django.core.urlresolvers import reverse
# from rest_framework.reverse import reverse as rest_reverse
# from django.template import loader
# from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
# from django.utils.safestring import mark_safe

# from durationfield.db.models.fields.duration import DurationField
# from django.db.models.fields import DurationField
from django_fsm import FSMField, transition
from django_fsm_log.decorators import fsm_log_by
# from django_fsm_log.models import StateLog
# from polymorphic.models import PolymorphicModel

from wastd.users.models import User

logger = logging.getLogger(__name__)


# Abstract models ------------------------------------------------------------#
class ObservationAuditMixin(models.Model):
    """Mixin class to track observer and observation date."""

    encountered_on = models.DateTimeField(
        verbose_name=_("Encountered on"),
        blank=True, null=True,
        help_text=_("The datetime of the original encounter."))

    encountered_by = models.ForeignKey(
        User,
        verbose_name=_("Encountered by"),
        blank=True, null=True,
        help_text=_("The person who experience the original encounter."))

    class Meta:
        """Class opts."""

        abstract = True


class LegacySourceMixin(models.Model):
    """Mixin class for Legacy source and source_id.

    Using this class allows a model to preserve a link to a legacy source.
    This is useful to make a data import repeatable by identifying which records
    to overwrite.
    """

    SOURCE_MANUAL_ENTRY = 0
    SOURCE_PAPER_DATASHEET = 1
    SOURCE_DIGITAL_CAPTURE_ODK = 2
    SOURCE_THREATENED_FAUNA = 10
    SOURCE_THREATENED_FLORA = 11
    SOURCE_THREATENED_COMMUNITIES = 12
    SOURCE_WAMTRAM2 = 20
    SOURCE_NINGALOO_TURTLE_PROGRAM = 21
    SOURCE_BROOME_TURTLE_PROGRAM = 22
    SOURCE_PORT_HEDLAND_TURTLE_PROGRAM = 23
    SOURCE_GNARALOO_TURTLE_PROGRAM = 24
    SOURCE_ECO_BEACH_TURTLE_PROGRAM = 25
    SOURCE_CETACEAN_STRANDINGS = 30
    SOURCE_PINNIPED_STRANDINGS = 31

    SOURCES = (
        (SOURCE_MANUAL_ENTRY, 'Direct entry'),
        (SOURCE_PAPER_DATASHEET, 'Manual entry from paper datasheet'),
        (SOURCE_DIGITAL_CAPTURE_ODK, 'Digital data capture (ODK)'),
        (SOURCE_THREATENED_FAUNA, 'Threatened Fauna'),
        (SOURCE_THREATENED_FLORA, 'Threatened Flora'),
        (SOURCE_THREATENED_COMMUNITIES, 'Threatened Communities'),
        (SOURCE_WAMTRAM2, "Turtle Tagging Database WAMTRAM2"),
        (SOURCE_NINGALOO_TURTLE_PROGRAM, "Ningaloo Turtle Program"),
        (SOURCE_BROOME_TURTLE_PROGRAM, "Broome  Turtle Program"),
        (SOURCE_PORT_HEDLAND_TURTLE_PROGRAM, "Pt Hedland Turtle Program"),
        (SOURCE_GNARALOO_TURTLE_PROGRAM, "Gnaraloo Turtle Program"),
        (SOURCE_ECO_BEACH_TURTLE_PROGRAM, "Eco Beach Turtle Program"),
        (SOURCE_CETACEAN_STRANDINGS, "Cetacean Strandings Database"),
        (SOURCE_PINNIPED_STRANDINGS, "Pinniped Strandings Database"),
    )

    source = models.PositiveIntegerField(
        verbose_name=_("Data Source"),
        default=SOURCE_MANUAL_ENTRY,
        choices=SOURCES,
        help_text=_("Where was this record captured initially?"), )

    source_id = models.CharField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Source ID"),
        help_text=_("The ID of the record in the original source, if available."), )

    class Meta:
        """Class opts."""

        abstract = True
        unique_together = ("source", "source_id")


class QualityControlMixin(models.Model):
    """Mixin class for QA status levels with django-fsm transitions."""

    STATUS_NEW = 'new'
    STATUS_PROOFREAD = 'proofread'
    STATUS_CURATED = 'curated'
    STATUS_PUBLISHED = 'published'

    STATUS_CHOICES = (
        (STATUS_NEW, _("New")),
        (STATUS_PROOFREAD, _("Proofread")),
        (STATUS_CURATED, _("Curated")),
        (STATUS_PUBLISHED, _("Published")), )

    STATUS_LABELS = {
        STATUS_NEW: "danger",
        STATUS_PROOFREAD: "warning",
        STATUS_CURATED: "info",
        STATUS_PUBLISHED: "success", }

    status = FSMField(
        default=STATUS_NEW,
        choices=STATUS_CHOICES,
        verbose_name=_("QA Status"))

    class Meta:
        """Class opts."""

        abstract = True

# FSM transitions --------------------------------------------------------#
    def can_proofread(self):
        """Return true if this document can be proofread."""
        return True

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS_NEW,
        target=STATUS_PROOFREAD,
        conditions=[can_proofread],
        # permission=lambda instance, user: user in instance.all_permitted,
        custom=dict(
            verbose="Mark as proofread",
            explanation=("This record is a faithful representation of the "
                         "data sheet."),
            notify=True,)
    )
    def proofread(self, by=None):
        """Mark encounter as proof-read.

        Proofreading compares the attached data sheet with entered values.
        Proofread data is deemed a faithful representation of original data
        captured on a paper field data collection form, or stored in a legacy
        system.
        """
        return

    def can_require_proofreading(self):
        """Return true if this document can be proofread."""
        return True

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS_PROOFREAD,
        target=STATUS_NEW,
        conditions=[can_require_proofreading],
        # permission=lambda instance, user: user in instance.all_permitted,
        custom=dict(
            verbose="Require proofreading",
            explanation=("This record deviates from the data source and "
                         "requires proofreading."),
            notify=True,)
    )
    def require_proofreading(self, by=None):
        """Mark encounter as having typos, requiring more proofreading.

        Proofreading compares the attached data sheet with entered values.
        If a discrepancy to the data sheet is found, proofreading is required.
        """
        return

    def can_curate(self):
        """Return true if this document can be marked as curated."""
        return True

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS_PROOFREAD,
        target=STATUS_CURATED,
        conditions=[can_curate],
        # permission=lambda instance, user: user in instance.all_permitted,
        custom=dict(
            verbose="Mark as trustworthy",
            explanation=("This record is deemed trustworthy."),
            notify=True,)
    )
    def curate(self, by=None):
        """Mark encounter as curated.

        Curated data is deemed trustworthy by a subject matter expert.
        """
        return

    def can_revoke_curated(self):
        """Return true if curated status can be revoked."""
        return True

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS_CURATED,
        target=STATUS_PROOFREAD,
        conditions=[can_revoke_curated],
        # permission=lambda instance, user: user in instance.all_permitted,
        custom=dict(
            verbose="Flag",
            explanation=("This record cannot be true. This record requires"
                         " review by a subject matter expert."),
            notify=True,)
    )
    def flag(self, by=None):
        """Flag as requiring changes to data.

        Curated data is deemed trustworthy by a subject matter expert.
        Revoking curation flags data for requiring changes by an expert.
        """
        return

    def can_publish(self):
        """Return true if this document can be published."""
        return True

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS_CURATED,
        target=STATUS_PUBLISHED,
        conditions=[can_publish],
        # permission=lambda instance, user: user in instance.all_permitted,
        custom=dict(
            verbose="Publish",
            explanation=("This record is fit for release."),
            notify=True,)
    )
    def publish(self, by=None):
        """Mark encounter as ready to be published.

        Published data has been deemed fit for release by the data owner.
        """
        return

    def can_embargo(self):
        """Return true if encounter can be embargoed."""
        return True

    @fsm_log_by
    @transition(
        field=status,
        source=STATUS_PUBLISHED,
        target=STATUS_CURATED,
        conditions=[can_embargo],
        # permission=lambda instance, user: user in instance.all_permitted,
        custom=dict(
            verbose="Embargo",
            explanation=("This record is not fit for release."),
            notify=True,)
    )
    def embargo(self, by=None):
        """Mark encounter as NOT ready to be published.

        Published data has been deemed fit for release by the data owner.
        Embargoed data is marked as curated, but not ready for release.
        """
        return