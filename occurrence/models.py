# -*- coding: utf-8 -*-
"""Occurrence models.

These models support opportunistic encounters with threatened and priority
Fauna, Flora and Comunities (defined in taxonomy).

Observer name / address / phone / email is captured through the observer being
a system user.
"""
import logging

from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as geo_models
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save, pre_delete, pre_save  # noqa
from django.dispatch import receiver

from django.template import loader
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from polymorphic.models import PolymorphicModel

from shared.models import (
    CodeLabelDescriptionMixin,
    RenderMixin,
    LegacySourceMixin,
    ObservationAuditMixin,
    QualityControlMixin,
    UrlsMixin
)
from taxonomy.models import Community, Taxon

logger = logging.getLogger(__name__)
User = get_user_model()


class EncounterType(CodeLabelDescriptionMixin, models.Model):
    """The encounter type."""
    pass


class AreaEncounter(PolymorphicModel,
                    RenderMixin,
                    UrlsMixin,
                    LegacySourceMixin,
                    ObservationAuditMixin,
                    QualityControlMixin,
                    geo_models.Model):
    """An Encounter with an Area.

    The Area is represented spatially throuh a polygonal extent
    and an additional point.

    This model accommodates anything with a spatial extent, providing:

    * Area type (to classify different kinds of areas)
    * Area code to identify multiple measurements of the same Area
    * Polygonal or Point representation of the area
    * Mixins: data QA levels, legacy source tracking

    Some additional fields are populated behind the scenes at each save and
    serve to cache low churn, high use content:

    * label: the cached __str__ representation
    * point: set from geom centroid id empty
    * northern extent: useful to sort Areas by latitude
    * as html: a pre-compiled HTML map popup
    """

    AREA_TYPE_EPHEMERAL_SITE = 0
    AREA_TYPE_PERMANENT_SITE = 1
    AREA_TYPE_CRITICAL_HABITAT = 2
    AREA_TYPE_PARTIAL_SURVEY = 3
    AREA_TYPE_TEC_BOUNDARY = 10
    AREA_TYPE_TEC_BUFFER = 11
    AREA_TYPE_TEC_SITE = 12
    AREA_TYPE_FLORA_POPULATION = 20
    AREA_TYPE_FLORA_SUBPOPULATION = 21
    AREA_TYPE_FAUNA_SITE = 30
    AREA_TYPE_MPA = 40
    AREA_TYPE_LOCALITY = 41

    AREA_TYPES = (
        (AREA_TYPE_EPHEMERAL_SITE, "Fauna Ephemeral Site"),
        (AREA_TYPE_PERMANENT_SITE, "Fauna Permanent Site"),
        (AREA_TYPE_PARTIAL_SURVEY, "Generic Partial survey"),
        (AREA_TYPE_CRITICAL_HABITAT, "Critical Habitat"),
        (AREA_TYPE_TEC_BOUNDARY, "TEC Boundary"),
        (AREA_TYPE_TEC_BUFFER, "TEC Buffer"),
        (AREA_TYPE_TEC_SITE, "TEC Site"),
        (AREA_TYPE_FLORA_POPULATION, "Flora Population"),
        (AREA_TYPE_FLORA_SUBPOPULATION, "Flora Subpopulation"),
        (AREA_TYPE_FAUNA_SITE, "Fauna Site"),
        (AREA_TYPE_MPA, "Marine Protected Area"),
        (AREA_TYPE_LOCALITY, "Locality"),
    )

    COMMUNITY_AREA_TYPES = (
        (AREA_TYPE_PARTIAL_SURVEY, "Generic Partial Survey"),
        (AREA_TYPE_TEC_BOUNDARY, "TEC Boundary"),
        (AREA_TYPE_TEC_BUFFER, "TEC Buffer"),
        (AREA_TYPE_TEC_SITE, "TEC Site"),
    )

    TAXON_AREA_TYPES = (
        (AREA_TYPE_EPHEMERAL_SITE, "Fauna Ephemeral Site"),
        (AREA_TYPE_PERMANENT_SITE, "Fauna Permanent Site"),
        (AREA_TYPE_PARTIAL_SURVEY, "Generic Partial Survey"),
        (AREA_TYPE_FLORA_POPULATION, "Flora Population"),
        (AREA_TYPE_FLORA_SUBPOPULATION, "Flora Subpopulation"),
    )

    GEOLOCATION_CAPTURE_METHOD_DEFAULT = 'drawn-online-map-widget'
    GEOLOCATION_CAPTURE_METHOD_CHOICES = (
        (GEOLOCATION_CAPTURE_METHOD_DEFAULT, _("Hand-drawn on online map widget")),
        ("gps-point", _("GPS point with text description of location extent")),
        ("gps-perimeter-walk", _("GPS perimeter walk")),
        ("dgps", _("Differential GPS capture of entire location extent")),
    )

    # Naming -----------------------------------------------------------------#
    code = models.SlugField(
        max_length=1000,
        blank=True, null=True,
        verbose_name=_("Area code"),
        help_text=_("A URL-safe, short code for the area. "
                    "Multiple records of the same Area "
                    "will be recognised by the same area type and code."),
    )

    label = models.CharField(
        blank=True, null=True,
        max_length=1000,
        editable=False,
        verbose_name=_("Label"),
        help_text=_("A short but comprehensive label for the encounter, "
                    "populated from the model's string representation."),
    )

    name = models.CharField(
        blank=True, null=True,
        db_index=True,
        max_length=1000,
        verbose_name=_("Area name"),
        help_text=_("A human-readable name for the observed area."),
    )

    description = models.TextField(
        blank=True, null=True,
        verbose_name=_("Description"),
        help_text=_(
            "A comprehensive description of the location "
            "(nearby features and places, identifiable boundaries, extent) "
            "and the encounter where forms and attached photos lack detail."
        ),
    )

    # Time: ObservationAuditMixin provides date and observer -----------------#
    #
    # Encounter type: what brought the observer to the encounter? opportunistic, research, monitoring
    encounter_type = models.ForeignKey(
        EncounterType,
        db_index=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Encounter Type"),
        blank=True, null=True,
        help_text=_("Add missing encounter types via the data curation portal.")
    )

    # Geolocation ------------------------------------------------------------#
    area_type = models.PositiveIntegerField(
        verbose_name=_("Area type"),
        db_index=True,
        default=AREA_TYPE_EPHEMERAL_SITE,
        choices=AREA_TYPES,
        help_text=_(
            "What type describes the area occupied by the encounter "
            "most accurately? The area can be an opportunistic, once-off "
            "chance encounter (point), a fixed survey site (polygon), a "
            "partial or a complete survey of an area occupied by the "
            "encountered subject (polygon)."),
    )

    accuracy = models.FloatField(
        blank=True, null=True,
        verbose_name=_("Accuracy [m]"),
        help_text=_("The measured or estimated accuracy "
                    "of the location in meters."),
    )

    geolocation_capture_method = models.CharField(
        verbose_name=_("Geolocation capture method"),
        max_length=100,
        default=GEOLOCATION_CAPTURE_METHOD_DEFAULT,
        choices=GEOLOCATION_CAPTURE_METHOD_CHOICES,
        help_text=_(
            "How were the coordinates of the geolocation captured? "
        ),
    )

    point = geo_models.PointField(
        srid=4326,
        blank=True, null=True,
        verbose_name=_("Representative Point"),
        help_text=_(
            "A point representing the area occupied by the encountered "
            "subject. If empty, the point will be calculated as the centroid "
            "of the polygon extent."))

    northern_extent = models.FloatField(
        verbose_name=_("Northernmost latitude"),
        editable=False,
        db_index=True,
        blank=True, null=True,
        help_text=_("The northernmost latitude is derived from location "
                    "polygon or point and serves to sort areas."),)

    geom = geo_models.PolygonField(
        srid=4326,
        blank=True, null=True,
        verbose_name=_("Location"),
        help_text=_("The exact extent of the area occupied by the encountered "
                    "subject as polygon in WGS84, if available."))

    # -------------------------------------------------------------------------
    # Cached fields
    as_html = models.TextField(
        verbose_name=_("HTML representation"),
        blank=True, null=True, editable=False,
        help_text=_("The cached HTML representation for display purposes."),)

    class Meta:
        """Class options."""

        # ordering = ["-northern_extent", "name"]
        verbose_name = "Area Encounter"
        verbose_name_plural = "Area Encounters"
        index_together = [["northern_extent", "name"], ]
        unique_together = ("source", "source_id")

    def __str__(self):
        """The unicode representation."""
        return "Encounter at [{0}] ({1}) {2} on {3} by {4}".format(
            self.get_area_type_display(),
            self.code,
            self.name,
            self.encountered_on,
            self.encountered_by)

    # -------------------------------------------------------------------------
    # URLs

    # -------------------------------------------------------------------------
    # Derived properties
    @property
    def latitude(self):
        """The latitude of the point."""
        return self.point.y if self.point else None

    @property
    def longitude(self):
        """The longitude of the point."""
        return self.point.x if self.point else None

    @property
    def derived_point(self):
        """The point, derived from the polygon."""
        if self.geom:
            return self.geom.centroid
        elif self.point:
            return self.point
        else:
            return None

    @property
    def derived_northern_extent(self):
        """The northernmost extent of the polygon, or the latitude of the point."""
        if self.geom:
            return self.geom.extent[3]
        elif self.point:
            return self.point.y
        else:
            return None

    @property
    def card_template(self):
        """One shared template works for both TAE and CAE."""
        return "occurrence/cards/areaencounter.html"

    @property
    def html_template(self):
        """One shared template works for both TAE and CAE."""
        return "occurrence/popup/areaencounter.html"

    @property
    def derived_html(self):
        """Generate HTML popup content."""
        t = loader.get_template(self.html_template)
        return mark_safe(t.render({"object": self}))

    @property
    def subject(self):
        """Return the subject of the encounter."""
        return self

    # -------------------------------------------------------------------------
    # Functions
    def get_nearby_encounters(self, dist_dd=0.005):
        """Get encounters within dist_dd (default 0.005 degrees, ca 500m).

        Arguments:

        dist_dd <float> The search radius in decimal degrees. Default: 0.005 (ca 500 m).

        Returns:
        A queryset of nearby AreaEncounters.
        """
        return AreaEncounter.objects.filter(point__distance_lte=(self.point, dist_dd))


