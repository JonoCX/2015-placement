import bitly_api
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.utils.encoding import smart_str
import csv

__author__ = 'student'
"""
Utility class that provides some common functionality to one or more views
"""

from core.models import Communication, CommsAudit, Newsletter, Audience

def twitter_link(path, token):
    """
    Usage:
        * Pass the function the full path (url) of the request
        * Pass the access token, https://bitly.com/a/oauth_apps
    :param path: full path of the request to be shortened
    :param token: API access token from registered developer account
    :return: shortened URL
    """
    c = bitly_api.Connection(access_token=token)
    d = c.shorten(path)
    return d['url']

def get_stats():
    """
    Compile the statistics of the website, used on the
    landing page
    :return: dictionary of relevant stats
    """
    total_comm = 0
    not_admin_checked = 0
    ncl_value = 0
    comm_objs = Communication.objects.all().order_by('-created_on')

    for i in comm_objs:
        # Count the total objects
        total_comm += 1

        # If admin_checked is false
        if not i.admin_checked:
            # Increment that counter
            not_admin_checked += 1

        # Sum total value awarded to Newcastle Uni
        ncl_value += i.value_awarded_to_ncl

    audit_objs = CommsAudit.objects.all()
    audited = audit_objs.count()
    unaudited = total_comm - audited

    audience_objs = Audience.objects.all()

    d = {}
    # Sum all of the audited articles that have a shared
    # audience
    for x in audit_objs:
        for y in audience_objs:
            # If the object is stored in both audit_objs and audience_objs
            if x.audience.pk == y.pk:
                # If it's not already stored in the dictionary (d)
                if not str(y.name) in d:
                    # Create entry in dictionary and set value to 1
                    # (must have an object set for that audience)
                    d[str(y.name)] = 1
                # Else, the audience isn't already stored in the dictionary
                else:
                    # Increment the value for that audience
                    d[str(y.name)] += 1

    total_newsletter = Newsletter.objects.all().count()

    # Build a dictionary of statistics gather above
    stats = {
        "total_comm": total_comm,
        "not_admin_checked": not_admin_checked,
        "ncl_value": ncl_value,
        "audited": audited,
        "unaudited": unaudited,
        "comm_objs": comm_objs,
        "total_newsletter": total_newsletter,
        "audit_objs": audit_objs,
        "d": d,
        "audience_objs": audience_objs
    }

    return stats

def send_mail_confirm(communication_instance):
    """
    Send an email confirmation of a new communication
    :param communication_instance: instance of the communication form
    :return: fail_silently will catch errors
    """
    created_by = communication_instance.created_by
    created_on = communication_instance.created_on
    subject = "Comminication Added - %s" % communication_instance.pk
    to_list = ['j.carlton@ncl.ac.uk']
    from_email = 'j.carlton@ncl.ac.uk'

    plain_txt = get_template('core/email/new_communication.txt')
    html = get_template('core/email/new_communication.html')

    d = Context({
        "created_by": created_by,
        "created_on": created_on
    })

    txt_content = plain_txt.render(d)
    html_content = html.render(d)
    msg = EmailMultiAlternatives(subject, txt_content, from_email, to_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)

def audited_article_to_csv(queryset):
    """
    Turn a set of audited articles into a csv
    file
    :param queryset: set of audited articles
    :return: HttpResponse containing csv file
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_audited_articles.csv"'

    writer = csv.writer(response)

    writer.writerow([
        smart_str(u'ID'),
        smart_str(u'Short Desc'),
        smart_str(u'Full Desc'),
        smart_str(u'BH Number'),
        smart_str(u'Value'),
        smart_str(u'Value to NCL'),
        smart_str(u'Start Date'),
        smart_str(u'Duration'),
        smart_str(u'External'),
        smart_str(u'Source'),
        smart_str(u'Level'),
        smart_str(u'Audience'),
    ])

    for obj in queryset:
        writer.writerow([
            smart_str(obj.sent.pk),
            smart_str(obj.sent.short_desc),
            smart_str(obj.sent.full_desc),
            smart_str(obj.sent.bh_number),
            smart_str(obj.sent.value_of_award),
            smart_str(obj.sent.value_awarded_to_ncl),
            smart_str(obj.sent.project_start_date),
            smart_str(obj.sent.duration),
            smart_str(obj.sent.external),
            smart_str(obj.sent.source),
            smart_str(obj.sent.level),
            smart_str(obj.audience)
        ])
    return response
