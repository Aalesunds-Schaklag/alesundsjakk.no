import logging

logger = logging.getLogger(__name__)


class EmailNotConfiguredError(Exception):
    """Raised when email sending is attempted but SMTP is not configured."""
    pass


async def send_magic_link(email: str, token: str) -> None:
    logger.warning("Email not configured — magic link for %s was not sent.", email)
    raise EmailNotConfiguredError(
        "E-post er ikke konfigurert. Kontakt administrator."
    )


async def send_contact_form(name: str, email: str, phone: str, message: str, subject: str = "Kontaktskjema") -> None:
    logger.warning("Email not configured — contact form from %s was not sent.", email)
    raise EmailNotConfiguredError(
        "E-post er ikke konfigurert. Kontakt administrator."
    )