class TaxonAreaEncounter(AreaEncounter):
    """An Encounter in time and space with a Taxon."""

    taxon = models.ForeignKey(
        Taxon,
        on_delete=models.PROTECT,
        related_name="taxon_occurrences",
        help_text=_("The taxonomic name of the encountered subject."),
    )

    class Meta:
        """Class options."""

        verbose_name = "Taxon Encounter"
        verbose_name_plural = "Taxon Encounters"
        card_template = "occurrence/cards/areaencounter.html"
        ordering = ["id", ]

    def __str__(self):
        """The unicode representation."""
        return "Encounter of {5} at [{0}] ({1}) {2} on {3} by {4}".format(
            self.get_area_type_display(),
            self.code,
            self.name,
            self.encountered_on,
            self.encountered_by,
            self.taxon)

    # -------------------------------------------------------------------------
    # Derived properties
    @property
    def subject(self):
        """Return the subject of the encounter."""
        return self.taxon

    def get_subject(self):
        """Return the subject of the encounter."""
        return self.taxon

    # -------------------------------------------------------------------------
    # Functions
    def nearby_same(self, dist_dd=0.005):
        """Return encounters with same taxon within search radius (dist_dd).

        Arguments:

        dist_dd <float> The search radius in decimal degrees. Default: 0.005 (ca 500 m).

        Returns:
        A queryset of nearby TaxonAreaEncounters.
        """
        return TaxonAreaEncounter.objects.filter(
            taxon=self.taxon,
            point__distance_lte=(self.point, dist_dd)
        )


