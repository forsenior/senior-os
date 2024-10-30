import re

from validate_email import validate_email

# Regex source: https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
_url_regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class Validators:

    @staticmethod
    def validate_email(value: str):
        return validate_email(email_address=value,
                              check_regex=True,
                              check_mx=True,
                              from_address='my@from.addr.ess',
                              helo_host='my.host.name',
                              smtp_timeout=10,
                              dns_timeout=10,
                              use_blacklist=True)

    @staticmethod
    def validate_url(value: str):
        value = ''.join(e for e in value if e != ',' and e != ' ' and e != '\'')
        if re.match(_url_regex, value) is not None:
            return True

        return False
