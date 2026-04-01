from django.db import models
from modelcluster.fields import ParentalKey
from rest_framework.fields import Field
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.models import Orderable, Page


class HomePage(Page):
    """Site root page. All content pages live under this."""

    max_count = 1
    subpage_types = ["home.ContentPage", "home.FunctionalPage"]

    class Meta:
        verbose_name = "Hjemmeside"


class ContentPage(Page):
    """A bilingual content page (Norwegian + English) with navigation support."""

    title_en = models.CharField(
        "Title (English)", max_length=500, blank=True, default=""
    )
    body_no = RichTextField("Innhold (norsk)", blank=True, default="")
    body_en = RichTextField("Content (English)", blank=True, default="")
    icon = models.CharField(
        "Ikon (MDI)", max_length=50, blank=True, default="",
        help_text="Material Design icon name, e.g. mdi-information",
    )
    show_in_menu = models.BooleanField("Vis i meny", default=True)
    menu_order = models.IntegerField(
        "Sortering i meny", default=0,
        help_text="Lavere tall = vises først",
    )

    content_panels = Page.content_panels + [
        FieldPanel("title_en"),
        FieldPanel("body_no"),
        FieldPanel("body_en"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("icon"),
        FieldPanel("show_in_menu"),
        FieldPanel("menu_order"),
    ]

    api_fields = [
        APIField("title_en"),
        APIField("body_no"),
        APIField("body_en"),
        APIField("icon"),
        APIField("show_in_menu"),
        APIField("menu_order"),
    ]

    parent_page_types = ["home.HomePage", "home.ContentPage"]
    subpage_types = ["home.ContentPage", "home.PricingPage"]

    class Meta:
        verbose_name = "Innholdsside"
        verbose_name_plural = "Innholdssider"


class FunctionalPage(Page):
    """A page representing a Vue route. Appears in navigation but content comes from Vue."""

    title_en = models.CharField(
        "Title (English)", max_length=500, blank=True, default=""
    )
    icon = models.CharField(
        "Ikon (MDI)", max_length=50, blank=True, default="",
        help_text="Material Design icon name, e.g. mdi-calendar",
    )
    vue_route_name = models.CharField(
        "Vue route name", max_length=100,
        help_text="Named route in Vue router, e.g. 'schedule'",
    )
    show_in_menu = models.BooleanField("Vis i meny", default=True)
    menu_order = models.IntegerField(
        "Sortering i meny", default=0,
        help_text="Lavere tall = vises først",
    )

    content_panels = Page.content_panels + [
        FieldPanel("title_en"),
        FieldPanel("icon"),
        FieldPanel("vue_route_name"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("show_in_menu"),
        FieldPanel("menu_order"),
    ]

    api_fields = [
        APIField("title_en"),
        APIField("icon"),
        APIField("vue_route_name"),
        APIField("show_in_menu"),
        APIField("menu_order"),
    ]

    parent_page_types = ["home.HomePage", "home.ContentPage"]
    subpage_types = []

    class Meta:
        verbose_name = "Funksjonsside"
        verbose_name_plural = "Funksjonssider"


class PriceItemSerializer(Field):
    """Serializes PriceItem orderables for the Wagtail API."""

    def to_representation(self, value):
        return [
            {
                "category_no": item.category_no,
                "category_en": item.category_en,
                "price_nok": item.price_nok,
                "description_no": item.description_no,
                "description_en": item.description_en,
            }
            for item in value.all()
        ]


class PriceItem(Orderable):
    """A single price/fee line item."""

    page = ParentalKey("home.PricingPage", related_name="price_items")
    category_no = models.CharField("Kategori (norsk)", max_length=200)
    category_en = models.CharField(
        "Category (English)", max_length=200, blank=True, default=""
    )
    price_nok = models.IntegerField("Pris (NOK)")
    description_no = models.CharField(
        "Beskrivelse (norsk)", max_length=500, blank=True, default=""
    )
    description_en = models.CharField(
        "Description (English)", max_length=500, blank=True, default=""
    )

    panels = [
        FieldPanel("category_no"),
        FieldPanel("category_en"),
        FieldPanel("price_nok"),
        FieldPanel("description_no"),
        FieldPanel("description_en"),
    ]

    class Meta(Orderable.Meta):
        verbose_name = "Prislinje"
        verbose_name_plural = "Prislinjer"


class PricingPage(ContentPage):
    """Content page with additional structured pricing data."""

    content_panels = ContentPage.content_panels + [
        InlinePanel("price_items", label="Priser"),
    ]

    api_fields = ContentPage.api_fields + [
        APIField("price_items", serializer=PriceItemSerializer()),
    ]

    parent_page_types = ["home.ContentPage", "home.HomePage"]
    subpage_types = []

    class Meta:
        verbose_name = "Prisside"
        verbose_name_plural = "Prissider"