class CommunityAreaEncounter(AreaEncounter):
    """An Encounter in time and space with a community."""

    community = models.ForeignKey(Community, on_delete=models.PROTECT, related_name="community_occurrences")

    class Meta:
        """Class options."""

        verbose_name = "Community Encounter"
        verbose_name_plural = "Community Encounters"
        card_template = "occurrence/cards/areaencounter.html"
        ordering = ["id", ]

    def __str__(self):
        """The unicode representation."""
        return "Encounter of {5} at [{0}] ({1}) {2} on {3} by {4}".format(
            self.get_area_type_display(),
            self.code,
            self.name,
            self.encountered_on,
            self.encountered_by,
            self.community)

    # -------------------------------------------------------------------------
    # Derived properties
    @property
    def subject(self):
        """Return the subject of the encounter."""
        return self.community

    # -------------------------------------------------------------------------
    # Functions
    def nearby_same(self, dist_dd=0.005):
        """Return encounters with same community within search radius (dist_dd).

        Arguments:

        dist_dd <float> The search radius in decimal degrees. Default: 0.005 (ca 500 m).

        Returns:
        A queryset of nearby CommunityAreaEncounters.
        """
        return CommunityAreaEncounter.objects.filter(
            community=self.community,
            point__distance_lte=(self.point, dist_dd)
        )


@receiver(pre_save, sender=TaxonAreaEncounter)
@receiver(pre_save, sender=CommunityAreaEncounter)
def area_caches(sender, instance, *args, **kwargs):
    """AreaEncounter: Cache expensive lookups."""
    if instance.code:
        instance.code = slugify(instance.code)

    if not instance.code and instance.name:
        instance.code = slugify(instance.name)

    if instance.code and not instance.name:
        instance.name = instance.code.title().replace('-', ' ')

    if instance.geom and not instance.point:
        instance.point = instance.derived_point

    instance.northern_extent = instance.derived_northern_extent
    instance.label = instance.__str__()[0:1000]

    if instance.pk:
        logger.info("[areaencounter_caches] Updating cache fields.")
        instance.as_html = instance.derived_html
    else:
        logger.info("[area_caches] New Area, re-save to populate caches.")


