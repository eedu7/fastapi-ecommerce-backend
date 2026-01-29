from string import Template


def otp_email(otp: str) -> str:
    template = Template(
        """
        <h2>Your OTP Code<h2>
        <p>Your one-time password is:</p>
        <h1>$otp</h1>
        """
    )
    return template.substitute({"otp": otp})


def verify_email(token: str) -> str:
    template = Template(
        """
        <h2>Verify your email</h2>
        <p>Please verify your email by clicking the link below:</p>
        <a href="https://yourapp.com/verify-email?token=$verify_email_token">
            Verify Email
        </a>
        """
    )
    return template.substitute({"verify_email_token": token})
