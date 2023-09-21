import logging
import secrets
from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import TemplateDoesNotExist, render_to_string

Logger = logging.getLogger()

def generate_token()-> str:
  """Generates 6 digit random token."""
  otp = "".join([f"{secrets.randbelow(10)}" for _ in range(6)])
  return otp



class EmailManagerError(Exception):
    """Raise this error if an error occurs in the email manager."""


class EmailManager:
    def __init__(self) -> None:
       pass


    @classmethod
    async def send_mail(
       self,
       subject: str,
       recipients: list[str],
       context: dict[str, Any] | None,
       template_name: str | None,
       message: str | None = None,
       ) -> None:
        """Send email to invited user's email."""
        if (context and template_name is None) or (template_name and context is None):
          raise EmailManagerError(
             "context set but template_name not set OR template_name set and context not set."
             )
        if (context is None) and (template_name is None) and (message is None):
            raise EmailManagerError(
                "Must set either {context and template_name} or message args."
            )

        html_message: str | None = None

        if context is not None:
            # html message
            try:
                html_message = render_to_string(
                    template_name=template_name, context=context
                )
            except TemplateDoesNotExist as error:
                raise EmailManagerError from error

        try:
            send_mail(
            from_email=settings.EMAIL_HOST_USER,
            subject=subject,
            recipient_list=recipients,
            fail_silently=False,
            message=message,
            html_message=html_message,
        )
            # message = Mail(
            #     from_email='ddummydum11@gmail.com',
            #     to_emails=recipients,
            #     subject=subject,
            #     html_content=html_message
            # )
            # try:
            #     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            #     response = sg.send(message)
            #     print(response.status_code)
            #     print(response.body)
            #     print(response.header)
        except Exception as error:
            Logger.log(msg=error, level=logging.ERROR)