# Observation models ---------------------------------------------------------#
class ObservationGroup(
        QualityControlMixin,
        RenderMixin,
        UrlsMixin,
        PolymorphicModel,
        models.Model):
    """The Observation base class for area encounter observations.

    Everything happens somewhere, at a time, to someone, and someone records it.
    Therefore, an ObservationGroup must happen during an Encounter.

    The ObservationGroup shares with Encounter:

    * location,
    * datetime,
    * reporter,
    * subject (species or community).

    The ObservationGroup has its own:

    * QA trust levels.

    Having separate QA trust levels allows to synthesize the "best available information"
    about a Species / Community occurrence, hand-selected by custodians from different
    TAE/CAE.
    """

    encounter = models.ForeignKey(
        AreaEncounter,
        on_delete=models.CASCADE,
        verbose_name=_("Occurrence"),
        related_name="observations",
        help_text=("The Occurrence report containing the observation group."),)

    class Meta:
        """Class options."""

        verbose_name = "Observation Group"

    def __str__(self):
        """The unicode representation."""
        return "[{0} {1}] {2} {3}".format(
            self.encounter.opts.verbose_name.title(),
            self.encounter.pk,
            self.opts.verbose_name,
            self.pk
        )

    # -------------------------------------------------------------------------
    # URLs
    def get_absolute_url(self):
        """Detail url."""
        return self.encounter.get_absolute_url()

    def list_url(self):
        """ObsGroup list is not defined."""
        return NotImplementedError("TODO: implement ObservationGroup list view.")

    @property
    def update_url(self):
        """Custom update url contains occ pk and obsgroup pk."""
        return reverse('{0}:{1}-update'.format(
            self._meta.app_label, self._meta.model_name),
            kwargs={'occ_pk': self.encounter.pk, 'obs_pk': self.pk})

    # -------------------------------------------------------------------------
    # Derived properties
    @property
    def opts(self):
        """Model opts."""
        return self._meta

    # Text representation
    @property
    def tldr(self):
        """A text summary of the observation."""
        return ""

    # Location and date
    @property
    def point(self):
        """Return the encounter point location."""
        return self.encounter.point

    @property
    def latitude(self):
        """The encounter's latitude."""
        return self.encounter.point.y or ''

    @property
    def longitude(self):
        """The encounter's longitude."""
        return self.encounter.point.x or ''

    @property
    def datetime(self):
        """The encounter's timestamp."""
        return self.encounter.encountered_on or ''

    # Display and cached properties
    @property
    def observation_name(self):
        """The concrete model name.

        This method will inherit down the polymorphic chain, and always return
        the actual child model's name.

        `observation_name` can be included as field e.g. in API serializers,
        so e.g. a writeable serializer would know which child model to `create`
        or `update`.
        """
        return self.polymorphic_ctype.model

    @property
    def model_name_verbose(self):
        """Return the model's verbose name."""
        return self.opts.verbose_name

    # -------------------------------------------------------------------------
    # Functions
    # none yet


def fileattachmentobservation_media(instance, filename):
    """Return an upload path for FileAttachment media."""
    return 'files/{0}/{1}/{2}'.format(
        instance.encounter.pk,
        instance.pk,
        filename
    )


class FileAttachment(ObservationGroup):
    """A file attachment to an ObservationGroup.

    The file attachment can be a photo, a paper datasheet scanned to PDF,
    a video or audio clip, a communication record or any other digital resource
    up to the maximum upload size.

    Copyright is handled at application level, i.e. by submitting a file
    as attachment, the author permits use by the application and downstream
    systems under the application's agreed license, e.g. cc-by-sa.

    Each attachment can be marked as confidential to be excluded from publication.
    """

    attachment = models.FileField(upload_to=fileattachmentobservation_media)

    title = models.CharField(
        blank=True, null=True,
        max_length=500,
        verbose_name=_("Title"),
        help_text=_("A self-explanatory title for the file attachment."))

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name=_("Author"),
        related_name="occurrence_fileattachments",
        blank=True, null=True,
        help_text=_("The person who authored and endorsed this file."))

    confidential = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Is confidential"),
        help_text=_("Whether this file is confidential or "
                    "can be released to the public."),)

    class Meta:
        """Class options."""

        verbose_name = "File Attachment"
        verbose_name_plural = "File Attachments"

    @property
    def tldr(self):
        """A text summary of the observation."""
        return "{0} ({1})".format(self.title, self.author.fullname)


# -----------------------------------------------------------------------------
# Site level observations
#
class Landform(CodeLabelDescriptionMixin, models.Model):
    """The landform.

    Sources:

    Gillian Stack 2017: TPFR Field Manual, Appendix 5, Landform.
    McDonald et al 1998: The Australian Soil and Land Survey Field Handbook.
    Hill et al 1996: Wetland of the Swan Coastal Plain - Wetland Mapping,
    Clasification and Evaluation Vol 2a.
    """

    pass


class RockType(CodeLabelDescriptionMixin, models.Model):
    """The rock type.

    Sources:

    Gillian Stack 2017: TPFR Field Manual, Appendix 6, Rock type. p31.
    """

    pass


class SoilType(CodeLabelDescriptionMixin, models.Model):
    """The soil type.

    Sources:

    Gillian Stack 2017: TPFR Field Manual, Appendix 7, Soil type. p32.
    """

    pass


class SoilColour(CodeLabelDescriptionMixin, models.Model):
    """The soil colour.

    Sources:

    Gillian Stack 2017: TPFR Field Manual, Appendix 8, Soil colour. p33.
    """

    pass


class Drainage(CodeLabelDescriptionMixin, models.Model):
    """The water drainage."""

    pass


