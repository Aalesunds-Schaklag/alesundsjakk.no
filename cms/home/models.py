from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.api import APIField
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    """Site root page. All content pages live under this."""

    max_count = 1
    subpage_types = ["home.ContentPage"]

    class Meta:
        verbose_name = "Hjemmeside"


class ContentPage(Page):
    """A bilingual content page (Norwegian + English)."""

    title_en = models.CharField(
        "Title (English)", max_length=500, blank=True, default=""
    )
    body_no = RichTextField("Innhold (norsk)", blank=True, default="")
    body_en = RichTextField("Content (English)", blank=True, default="")

    content_panels = Page.content_panels + [
        FieldPanel("title_en"),
        FieldPanel("body_no"),
        FieldPanel("body_en"),
    ]

    api_fields = [
        APIField("title_en"),
        APIField("body_no"),
        APIField("body_en"),
    ]

    parent_page_types = ["home.HomePage"]
    subpage_types = []

    class Meta:
        verbose_name = "Innholdsside"
        verbose_name_plural = "Innholdssider"
