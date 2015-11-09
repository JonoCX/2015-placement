from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import csv
from django.utils.encoding import smart_str

__author__ = 'Jonathan Carlton'

from core.forms import *
from core.models import *

@login_required
def view_communcation(request):
    tags = Tags.objects.all()
    notes = Notes.objects.all()
    source = Sources.objects.all()
    queryset = Communication.objects.select_related("individuals", "collaborators").all()

    tag_form = TagForm(request.POST or None)
    if tag_form.is_valid():
        tag_form.save()

    notes_form = NotesForm(request.POST or None)
    if notes_form.is_valid():
        note_instance = notes_form.save(commit=False)
        note_instance.save()

    # CSV file
    if request.method == 'POST':
        ids = request.POST.getlist('select')
        queryset = Communication.objects.filter(id__in=ids)
        response = articles_to_csv(queryset)
        return response

    context = {
        "tag_form": tag_form,
        "notes_form": notes_form,
        "queryset": queryset,
        "tags": tags,
        "notes": notes,
        "source": source
    }

    return render(request, "core/tables/view_comm.html", context)

@login_required
def view_audience(request):
    queryset = Audience.objects.all()
    context = {
        "queryset": queryset,
    }
    return render(request, "core/tables/view_audience.html", context)

@login_required
def view_sources(request):
    queryset = Sources.objects.all()
    context = {
        "queryset": queryset,
    }
    return render(request, "core/tables/view_sources.html", context)

@login_required
def view_user_profiles(request):
    queryset = UserProfile.objects.all()
    context = {
        "queryset": queryset,
    }
    return render(request, "core/tables/view_user_profile.html", context)

@login_required
def view_comms_audit(request):
    queryset = CommsAudit.objects.all()
    audience = Audience.objects.all()
    context = {
        "queryset": queryset,
        "audience": audience
    }
    return render(request, "core/tables/view_comms_audit.html", context)

@login_required
def view_notes(request):
    queryset = Notes.objects.all()
    context = {
        "queryset": queryset,
    }
    return render(request, "core/tables/view_notes.html", context)

@login_required
def view_tags(request):
    queryset = Tags.objects.all()
    context = {
        "queryset": queryset,
    }
    return render(request, "core/tables/view_tags.html", context)

@login_required
def view_newsletter_table(request):
    queryset = Newsletter.objects.all()
    context = {
        "queryset": queryset
    }
    return render(request, "core/tables/view_newsletter.html", context)

@login_required
def audit_trail(request):
    queryset = CommsAudit.history.all()
    context = {
        "queryset": queryset
    }
    return render(request, "core/tables/view_audit_trail.html", context)

def articles_to_csv(queryset):
    """
    Written specfically for the view_comm view
    :param queryset: set of articles
    :return: HttpResponse
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_articles.csv"'

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
        smart_str(u'Individuals'),
        smart_str(u'External'),
        smart_str(u'Source'),
        smart_str(u'Level'),
    ])

    for i in queryset:
        writer.writerow([
            smart_str(i.pk),
            smart_str(i.short_desc),
            smart_str(i.full_desc),
            smart_str(i.bh_number),
            smart_str(i.value_of_award),
            smart_str(i.value_awarded_to_ncl),
            smart_str(i.project_start_date),
            smart_str(i.duration),
            smart_str(i.individuals.all()),
            smart_str(i.external),
            smart_str(i.source),
            smart_str(i.level)
        ])
    return response