class HabitatComposition(ObservationGroup):
    """Habitat composition."""

    landform = models.ForeignKey(
        Landform,
        on_delete=models.SET_NULL,
        verbose_name=_("Landform"),
        blank=True, null=True,
        help_text=_("The landform."))

    rock_type = models.ForeignKey(
        RockType,
        on_delete=models.SET_NULL,
        verbose_name=_("Rock type"),
        blank=True, null=True,
        help_text=_("Add missing rock types via the data curation portal."))

    loose_rock_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True,
        verbose_name=_("Loose rock [%]"),
        help_text=_("The proportion of habitat covered by loose rock "
                    "in percent from none (0) to all (100)."),
    )

    soil_type = models.ForeignKey(
        SoilType,
        on_delete=models.SET_NULL,
        verbose_name=_("Soil type"),
        blank=True, null=True,
        help_text=_("Add missing soil types via the data curation portal.")
    )

    soil_colour = models.ForeignKey(
        SoilColour,
        on_delete=models.SET_NULL,
        verbose_name=_("Soil colour"),
        blank=True, null=True,
        help_text=_("Add missing soil colours via the data curation portal.")
    )

    drainage = models.ForeignKey(
        Drainage,
        on_delete=models.SET_NULL,
        verbose_name=_("Drainage"),
        blank=True, null=True,
        help_text=_("Add missing drainage types via the data curation portal.")
    )

    class Meta:
        """Class options."""

        verbose_name = "Habitat Composition"
        verbose_name_plural = "Habitat Compositions"

    def tldr(self):
        """A text summary of the observation."""
        return "Lf {0}, RT {1}, LR {2}%, ST {3}, SC {4}, Dr {5}".format(
            self.landform.label,
            self.rocktype.label,
            self.loose_rock_percent,
            self.soiltype.label,
            self.soilcolour.label,
            self.drainage.label,

        )


# Fire response is OOS

# -----------------------------------------------------------------------------
# Survey level observations
#
class SurveyMethod(CodeLabelDescriptionMixin, models.Model):
    """The survey method."""

    pass


class AreaAssessment(ObservationGroup):
    """A description of survey effort at a flora or TEC site."""

    survey_method = models.ForeignKey(
        SurveyMethod,
        on_delete=models.SET_NULL,
        verbose_name=_("Survey Method"),
        blank=True, null=True,
        help_text=_("Add missing survey methods via the data curation portal.")
    )

    area_surveyed_m2 = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Surveyed Area [m2]"),
        help_text=_("An estimate of surveyed area in square meters."),
    )

    survey_duration_min = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Survey Duration [min]"),
        help_text=_("An estimate of survey duration minutes."),
    )

    class Meta:
        """Class options."""

        verbose_name = "Area Assessment"
        verbose_name_plural = "Area Assessments"

    @property
    def tldr(self):
        """A text summary of the observation."""
        return "{0} of {1} m2 in {2} mins".format(
            self.survey_method,
            self.area_surveyed_m2,
            self.survey_duration_min)

    @property
    def survey_effort_minutes_per_100sqm(self):
        """Give an estimate of survey intensity as time spent per area.

        Calculated from area surveyed and survey duration, or None.
        Unit is minutes / 100 m2.
        """
        if self.area_surveyed_m2 and self.survey_duration_min:
            return round(100 * (self.survey_duration_min / self.area_surveyed_m2))
        else:
            return None


class SoilCondition(CodeLabelDescriptionMixin, models.Model):
    """The soil condition."""

    pass


class HabitatCondition(ObservationGroup):
    """Community occurrence or habitat condition on date of encounter.

    Estimated percentages of observed area at each bush forever scale.
    """

    pristine_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True,
        verbose_name=_("Pristine [%]"),
        help_text=_("The proportion of habitat in percent [0..100] in pristine condition."),
    )

    excellent_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True,
        verbose_name=_("Excellent [%]"),
        help_text=_("The proportion of habitat in percent [0..100] in excellent condition."),
    )

    very_good_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True,
        verbose_name=_("Very good [%]"),
        help_text=_("The proportion of habitat in percent [0..100] in very good condition."),
    )

    good_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True,
        verbose_name=_("Good [%]"),
        help_text=_("The proportion of habitat in percent [0..100] in good condition."),
    )

    degraded_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True,
        verbose_name=_("Degraded [%]"),
        help_text=_("The proportion of habitat in percent [0..100] in degraded condition."),
    )

    completely_degraded_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True,
        verbose_name=_("Completely_degraded [%]"),
        help_text=_("The proportion of habitat in percent [0..100] in completely degraded condition."),
    )

    soil_condition = models.ForeignKey(
        SoilCondition,
        on_delete=models.SET_NULL,
        verbose_name=_("Soil condition"),
        blank=True, null=True,
        help_text=_("Add missing soil conditions via the data curation portal.")
    )

    class Meta:
        """Class options."""

        verbose_name = "Habitat Condition"
        verbose_name_plural = "Habitat Conditions"

    @property
    def tldr(self):
        """A text summary of the observation."""
        return "PRS {0}, EXC {1}, VGD {2}, GOO {3}, DGR {4}, CDG {5}, SC {6}".format(
            self.pristine_percent,
            self.excellent_percent,
            self.very_good_percent,
            self.good_percent,
            self.degraded_percent,
            self.completely_degraded_percent,
            self.soil_condition
        )


class FireHistory(ObservationGroup):
    """Evidence of past fire date and intensity."""

    HMLN_DEFAULT = "NA"
    HMLN_NONE = "no"
    HMLN_LOW = "low"
    HMLN_MEDIUM = "medium"
    HMLN_HIGH = "high"
    HMLN_CHOICES = (
        (HMLN_DEFAULT, "NA"),
        (HMLN_NONE, "No evidence of fire"),
        (HMLN_LOW, "Low"),
        (HMLN_MEDIUM, "Medium"),
        (HMLN_HIGH, "High"),
    )

    last_fire_date = models.DateField(
        verbose_name=_("Date of last fire"),
        blank=True, null=True,
        help_text=_("The estimated date of the last fire, if evident."))

    fire_intensity = models.CharField(
        verbose_name=_("Fire intensity"),
        max_length=100,
        default=HMLN_DEFAULT,
        choices=HMLN_CHOICES,
        help_text=_(
            "Estimated intensity of last fire on a scale from High to Low, "
            "or NA if no evidence of past fires."
        ),
    )

    class Meta:
        """Class options."""

        verbose_name = "Fire History"
        verbose_name_plural = "Fire Histories"

    @property
    def tldr(self):
        """A text summary of the observation."""
        return "{0} intensity fire on {1}".format(
            self.get_fire_intensity_display(),
            self.last_fire_date.strftime("%d/%m/%Y"),
        )


