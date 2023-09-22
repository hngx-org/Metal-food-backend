import logging
import secrets
from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import TemplateDoesNotExist, render_to_string

Logger = logging.getLogger()

def abort(code, message=None):
  '''
  Returns an endpoint with an error code and message
  '''
  messages = {
    404: 'The requested resource cannot be found.',
    403: 'Not allowed.',
    422: 'The request cannot be processed.',
    400: 'Bad Request.',
    }
  message = message or messages.get(code, '')
  data = {
    'success': False,
    'message': message,
    'data': None
  }
  return JsonResponse(data, json_dumps_params={'indent': 2}, status=code)

def response(data, status=None):
  '''
  Returns an endpoint with data
  '''
  status = status or 200
  return JsonResponse(data, json_dumps_params={'indent': 2}, safe=False, status=status)




class BaseResponse(object):
    
  data = None
  success = False
  message = None

  def __init__(self, data, exception, message):
    self.data = data
    self.message = str(exception) if exception is not None else message
    self.success = exception is None

  def to_dict(self):
    return {
        'success': self.success,
        'message': self.message,
        'data': self.data,
    }
  

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
    def send_mail(
       self,
       subject: str,
       recipients: list[str],
       context: dict[str, Any] or None,
       template_name: str or None,
       message: str or None = None,
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
        except Exception as error:
            Logger.log(msg=error, level=logging.ERROR)
