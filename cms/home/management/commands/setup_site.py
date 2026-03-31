from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from home.models import ContentPage, HomePage


class Command(BaseCommand):
    help = "Create initial Wagtail page tree with demo content"

    def handle(self, *args, **options):
        # Get the Wagtail root page (depth=1, always exists after migrate)
        root = Page.objects.get(depth=1)

        # Remove the default "Welcome to your new Wagtail site!" page
        Page.objects.filter(depth=2, slug="home").exclude(
            content_type__model="homepage"
        ).delete()

        # Create or get HomePage
        if not HomePage.objects.exists():
            home = HomePage(title="Aalesunds Schaklag", slug="home")
            root.add_child(instance=home)
            home.save_revision().publish()
            self.stdout.write("Created HomePage")
        else:
            home = HomePage.objects.first()
            self.stdout.write("HomePage already exists")

        # Point default site to our HomePage
        site = Site.objects.filter(is_default_site=True).first()
        if site:
            site.root_page = home
            site.site_name = "Aalesunds Schaklag"
            site.save()
        else:
            Site.objects.create(
                hostname="localhost",
                root_page=home,
                is_default_site=True,
                site_name="Aalesunds Schaklag",
            )

        # Demo content pages
        demo_pages = [
            {
                "title": "Om oss",
                "slug": "om-oss",
                "title_en": "About Us",
                "body_no": (
                    "<h2>Om Aalesunds Schaklag</h2>"
                    "<p>Aalesunds Schaklag ble stiftet i 1913 og er en av de "
                    "eldste sjakklubbene i Norge. Klubben holder til i egne "
                    "lokaler p\u00e5 Steinv\u00e5gvegen 60 p\u00e5 Asp\u00f8ya i \u00c5lesund.</p>"
                    "<p>Klubben arrangerer ukentlige klubbkvelder, turneringer "
                    "gjennom hele \u00e5ret, ungdomssjakk og den \u00e5rlige "
                    "\u00c5lesund Sjakkfestival.</p>"
                ),
                "body_en": (
                    "<h2>About Aalesunds Schaklag</h2>"
                    "<p>Founded in 1913, Aalesunds Schaklag is one of Norway's "
                    "oldest chess clubs. The club is located at Steinv\u00e5gvegen "
                    "60 on Asp\u00f8ya island in \u00c5lesund.</p>"
                    "<p>We host weekly club evenings, tournaments throughout the "
                    "year, youth chess, and the annual \u00c5lesund Chess Festival.</p>"
                ),
            },
            {
                "title": "Festival",
                "slug": "festival",
                "title_en": "Chess Festival",
                "body_no": (
                    "<h2>\u00c5lesund Sjakkfestival</h2>"
                    "<p>\u00c5lesund Sjakkfestival er en \u00e5rlig sjakkfestival "
                    "arrangert av Aalesunds Schaklag. Festivalen har turneringer "
                    "for alle niv\u00e5er, fra nybegynnere til mesterniv\u00e5.</p>"
                    "<p>Programmet og p\u00e5melding publiseres n\u00e5r festivalen "
                    "n\u00e6rmer seg. F\u00f8lg med p\u00e5 nettsiden og v\u00e5re "
                    "sosiale medier for oppdateringer.</p>"
                ),
                "body_en": (
                    "<h2>\u00c5lesund Chess Festival</h2>"
                    "<p>The \u00c5lesund Chess Festival is an annual chess festival "
                    "organized by Aalesunds Schaklag. The festival features "
                    "tournaments for all levels, from beginners to masters.</p>"
                    "<p>The programme and registration will be published as the "
                    "festival approaches. Follow our website and social media "
                    "for updates.</p>"
                ),
            },
            {
                "title": "Lei lokaler",
                "slug": "lokaler",
                "title_en": "Venue Rental",
                "body_no": (
                    "<h2>Lei lokaler</h2>"
                    "<p>Aalesunds Schaklag holder til i Steinv\u00e5gvegen 60, "
                    "6005 \u00c5lesund. Lokalet kan leies ut til arrangementer, "
                    "m\u00f8ter og kurs.</p>"
                    "<p>Lokalet har plass til ca. 40 personer, projektor, "
                    "whiteboard, kj\u00f8kken med kaffemaskin, WiFi og gratis "
                    "parkering.</p>"
                    "<p>Ta kontakt for priser og tilgjengelighet.</p>"
                ),
                "body_en": (
                    "<h2>Venue Rental</h2>"
                    "<p>Aalesunds Schaklag is located at Steinv\u00e5gvegen 60, "
                    "6005 \u00c5lesund. The venue is available for rent for "
                    "events, meetings and courses.</p>"
                    "<p>The venue accommodates approx. 40 people and includes "
                    "a projector, whiteboard, kitchen with coffee machine, "
                    "WiFi and free parking.</p>"
                    "<p>Contact us for pricing and availability.</p>"
                ),
            },
        ]

        for data in demo_pages:
            if ContentPage.objects.filter(slug=data["slug"]).exists():
                self.stdout.write(f"  Page '{data['slug']}' already exists, skipping")
                continue
            page = ContentPage(**data)
            home.add_child(instance=page)
            page.save_revision().publish()
            self.stdout.write(f"  Created page: {data['slug']}")

        self.stdout.write(self.style.SUCCESS("Site setup complete!"))