# -----------------------------------------------------------------------------
# Population level observations
#
class VegetationClassification(ObservationGroup):
    """Veg Classification should follow NVIS classification categories.

    This is a free text version for legacy data.
    """

    level1 = models.TextField(
        blank=True, null=True,
        verbose_name=_("Level 1"),
        help_text=_("The first classification level."),
    )

    level2 = models.TextField(
        blank=True, null=True,
        verbose_name=_("Level 2"),
        help_text=_("The first classification level."),
    )

    level3 = models.TextField(
        blank=True, null=True,
        verbose_name=_("Level 3"),
        help_text=_("The first classification level."),
    )

    level4 = models.TextField(
        blank=True, null=True,
        verbose_name=_("Level 4"),
        help_text=_("The first classification level."),
    )

    class Meta:
        """Class options."""

        verbose_name = "Vegetation Classification"
        verbose_name_plural = "Vegetation Classifications"

    @property
    def tldr(self):
        """A text summary of the observation."""
        return self.level1


class CountAccuracy(CodeLabelDescriptionMixin, models.Model):
    """Accuracy levels."""

    pass


class CountMethod(CodeLabelDescriptionMixin, models.Model):
    """The count method."""

    pass


class CountSubject(CodeLabelDescriptionMixin, models.Model):
    """The count subject."""

    pass


class PlantCondition(CodeLabelDescriptionMixin, models.Model):
    """The plant condition."""

    pass


class PlantCount(ObservationGroup):
    """Population plant count."""

    # Survey level
    land_manager_present = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Land Manager Present"),
        help_text=_("Especially on private property, was the land manager or owner present?"),)

    count_method = models.ForeignKey(
        CountMethod,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Plant Count Method"),
        help_text=_("Add missing lookup values via the data curation portal.")
    )

    count_accuracy = models.ForeignKey(
        CountAccuracy,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Plant Count Accuracy"),
        help_text=_("Add missing lookup values via the data curation portal.")
    )

    count_subject = models.ForeignKey(
        CountSubject,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Counted Subject"),
        help_text=_("What was counted?"),
    )

    # Plant Count (Detailed)
    no_alive_mature = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number Alive Mature"),
        help_text=_("Number of alive, mature individuals counted."),
    )

    no_alive_juvenile = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number Alive Juvenile"),
        help_text=_("Number of alive, juvenile individuals counted."),
    )

    no_alive_seedlings = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number Alive Seedlings"),
        help_text=_("Number of alive seedlings counted."),
    )
    no_dead_mature = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number Dead Mature"),
        help_text=_("Number of dead, mature individuals counted."),
    )
    no_dead_juvenile = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number Dead Juvenile"),
        help_text=_("Number of dead, juvenile individuals counted."),
    )
    no_dead_seedlings = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number Dead Seedlings"),
        help_text=_("Number of dead seedlings counted."),
    )

    # Plant Count (Simple)
    no_alive_simple = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number Alive (Simple)"),
        help_text=_("Number of alive individuals counted in a simple count."),
    )

    no_dead_simple = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number Dead (Simple)"),
        help_text=_("Number of dead individuals counted in a simple count."),
    )

    # Quadrats
    population_area_estimated_m2 = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Estimated population area [m2]"),
        help_text=_("The estimated area of the encountered plant"
                    " population in square meters."),
    )

    quadrats_present = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Quadrats Present"),
        help_text=_("Were survey quadrats present?"),)

    quadrats_details_attached = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Quadrat Details Attached"),
        help_text=_("Are details of quadrat surveys uploaded as File Attachment?"),)

    no_quadrats_surveyed = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number of Quadrats Surveyed"),
        help_text=_("Number of quadrats which were surveyed."),
    )

    quadrat_area_individual_m2 = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Individual Quadrat Area [m2]"),
        help_text=_("The area one individual survey quadrat in square meters."),
    )

    quadrat_area_total_m2 = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Total Quadrat Area [m2]"),
        help_text=_("The area all survey quadrats combined in square meters."),
    )

    # Flowering
    flowering_plants_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        blank=True, null=True,
        verbose_name=_("Flowering Plants [%]"),
        help_text=_("The proportion of plants of surveyed population in ."),
    )

    clonal_present = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Clonal Peproduction Present"),
        help_text=_("Was evidence of clonal reproduction found?"),)

    vegetative_present = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Vegetative State Present"),
        help_text=_("Were plants in vegetative state found?"),)

    flowerbuds_present = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Flower Buds Present"),
        help_text=_("Were plants with flower buds found?"),)

    flowers_present = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Flowers Present"),
        help_text=_("Were plants with flowers found?"),)

    immature_fruit_present = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Immature Fruit Present"),
        help_text=_("Were plants with immature fruit found?"),)

    ripe_fruit_present = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Ripe Fruit Present"),
        help_text=_("Were plants with ripe fruit found?"),)

    dehisced_fruit_present = models.BooleanField(
        db_index=True,
        default=False,
        verbose_name=_("Dehisced Fruit Present"),
        help_text=_("Were plants with dehisced fruit found?"),)

    # Plant condition
    plant_condition = models.ForeignKey(
        PlantCondition,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Plant condition"),
        help_text=_("What condition were most of the plants in?"),
    )

    comments = models.TextField(
        blank=True, null=True,
        verbose_name=_("Comments"),
        help_text=_("Any further comments on the plant population."),
    )

    class Meta:
        """Class options."""

        verbose_name = "Plant Count"
        verbose_name_plural = "Plant Counts"

    @property
    def tldr(self):
        """A text summary of the observation."""
        return self.count_method

    @property
    def no_alive_total(self):
        """The total number of alive individuals counted."""
        return (
            self.no_alive_mature or 0
        ) + (
            self.no_alive_juvenile or 0
        ) + (
            self.no_alive_seedlings or 0
        )

    @property
    def no_dead_total(self):
        """The total number of dead individuals counted."""
        return (
            self.no_dead_mature or 0
        ) + (
            self.no_dead_juvenile or 0
        ) + (
            self.no_dead_seedlings or 0
        )


