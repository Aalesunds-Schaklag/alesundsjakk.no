from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from home.models import ContentPage, FunctionalPage, HomePage, PriceItem, PricingPage


class Command(BaseCommand):
    help = "Create Wagtail page tree with real content from old WordPress site"

    def _create_page(self, parent, model, data):
        """Create a page if it doesn't exist yet. Returns (page, created)."""
        slug = data["slug"]
        existing = model.objects.filter(slug=slug).first()
        if existing:
            self.stdout.write(f"  Page '{slug}' already exists, skipping")
            return existing, False
        page = model(**data)
        parent.add_child(instance=page)
        page.save_revision().publish()
        self.stdout.write(f"  Created page: {slug}")
        return page, True

    def handle(self, *args, **options):
        root = Page.objects.get(depth=1)

        # Remove default Wagtail welcome page
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

        # ── Functional pages (Vue routes) ──────────────────────────

        functional_pages = [
            {
                "title": "Bli med",
                "slug": "bli-med",
                "title_en": "Join",
                "icon": "mdi-account-plus",
                "vue_route_name": "join",
                "menu_order": 10,
            },
            {
                "title": "Terminliste",
                "slug": "terminliste",
                "title_en": "Schedule",
                "icon": "mdi-calendar",
                "vue_route_name": "schedule",
                "menu_order": 20,
            },
            {
                "title": "Resultater",
                "slug": "resultater",
                "title_en": "Results",
                "icon": "mdi-trophy",
                "vue_route_name": "results",
                "menu_order": 30,
            },
            {
                "title": "Nyheter",
                "slug": "nyheter",
                "title_en": "News",
                "icon": "mdi-newspaper",
                "vue_route_name": "news",
                "menu_order": 80,
            },
            {
                "title": "Daglig oppgave",
                "slug": "oppgave",
                "title_en": "Daily puzzle",
                "icon": "mdi-puzzle",
                "vue_route_name": "puzzle",
                "menu_order": 90,
            },
        ]

        for data in functional_pages:
            self._create_page(home, FunctionalPage, data)

        # ── Content pages (top-level) ──────────────────────────────

        # Festival
        self._create_page(home, ContentPage, {
            "title": "Sjakkfestival",
            "slug": "festival",
            "title_en": "Chess Festival",
            "icon": "mdi-party-popper",
            "menu_order": 40,
            "body_no": (
                "<h2>Ålesund Sjakkfestival</h2>"
                "<p>Ålesund Sjakkfestival er en årlig sjakkfestival arrangert av "
                "Aalesunds Schaklag. Festivalen trekker spillere fra hele Norge og "
                "utlandet, og tilbyr turneringer for alle nivåer — fra nybegynnere "
                "til mesterspillere.</p>"
                "<h3>Program</h3>"
                "<p>Festivalen inkluderer vanligvis:</p>"
                "<ul>"
                "<li>Åpent hurtigsjakkmesterskap</li>"
                "<li>Åpent lynsjakkmesterskap</li>"
                "<li>Sjakkturneringer for barn og ungdom</li>"
                "<li>Simultanoppvisning</li>"
                "</ul>"
                "<p>Programmet og påmelding publiseres når festivalen nærmer seg. "
                "Følg med på nettsiden og våre sosiale medier for oppdateringer.</p>"
                "<h3>Sted</h3>"
                "<p>Festivalen arrangeres i Aalesunds Schaklag sine lokaler på "
                "Steinvågvegen 60, 6005 Ålesund.</p>"
            ),
            "body_en": (
                "<h2>Ålesund Chess Festival</h2>"
                "<p>The Ålesund Chess Festival is an annual chess festival organised by "
                "Aalesunds Schaklag. The festival attracts players from all over Norway "
                "and abroad, offering tournaments for all levels — from beginners "
                "to master players.</p>"
                "<h3>Programme</h3>"
                "<p>The festival typically includes:</p>"
                "<ul>"
                "<li>Open rapid chess championship</li>"
                "<li>Open blitz chess championship</li>"
                "<li>Chess tournaments for children and youth</li>"
                "<li>Simultaneous exhibition</li>"
                "</ul>"
                "<p>The programme and registration will be published as the festival "
                "approaches. Follow our website and social media for updates.</p>"
                "<h3>Venue</h3>"
                "<p>The festival takes place at Aalesunds Schaklag's premises at "
                "Steinvågvegen 60, 6005 Ålesund.</p>"
            ),
        })

        # Lei lokaler
        self._create_page(home, ContentPage, {
            "title": "Lei lokaler",
            "slug": "lokaler",
            "title_en": "Venue Rental",
            "icon": "mdi-home-city",
            "menu_order": 50,
            "body_no": (
                "<h2>Lei lokaler hos Aalesunds Schaklag</h2>"
                "<p>Aalesunds Schaklag holder til i nyrenoverte lokaler på "
                "Steinvågvegen 60, 6005 Ålesund (Aspøya). Lokalene kan leies "
                "ut til arrangementer, møter, kurs, feiringer og private "
                "tilstelninger.</p>"
                "<h3>Fasiliteter</h3>"
                "<ul>"
                "<li>Plass til ca. 40 personer</li>"
                "<li>Projektor og lerret</li>"
                "<li>Whiteboard</li>"
                "<li>Kjøkken med kaffemaskin og kjøleskap</li>"
                "<li>WiFi</li>"
                "<li>Gratis parkering</li>"
                "<li>Handicaptilgjengelig</li>"
                "</ul>"
                "<h3>Kontakt</h3>"
                "<p>Ta kontakt for priser og tilgjengelighet. "
                "Send forespørsel via kontaktskjemaet eller ring oss på "
                "+47 932 58 938.</p>"
            ),
            "body_en": (
                "<h2>Venue Rental at Aalesunds Schaklag</h2>"
                "<p>Aalesunds Schaklag is located in newly renovated premises at "
                "Steinvågvegen 60, 6005 Ålesund (Aspøya island). The venue is "
                "available for rent for events, meetings, courses, celebrations "
                "and private functions.</p>"
                "<h3>Facilities</h3>"
                "<ul>"
                "<li>Capacity for approx. 40 people</li>"
                "<li>Projector and screen</li>"
                "<li>Whiteboard</li>"
                "<li>Kitchen with coffee machine and refrigerator</li>"
                "<li>WiFi</li>"
                "<li>Free parking</li>"
                "<li>Wheelchair accessible</li>"
                "</ul>"
                "<h3>Contact</h3>"
                "<p>Contact us for pricing and availability. "
                "Send an enquiry via the contact form or call us at "
                "+47 932 58 938.</p>"
            ),
        })

        # Om oss (parent for sub-pages)
        om_oss, _ = self._create_page(home, ContentPage, {
            "title": "Om oss",
            "slug": "om-oss",
            "title_en": "About Us",
            "icon": "mdi-information",
            "menu_order": 60,
            "body_no": (
                "<h2>Om Aalesunds Schaklag</h2>"
                "<p>Aalesunds Schaklag ble stiftet i 1913 og er en av de eldste "
                "sjakklubbene i Norge. Klubben holder til i egne lokaler på "
                "Steinvågvegen 60 på Aspøya i Ålesund.</p>"
                "<p>Klubben har et aktivt og inkluderende miljø for sjakkspillere "
                "i alle aldre og på alle nivåer. Vi tilbyr:</p>"
                "<ul>"
                "<li><b>Klubbkvelder</b> — hver torsdag fra kl. 18:00</li>"
                "<li><b>Turneringer</b> — klassisk, hurtig- og lynsjakk gjennom hele året</li>"
                "<li><b>Ungdomssjakk</b> — trening for barn og ungdom på flere steder i Ålesund-området</li>"
                "<li><b>Ålesund Sjakkfestival</b> — årlig festival åpen for alle</li>"
                "</ul>"
                "<p>Med over 100 år med sjakk i Ålesund er vi stolte over å videreføre "
                "en lang tradisjon. Nye spillere er alltid velkomne — bare møt opp "
                "på en klubbkveld!</p>"
            ),
            "body_en": (
                "<h2>About Aalesunds Schaklag</h2>"
                "<p>Founded in 1913, Aalesunds Schaklag is one of Norway's oldest "
                "chess clubs. The club is located in its own premises at "
                "Steinvågvegen 60 on Aspøya island in Ålesund.</p>"
                "<p>The club offers an active and inclusive environment for chess "
                "players of all ages and skill levels. We offer:</p>"
                "<ul>"
                "<li><b>Club evenings</b> — every Thursday from 18:00</li>"
                "<li><b>Tournaments</b> — classical, rapid and blitz chess throughout the year</li>"
                "<li><b>Youth chess</b> — training for children and youth at several locations in the Ålesund area</li>"
                "<li><b>Ålesund Chess Festival</b> — annual festival open to everyone</li>"
                "</ul>"
                "<p>With over 100 years of chess in Ålesund, we are proud to continue "
                "a long tradition. New players are always welcome — just show up "
                "at a club evening!</p>"
            ),
        })

        # Kontakt
        self._create_page(home, ContentPage, {
            "title": "Kontakt",
            "slug": "kontakt",
            "title_en": "Contact",
            "icon": "mdi-email",
            "menu_order": 70,
            "body_no": (
                "<h2>Kontakt oss</h2>"

                "<h3>Voksenklubben</h3>"
                "<p>Aalesunds Schaklag har en Messenger-gruppe hvor vi deler "
                "relevant sjakkinformasjon om Ålesund. Ta kontakt for å bli "
                "lagt til. Vi legger også ut informasjon på nettsiden og "
                "Facebook-siden vår.</p>"

                "<h3>Ungdomsklubben</h3>"
                "<p>Barneorganisasjonen bruker Spond, hvor treningsinvitasjoner "
                "og påmeldinger håndteres. Be om å bli lagt til for å få "
                "oppdateringer. Informasjon er også tilgjengelig på nettsiden "
                "og Facebook.</p>"

                "<h3>Besøksadresse</h3>"
                "<p>Steinvågvegen 60</p>"
                "<p>6005 Ålesund (Aspøya)</p>"

                "<h3>Kontaktinformasjon</h3>"
                "<p>E-post: <a href='mailto:post@alesundsjakk.no'>post@alesundsjakk.no</a></p>"
                "<p>Telefon: <a href='tel:+4793258938'>+47 932 58 938</a></p>"

                "<h3>Sosiale medier</h3>"
                "<p><a href='https://www.facebook.com/aalesundsschaklag'>Facebook — Aalesunds Schaklag</a></p>"

                "<h3>Utleie</h3>"
                "<p>For utleie av lokaler, se vår <a href='/lokaler'>utleieside</a>.</p>"
            ),
            "body_en": (
                "<h2>Contact us</h2>"

                "<h3>Adult club</h3>"
                "<p>Aalesunds Schaklag has a Messenger group where we share "
                "relevant chess information about Ålesund. Get in touch to be "
                "added. We also post information on our website and Facebook page.</p>"

                "<h3>Youth club</h3>"
                "<p>The children's organisation uses Spond, where training "
                "invitations and sign-ups are managed. Ask to be added to "
                "receive updates. Information is also available on the website "
                "and Facebook.</p>"

                "<h3>Visiting address</h3>"
                "<p>Steinvågvegen 60</p>"
                "<p>6005 Ålesund (Aspøya)</p>"

                "<h3>Contact information</h3>"
                "<p>Email: <a href='mailto:post@alesundsjakk.no'>post@alesundsjakk.no</a></p>"
                "<p>Phone: <a href='tel:+4793258938'>+47 932 58 938</a></p>"

                "<h3>Social media</h3>"
                "<p><a href='https://www.facebook.com/aalesundsschaklag'>Facebook — Aalesunds Schaklag</a></p>"

                "<h3>Venue rental</h3>"
                "<p>For venue rental, see our <a href='/lokaler'>rental page</a>.</p>"
            ),
        })

        # ── Sub-pages under Om oss ─────────────────────────────────

        # Sjakkhistorie
        self._create_page(om_oss, ContentPage, {
            "title": "Sjakkhistorie",
            "slug": "sjakkhistorie",
            "title_en": "Chess History",
            "menu_order": 10,
            "body_no": (
                "<h2>Sjakkhistorie i Ålesund</h2>"
                "<p>Aalesunds Schaklag har eksistert ganske lenge. Her lenker vi "
                "til dokumenter som er knyttet til lagets historie.</p>"

                "<h3>Norgesmesterskapet i sjakk 1958</h3>"
                "<p>I 1958 ble Norgesmesterskapet i sjakk arrangert i Ålesund. "
                "Turneringsprogrammet er digitalisert og tilgjengelig. "
                "Programmet viser at Ålesund hadde en sterk sjakkscene allerede "
                "på 1950-tallet.</p>"

                "<h3>50-årsjubileum 1963</h3>"
                "<p>Da klubben fylte 50 år i 1963, ble det utgitt et jubileumsskrift: "
                "<em>«Aalesunds Schaklag 1913 – 1963»</em>. Heftet dokumenterer "
                "klubbens første femti år med historier, resultater og bilder fra "
                "sjakkmiljøet i Ålesund.</p>"

                "<h3>Artikkel i Ålesund Museum 1977</h3>"
                "<p>Ålesund Museum ga i 1977 ut samlingen <em>«Artikler om byen, "
                "folk og museet»</em>. Arne Skillestad bidro med en artikkel om "
                "sjakkklubben som gir et verdifullt innblikk i klubbens utvikling "
                "fra stiftelsen og fremover.</p>"

                "<p>Disse dokumentene er viktige kilder for å forstå sjakkmiljøet "
                "i Ålesund gjennom mer enn et århundre. Kontakt oss hvis du har "
                "historisk materiale du vil dele.</p>"
            ),
            "body_en": (
                "<h2>Chess History in Ålesund</h2>"
                "<p>Aalesunds Schaklag has been around for quite some time. Here "
                "we link to documents related to the club's history.</p>"

                "<h3>Norwegian Chess Championship 1958</h3>"
                "<p>In 1958 the Norwegian Chess Championship was held in Ålesund. "
                "The tournament programme has been digitised and is available. "
                "The programme shows that Ålesund had a strong chess scene already "
                "in the 1950s.</p>"

                "<h3>50th Anniversary 1963</h3>"
                "<p>When the club celebrated its 50th anniversary in 1963, a "
                "commemorative booklet was published: "
                "<em>'Aalesunds Schaklag 1913 – 1963'</em>. The booklet documents "
                "the club's first fifty years with stories, results and photos from "
                "the chess community in Ålesund.</p>"

                "<h3>Ålesund Museum Article 1977</h3>"
                "<p>Ålesund Museum published in 1977 the collection "
                "<em>'Articles about the city, people and the museum'</em>. "
                "Arne Skillestad contributed an article about the chess club, "
                "providing valuable insight into the club's development from its "
                "founding onwards.</p>"

                "<p>These documents are important sources for understanding the "
                "chess community in Ålesund through more than a century. Contact "
                "us if you have historical material you would like to share.</p>"
            ),
        })

        # Klubbmestere siden 1913
        self._create_page(om_oss, ContentPage, {
            "title": "Klubbmestere siden 1913",
            "slug": "klubbmestere",
            "title_en": "Club Champions since 1913",
            "menu_order": 20,
            "body_no": (
                "<h2>Klubbmestere i Aalesunds Schaklag</h2>"
                "<p>Oversikt over alle klubbmestere fra 1913 til i dag. "
                "Merk at det er et opphold under andre verdenskrig (1940–1944).</p>"
                "<table>"
                "<thead><tr><th>År</th><th>Klubbmester</th></tr></thead>"
                "<tbody>"
                "<tr><td>1913</td><td>M. Gran</td></tr>"
                "<tr><td>1914–1915</td><td>Leif Lund</td></tr>"
                "<tr><td>1916–1917</td><td>A. Ekenes</td></tr>"
                "<tr><td>1918</td><td>C. Vike</td></tr>"
                "<tr><td>1919</td><td>Joh. Keller</td></tr>"
                "<tr><td>1920</td><td>C. Vike</td></tr>"
                "<tr><td>1921–1922</td><td>Joh. Keller</td></tr>"
                "<tr><td>1923</td><td>Gustav Eker</td></tr>"
                "<tr><td>1924</td><td>Odin Fr. Voldsæter</td></tr>"
                "<tr><td>1925–1926</td><td>Arne Strande</td></tr>"
                "<tr><td>1927</td><td>Odd Jarshol</td></tr>"
                "<tr><td>1928–1929</td><td>Odin Fr. Voldsæter</td></tr>"
                "<tr><td>1930–1932</td><td>Gustav Eker</td></tr>"
                "<tr><td>1933</td><td>Einar M. Rødstøl</td></tr>"
                "<tr><td>1934</td><td>Odin Fr. Voldsæter</td></tr>"
                "<tr><td>1935</td><td>Sverre Alstad</td></tr>"
                "<tr><td>1936</td><td>Joh. Keller</td></tr>"
                "<tr><td>1937–1939</td><td>Sverre Alstad</td></tr>"
                "<tr><td colspan='2'><em>Opphold under 2. verdenskrig (1940–1944)</em></td></tr>"
                "<tr><td>1945</td><td>M. Ringstad</td></tr>"
                "<tr><td>1946</td><td>Birger Lied jr.</td></tr>"
                "<tr><td>1947–1948</td><td>Einar M. Rødstøl</td></tr>"
                "<tr><td>1949</td><td>Hjalmar Nilsen</td></tr>"
                "<tr><td>1950</td><td>Henrik Henriksen</td></tr>"
                "<tr><td>1951–1954</td><td>Jørgen Østensen jr.</td></tr>"
                "<tr><td>1955</td><td>Henrik Henriksen</td></tr>"
                "<tr><td>1956–1958</td><td>Arne Skillestad</td></tr>"
                "<tr><td>1959</td><td>Helge Henriksen</td></tr>"
                "<tr><td>1960</td><td>Arne Skillestad</td></tr>"
                "<tr><td>1961</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1962–1964</td><td>Arne Kalvø</td></tr>"
                "<tr><td>1965</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1966–1967</td><td>Olav Drabløs</td></tr>"
                "<tr><td>1968</td><td>Arne Skillestad</td></tr>"
                "<tr><td>1969–1970</td><td>Ulf Narverud</td></tr>"
                "<tr><td>1971–1972</td><td>Arne Skillestad</td></tr>"
                "<tr><td>1973</td><td>Einar Wattø</td></tr>"
                "<tr><td>1974–1975</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1976–1977</td><td>Erling Storeide</td></tr>"
                "<tr><td>1978</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1979</td><td>Arne Skillestad</td></tr>"
                "<tr><td>1980</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1981–1982</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1983</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1984</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1985–1988</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1989</td><td>Roar E. Nakken</td></tr>"
                "<tr><td>1990–1992</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1993</td><td>Roar Naalsund</td></tr>"
                "<tr><td>1994–1995</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1996</td><td>Siebe van Albada</td></tr>"
                "<tr><td>1997</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1998–2001</td><td>Håvard Ramstad</td></tr>"
                "<tr><td>2002–2005</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>2006–2008</td><td>Rafael T. Gonzalez</td></tr>"
                "<tr><td>2009–2010</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>2011–2013</td><td>Adel Gharebagi Fard</td></tr>"
                "<tr><td>2014–2017</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>2018–2020</td><td>Mathias Unneland</td></tr>"
                "<tr><td>2021</td><td>Åge Dyb Hagerup</td></tr>"
                "</tbody>"
                "</table>"
            ),
            "body_en": (
                "<h2>Club Champions of Aalesunds Schaklag</h2>"
                "<p>Complete list of club champions from 1913 to the present day. "
                "Note the hiatus during World War II (1940–1944).</p>"
                "<table>"
                "<thead><tr><th>Year</th><th>Champion</th></tr></thead>"
                "<tbody>"
                "<tr><td>1913</td><td>M. Gran</td></tr>"
                "<tr><td>1914–1915</td><td>Leif Lund</td></tr>"
                "<tr><td>1916–1917</td><td>A. Ekenes</td></tr>"
                "<tr><td>1918</td><td>C. Vike</td></tr>"
                "<tr><td>1919</td><td>Joh. Keller</td></tr>"
                "<tr><td>1920</td><td>C. Vike</td></tr>"
                "<tr><td>1921–1922</td><td>Joh. Keller</td></tr>"
                "<tr><td>1923</td><td>Gustav Eker</td></tr>"
                "<tr><td>1924</td><td>Odin Fr. Voldsæter</td></tr>"
                "<tr><td>1925–1926</td><td>Arne Strande</td></tr>"
                "<tr><td>1927</td><td>Odd Jarshol</td></tr>"
                "<tr><td>1928–1929</td><td>Odin Fr. Voldsæter</td></tr>"
                "<tr><td>1930–1932</td><td>Gustav Eker</td></tr>"
                "<tr><td>1933</td><td>Einar M. Rødstøl</td></tr>"
                "<tr><td>1934</td><td>Odin Fr. Voldsæter</td></tr>"
                "<tr><td>1935</td><td>Sverre Alstad</td></tr>"
                "<tr><td>1936</td><td>Joh. Keller</td></tr>"
                "<tr><td>1937–1939</td><td>Sverre Alstad</td></tr>"
                "<tr><td colspan='2'><em>Hiatus during World War II (1940–1944)</em></td></tr>"
                "<tr><td>1945</td><td>M. Ringstad</td></tr>"
                "<tr><td>1946</td><td>Birger Lied jr.</td></tr>"
                "<tr><td>1947–1948</td><td>Einar M. Rødstøl</td></tr>"
                "<tr><td>1949</td><td>Hjalmar Nilsen</td></tr>"
                "<tr><td>1950</td><td>Henrik Henriksen</td></tr>"
                "<tr><td>1951–1954</td><td>Jørgen Østensen jr.</td></tr>"
                "<tr><td>1955</td><td>Henrik Henriksen</td></tr>"
                "<tr><td>1956–1958</td><td>Arne Skillestad</td></tr>"
                "<tr><td>1959</td><td>Helge Henriksen</td></tr>"
                "<tr><td>1960</td><td>Arne Skillestad</td></tr>"
                "<tr><td>1961</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1962–1964</td><td>Arne Kalvø</td></tr>"
                "<tr><td>1965</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1966–1967</td><td>Olav Drabløs</td></tr>"
                "<tr><td>1968</td><td>Arne Skillestad</td></tr>"
                "<tr><td>1969–1970</td><td>Ulf Narverud</td></tr>"
                "<tr><td>1971–1972</td><td>Arne Skillestad</td></tr>"
                "<tr><td>1973</td><td>Einar Wattø</td></tr>"
                "<tr><td>1974–1975</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1976–1977</td><td>Erling Storeide</td></tr>"
                "<tr><td>1978</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1979</td><td>Arne Skillestad</td></tr>"
                "<tr><td>1980</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1981–1982</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1983</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1984</td><td>Emil Grønningsæter</td></tr>"
                "<tr><td>1985–1988</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1989</td><td>Roar E. Nakken</td></tr>"
                "<tr><td>1990–1992</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1993</td><td>Roar Naalsund</td></tr>"
                "<tr><td>1994–1995</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1996</td><td>Siebe van Albada</td></tr>"
                "<tr><td>1997</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>1998–2001</td><td>Håvard Ramstad</td></tr>"
                "<tr><td>2002–2005</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>2006–2008</td><td>Rafael T. Gonzalez</td></tr>"
                "<tr><td>2009–2010</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>2011–2013</td><td>Adel Gharebagi Fard</td></tr>"
                "<tr><td>2014–2017</td><td>Øyvind Antonsen</td></tr>"
                "<tr><td>2018–2020</td><td>Mathias Unneland</td></tr>"
                "<tr><td>2021</td><td>Åge Dyb Hagerup</td></tr>"
                "</tbody>"
                "</table>"
            ),
        })

        # Kontingenter (PricingPage)
        kontingenter, created = self._create_page(om_oss, PricingPage, {
            "title": "Kontingenter og turneringsavgifter",
            "slug": "kontingenter",
            "title_en": "Fees and Membership",
            "menu_order": 30,
            "body_no": (
                "<h2>Kontingenter og turneringsavgifter</h2>"

                "<h3>Årsmedlemskap</h3>"
                "<p>Medlemskapet inkluderer medlemskap i Norges Sjakkforbund (NSF), "
                "som gir rett til å delta i ratede turneringer og motta "
                "sjakkpublikasjoner.</p>"

                "<h3>Månedsabonnement «Alt inkludert»</h3>"
                "<p>Medlemmer som betaler månedskontingent er fritatt for "
                "turneringsavgifter i interne klubbkonkurranser (mesterskap i "
                "klassisk, hurtig- og lynsjakk, samt vårturneringer).</p>"

                "<h3>Turneringsavgifter</h3>"
                "<p>Turneringsavgifter gjelder for interne klubbkonkurranser. "
                "Spesifikke beløp varierer etter turnering og annonseres på forhånd. "
                "Fra 2017 er den tidligere kveldsavgiften (50 kr per torsdagsbesøk) "
                "innarbeidet i turneringsprisene.</p>"

                "<h3>Betaling</h3>"
                "<p>Kontonummer: 3900.34.65857</p>"
                "<p>Vipps: 79307</p>"
                "<p>Kontakt: <a href='mailto:hans.furstrand@yahoo.no'>hans.furstrand@yahoo.no</a></p>"
            ),
            "body_en": (
                "<h2>Fees and Membership</h2>"

                "<h3>Annual Membership</h3>"
                "<p>Membership includes membership in the Norwegian Chess Federation "
                "(NSF), enabling participation in rated tournaments and receiving "
                "chess publications.</p>"

                "<h3>Monthly Subscription 'All Inclusive'</h3>"
                "<p>Members paying the monthly subscription are exempt from "
                "tournament fees in internal club competitions (championships in "
                "classical, rapid and blitz chess, and spring tournaments).</p>"

                "<h3>Tournament Fees</h3>"
                "<p>Tournament fees apply to internal club competitions. "
                "Specific amounts vary by tournament and are announced beforehand. "
                "Since 2017, the former evening fee (50 NOK per Thursday visit) "
                "is incorporated into tournament pricing.</p>"

                "<h3>Payment</h3>"
                "<p>Bank account: 3900.34.65857</p>"
                "<p>Vipps: 79307</p>"
                "<p>Contact: <a href='mailto:hans.furstrand@yahoo.no'>hans.furstrand@yahoo.no</a></p>"
            ),
        })

        # Add price items if the page was just created
        if created and kontingenter.pk:
            price_items = [
                {
                    "category_no": "Årsmedlemskap voksen",
                    "category_en": "Annual membership adult",
                    "price_nok": 1000,
                    "description_no": "Inkluderer NSF-medlemskap",
                    "description_en": "Includes NSF membership",
                },
                {
                    "category_no": "Årsmedlemskap junior (under 20)",
                    "category_en": "Annual membership junior (under 20)",
                    "price_nok": 500,
                    "description_no": "Inkluderer NSF-medlemskap",
                    "description_en": "Includes NSF membership",
                },
                {
                    "category_no": "Årsmedlemskap barn (under 13)",
                    "category_en": "Annual membership children (under 13)",
                    "price_nok": 250,
                    "description_no": "Inkluderer NSF-medlemskap",
                    "description_en": "Includes NSF membership",
                },
                {
                    "category_no": "Månedsabonnement voksen",
                    "category_en": "Monthly subscription adult",
                    "price_nok": 250,
                    "description_no": "Per måned. Fritatt for turneringsavgifter.",
                    "description_en": "Per month. Exempt from tournament fees.",
                },
                {
                    "category_no": "Månedsabonnement barn/ungdom (under 20)",
                    "category_en": "Monthly subscription youth (under 20)",
                    "price_nok": 100,
                    "description_no": "Per måned. Fritatt for turneringsavgifter.",
                    "description_en": "Per month. Exempt from tournament fees.",
                },
            ]
            for i, item_data in enumerate(price_items):
                PriceItem.objects.create(
                    page=kontingenter, sort_order=i, **item_data
                )
            self.stdout.write(f"  Added {len(price_items)} price items to kontingenter")

        # Klubbdommere
        self._create_page(om_oss, ContentPage, {
            "title": "Klubbdommere",
            "slug": "klubbdommere",
            "title_en": "Club Referees",
            "menu_order": 40,
            "body_no": (
                "<h2>Klubbdommere</h2>"
                "<p>Aalesunds Schaklag har en liste over medlemmer som har "
                "gjennomført dommeropplæring. Listen er ikke fullstendig "
                "oppdatert etter vårt siste dommerkurs.</p>"
                "<p>Norges Sjakkforbund (NSF) arrangerer jevnlig kurs for "
                "klubbdommere. Kurset gir grunnleggende kompetanse i "
                "turneringsregler og -ledelse, og er en viktig ressurs "
                "for å kunne gjennomføre turneringer på en god måte.</p>"
                "<h3>Bli klubbdommer</h3>"
                "<p>Vi oppfordrer medlemmer som har gjennomført dommeropplæring "
                "til å registrere seg slik at listen kan holdes oppdatert. "
                "Ta kontakt med klubben hvis du ønsker å bli lagt til.</p>"
                "<p>Er du interessert i å ta dommerkurs? Følg med på "
                "NSF sine nettsider for kommende kurs, eller ta kontakt "
                "med klubben for mer informasjon.</p>"
            ),
            "body_en": (
                "<h2>Club Referees</h2>"
                "<p>Aalesunds Schaklag maintains a list of members who have "
                "completed referee training. The list is not fully up to date "
                "following our most recent referee course.</p>"
                "<p>The Norwegian Chess Federation (NSF) regularly organises "
                "courses for club referees. The course provides basic competence "
                "in tournament rules and management, and is an important resource "
                "for running tournaments properly.</p>"
                "<h3>Become a club referee</h3>"
                "<p>We encourage members who have completed referee training to "
                "register so that the list can be kept up to date. Contact the "
                "club if you wish to be added.</p>"
                "<p>Interested in taking a referee course? Follow the NSF website "
                "for upcoming courses, or contact the club for more information.</p>"
            ),
        })

        self.stdout.write(self.style.SUCCESS("Site setup complete!"))
