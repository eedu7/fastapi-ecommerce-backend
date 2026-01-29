from string import Template

from core.settings import settings


def verify_email(token: str, email: str) -> str:
    print("URL", settings.FRONTEND_BASE_URL)
    template = Template(
        """
        <h2>Verify your email</h2>
        <p>Please verify your email by clicking the link below:</p>
        <a href="$verify_email_url?token=$verify_email_token&email=$user_email">
            Verify Email
        </a>
        """
    )
    return template.substitute(
        {
            "verify_email_token": token,
            "user_email": email,
            "verify_email_url": settings.FRONTEND_BASE_URL,
        }
    )