class AssociatedSpecies(ObservationGroup):
    """Observation of an associated species."""

    taxon = models.ForeignKey(
        Taxon,
        on_delete=models.CASCADE,
        related_name="associated_species")

    class Meta:
        """Class options."""

        verbose_name = "Associated Species"
        verbose_name_plural = "Associated Species"

    @property
    def tldr(self):
        """A text summary of the observation."""
        return self.taxon


# -----------------------------------------------------------------------------
# Individual level observations
#
class DetectionMethod(CodeLabelDescriptionMixin, models.Model):
    """The detection method of an Encounter."""

    pass


class Confidence(CodeLabelDescriptionMixin, models.Model):
    """The confidence of the observer about the correctness of a given observation."""

    pass


class ReproductiveMaturity(CodeLabelDescriptionMixin, models.Model):
    """The reproductive maturity of an animal."""

    pass


class AnimalHealth(CodeLabelDescriptionMixin, models.Model):
    """The health of an animal."""

    pass


class AnimalSex(CodeLabelDescriptionMixin, models.Model):
    """The sex of an animal."""

    pass


class CauseOfDeath(CodeLabelDescriptionMixin, models.Model):
    """The cause of death of an animal."""

    pass


class SecondarySigns(CodeLabelDescriptionMixin, models.Model):
    """Secondary signs of an animal."""

    pass


class AnimalObservation(ObservationGroup):
    """Observation of an Animal.

    The observation may include several other animals
    apart from the primarily observed animal.

    * detection method
    * Taxonomic identification and confidence
    * sex
    * reproductive state
    * dist features, comments
    * demographics of all other observed animals
    * secondary signs
    """

    # detection method: sighting, trapped, spotlighting, remote camera,
    # remote sensing, oral report, written report, acoustic recorder,
    # fossil, subfossil, capture, release
    detection_method = models.ForeignKey(
        DetectionMethod,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Detection Method"),
        help_text=_("What brought the human observer to the Encounter?"),
    )

    # species id confidence: guess, certain, expert
    species_id_confidence = models.ForeignKey(
        Confidence,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Species ID Confidence"),
        help_text=_("How correct is the species ID according to the observer?"),
    )

    # species identified by (user/name and affiliation): expert changes species in TSC

    # reproductive state: adult, subadult, juvenile, dependent young
    maturity = models.ForeignKey(
        ReproductiveMaturity,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Reproductive Maturity"),
        help_text=_("Reproductive Maturity of the primary observed animal."),
    )

    sex = models.ForeignKey(
        AnimalSex,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Animal Sex"),
        help_text=_("The sex of the primary observed animal."),
    )

    health = models.ForeignKey(
        AnimalHealth,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Animal Health"),
        help_text=_("The health status of the primary observed animal."),
    )

    cause_of_death = models.ForeignKey(
        CauseOfDeath,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Cause of Death"),
        help_text=_("The cause of death of the primary observed animal, if applicable."),
    )

    # primary observed animal: dist feature description
    distinctive_features = models.TextField(
        blank=True, null=True,
        verbose_name=_("Distinctive features"),
        help_text=_("Distinctive features of the primary observed animal. "
                    "Include injuries if applicable."),
    )

    actions_taken = models.TextField(
        blank=True, null=True,
        verbose_name=_("Actions taken"),
        help_text=_("Any actions taken, if applicable."),
    )

    actions_required = models.TextField(
        blank=True, null=True,
        verbose_name=_("Actions required"),
        help_text=_("Any actions required, if applicable."),
    )

    # no_adult_male
    no_adult_male = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number of adult males"),
        help_text=_("Including the primary observed animal."),
    )
    no_adult_female = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number of adult females"),
        help_text=_("Including the primary observed animal."),
    )
    no_adult_unknown = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number of adult unknown"),
        help_text=_("Including the primary observed animal."),
    )

    no_juvenile_male = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number of juvenile males"),
        help_text=_("Including the primary observed animal."),
    )
    no_juvenile_female = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number of juvenile females"),
        help_text=_("Including the primary observed animal."),
    )
    no_juvenile_unknown = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number of juvenile unknown"),
        help_text=_("Including the primary observed animal."),
    )

    no_dependent_young_male = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number of dependent_young males"),
        help_text=_("Including the primary observed animal."),
    )
    no_dependent_young_female = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number of dependent_young females"),
        help_text=_("Including the primary observed animal."),
    )
    no_dependent_young_unknown = models.PositiveIntegerField(
        blank=True, null=True,
        verbose_name=_("Number of dependent_young unknown"),
        help_text=_("Including the primary observed animal."),
    )

    # observation details description
    observation_details = models.TextField(
        blank=True, null=True,
        verbose_name=_("Observation details"),
        help_text=_("Any relevant details of the observation."),
    )

    # secondary signs (select multiple): heard, scats, tracks, diggings, nest/mound,
    # natural hollow, artificial hollow, burrow, feathers/fur/hair/skin,
    # bones, egg/eggshell, shell, feeding residue, fauna run, other see comments
    secondary_signs = models.ManyToManyField(
        SecondarySigns,
        blank=True,
        verbose_name=_("Secondary Signs"),
        help_text=_("Any observed secondary signs of the animal."),
    )

    class Meta:
        """Class options."""

        verbose_name = "Animal Observation"
        verbose_name_plural = "Animal Observations"

    @property
    def tldr(self):
        """A text summary of the observation."""
        return "[{0}] {1} {2}".format(
            self.detection_method,
            self.maturity,
            self.health
        )

    @property
    def sum_adult(self):
        """The sum of all adults encountered."""
        return (
            self.no_adult_male or 0
        ) + (
            self.no_adult_female or 0
        ) + (
            self.no_adult_unknown or 0
        ) or 0

    @property
    def sum_juvenile(self):
        """The sum of all juveniles encountered."""
        return (
            self.no_juvenile_male or 0
        ) + (
            self.no_juvenile_female or 0
        ) + (
            self.no_juvenile_unknown or 0
        ) or 0

    @property
    def sum_dependent_young(self):
        """The sum of all dependent young encountered."""
        return (
            self.no_dependent_young_male or 0
        ) + (
            self.no_dependent_young_female or 0
        ) + (
            self.no_dependent_young_unknown or 0
        ) or 0

    @property
    def sum_observed(self):
        """The sum of all individuals encountered."""
        return self.sum_adult + self.sum_juvenile + self.sum_dependent_young


class SampleType(CodeLabelDescriptionMixin, models.Model):
    """A type of physical sample or specimen."""

    pass


class SampleDestination(CodeLabelDescriptionMixin, models.Model):
    """The destination of a physical sample or specimen."""

    pass


class PermitType(CodeLabelDescriptionMixin, models.Model):
    """The permit type to take a physical sample or specimen."""

    pass


class PhysicalSample(ObservationGroup):
    """Physical sample or specimen taken off an organism."""

    sample_type = models.ForeignKey(
        SampleType,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Sample Type"),
        help_text=_("Add missing values through the data curation portal."),
    )

    sample_label = models.TextField(
        blank=True, null=True,
        verbose_name=_("Sample Label"),
        help_text=_("The label should be unique within the sample type."),
    )

    collector_id = models.TextField(
        blank=True, null=True,
        verbose_name=_("Collector ID"),
        help_text=_("The unique collector ID."),
    )

    sample_destination = models.ForeignKey(
        SampleDestination,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Sample Destination"),
        help_text=_("Add missing values through the data curation portal."),
    )

    permit_type = models.ForeignKey(
        PermitType,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        verbose_name=_("Permit Type"),
        help_text=_("Add missing values through the data curation portal."),
    )

    permit_id = models.TextField(
        blank=True, null=True,
        verbose_name=_("Permit ID"),
        help_text=_("The unique permit ID."),
    )

    class Meta:
        """Class options."""

        verbose_name = "Physical Sample"
        verbose_name_plural = "Physical Samples"

    @property
    def tldr(self):
        """A text summary of the observation."""
        return "{0} {1}".format(
            self.sample_type,
            self.sample_label
        )


class WildlifeIncident(ObservationGroup):
    """A Wildlife incident: injury or death. Currently integrated into AnimalObservation."""

    # health
    # cause of death
    # injuries description
    # actions taken
    # actions required
    pass


# -----------------------------------------------------------------------------
# TEC Uses: FileAtt, HabComp, AreaAss, HabCond, Thr, FireHist, VegClass,             AssSp
# TFA Uses: FileAtt,          AreaAss, HabCond, Thr, FireHist, VegClass, AnimalObs,  AssSp, Specimen, WildlInc
# TFL Uses: FileAtt, HabComp, AreaAss, HabCond, Thr, FireHist,           PlantCount, AssSp, Specimen
