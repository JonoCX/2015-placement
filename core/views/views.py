
__author__ = "Jonathan"
import time

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from core.forms import *
from core.models import *
from core.util import *
from core.views.table_views import view_communcation


def get_user(request):
    return {"profile": UserProfile.objects.get(username=request.user.username)}

@login_required
def index(request):
    stats = get_stats()
    return render(request, "core/landing.html", context_instance=RequestContext(
        request,
        stats,
        [get_user]
    ))

def login(request):
    stats = get_stats()
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                u_obj = User.objects.get(username=u)
                profile = UserProfile.objects.get(username=u_obj.username)
                profile.login_count += 1 # Increment login counter
                profile.last_login = time.strftime("%m/%d/%Y")
                profile.save()

                return render(request, "core/landing.html", context_instance=RequestContext(
                    request,
                    stats,
                    [get_user]
                ))
            else:
                not_active = True
                return render(request, "login.html", {"not_active": not_active})
        else:
            invalid_login = True
            return render(request, "login.html", {"invalid_login": invalid_login})
    else:
        if request.user.is_authenticated():
            return render(request, "core/landing.html", context_instance=RequestContext(
                request,
                stats,
                [get_user]
            ))
        else:
            return render(request, "login.html", {})

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def audience(request):
    form = AudienceForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = AudienceForm()

    return render(
        request,
        "core/forms/audience.html",
        context_instance=RequestContext(
            request,
            {"form": form},
            [get_user]
        )
    )

@login_required
def commsAudit(request, audience_id):
    if request.method == 'POST':
        queryset = Newsletter.objects.all()
        return render(
            request,
            "core/newsletter.html",
            context_instance=RequestContext(
                request,
                {"queryset": queryset},
                [get_user]
            )
        )

    # Build a list of the audience primary keys
    a_pk = []
    for i in Audience.objects.all():
        a_pk.append(str(i.pk))

    # If the param id is in the list of primary keys
    if audience_id in a_pk:
        data = CommsAudit.objects.select_related('audience').filter(audience_id=audience_id)
        is_newsletter = False
        audience_obj = Audience.objects.get(pk=audience_id)
        if audience_obj.name == 'Newsletter':
            is_newsletter = True

        context = {
            "data": data,
            "is_newsletter": is_newsletter,
        }
        return render(
            request,
            "core/forms/comms_audit.html",
            context_instance=RequestContext(
                request,
                context,
                [get_user]
            )
        )
    # else, render all CommsAudit objects
    else:
        data = CommsAudit.objects.all()
        context = {"data": data}
        return render(
            request,
            "core/forms/comms_audit.html",
            context_instance=RequestContext(
                request,
                context,
                [get_user]
            )
        )

@login_required
def userProfile(request):
    context = {}
    if request.user.is_authenticated():
        profile = UserProfile.objects.get(username=request.user.username)
        form = UserProfileForm(instance=profile)
        context = {
            "form": form,
        }
    if request.method == 'POST':
        form = UserProfileForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.login_count = 1
            instance.save()
            form = UserProfileForm()
            context = {
                "form": form,
            }

    return render(
        request,
        "core/forms/user_profile.html",
        context_instance=RequestContext(
            request,
            context,
            [get_user]
        )
    )

# Set global variables to save new tags and notes


@login_required
def communication(request):
    # Global tag/note variables to save when posted before the comm form
    global global_tag
    global_tag = None
    global global_note
    global_note = None
    if request.method == 'POST':
        if 'name' in request.POST:
            name = request.POST.get('name')
            tag = Tags.objects.create(name=name)
            # global global_tag
            global_tag = tag
            print global_tag

        if 'title' in request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            created_by = UserProfile.objects.get(username=request.user.username)
            created_on = time.strftime("%Y-%m-%d")
            note = Notes.objects.create(
                title=title,
                content=content,
                created_by=created_by,
                created_on=created_on
            )
            # global global_note
            global_note = note

        c_form = CommunicationForm(request.POST or None)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.created_by = UserProfile.objects.get(username=request.user.username)
            instance.created_on = time.strftime("%Y-%m-%d")
            if request.user.is_superuser:
                instance.save()

                # Fetch the newest communication (article)
                obj = Communication.objects.all().order_by('-id')[:1].get()

                # If there is something stored in global_tag
                if global_tag:
                    # Attach it to the newest communication (article)
                    obj.tags.add(global_tag)

                    # global global_tag
                    global_tag = None
                if global_note:
                    obj.notes.add(global_note)
                    # global global_note
                    global_note = None
            else:
                # Send an email to super user to alert them that there has been a new Article added
                send_mail_confirm(instance)
                instance.save()
                obj = Communication.objects.all().order_by('-id')[:1].get()
                if global_tag:
                    obj.tags.add(global_tag)
                    # global global_tag
                    global_tag = None
                if global_note:
                    obj.notes.add(global_note)
                    # global global_note
                    global_note = None
            context = {
                "t_form": TagForm(),
                "n_form": NotesForm(),
                "c_form": CommunicationForm()
            }
            return render(
                request,
                "core/forms/communication.html",
                context_instance=RequestContext(
                    request,
                    context,
                    [get_user]
                )
            )

        c_form = CommunicationForm()
        t_form = TagForm()
        n_form = NotesForm()

        context = {
            "t_form": t_form,
            "n_form": n_form,
            "c_form": c_form
        }
    else:
        t_form = TagForm()
        n_form = NotesForm()
        c_form = CommunicationForm()
        context = {
            "t_form": t_form,
            "n_form": n_form,
            "c_form": c_form
        }

    return render(
        request,
        "core/forms/communication.html",
        context_instance=RequestContext(
            request,
            context,
            [get_user]
        )
    )

@login_required
def sources(request):
    form = SourcesForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = SourcesForm()

    return render(
        request,
        "core/forms/sources.html",
        context_instance=RequestContext(
            request,
            {"form": form},
            [get_user]
        )
    )

@login_required
def tags(request):
    form = TagForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = TagForm()

    return render(
        request,
        "core/forms/tags.html",
        context_instance=RequestContext(
            request,
            {"form": form},
            [get_user]
        )
    )

@login_required
def notes(request):
    if request.method == 'POST':
        n_form = NotesForm(request.POST or None)
        if n_form.is_valid():
            instance = n_form.save(commit=False)
            instance.created_by = UserProfile.objects.get(username=request.user.username)
            instance.created_on = time.strftime("%Y-%m-%d")
            instance.save()
        n_form = NotesForm()

        context = {
            "n_form": n_form
        }

        return render(
            request,
            "core/forms/notes.html",
            context_instance=RequestContext(
                request,
                context,
                [get_user]
            )
        )
    else:
        n_form = NotesForm()
        context = {
            "n_form": n_form
        }

        return render(
            request,
            "core/forms/notes.html",
            context_instance=RequestContext(
                request,
                context,
                [get_user]
            )
        )


@login_required
def push_to_newsletter(request):
    form = NewsletterForm()
    context = {
        "form": form
    }

    if request.method == 'POST':
        form = NewsletterForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            if Newsletter.objects.filter(audit_id=instance.audit.pk):
                error_stored = True
                context = {
                    "form": form,
                    "error_stored": error_stored
                }
                return render(
                    request,
                    "core/forms/push_newsletter.html",
                    context_instance=RequestContext(
                        request,
                        context,
                        [get_user]
                    )
                )
            else:
                comm_obj = instance.audit.sent
                url = request.get_full_path()
                split_url = url.split('/push')
                a = split_url[0]
                a += '/external/%s' % comm_obj.pk
                # TODO Will need changing; hard coded link + access token linked to my account (Jonathan)
                tiny_link = twitter_link('http://127.0.0.1:8000/' + a, 'afc22c3b2a28c504f9bff9cfcc02f92612616251')
                instance.link = tiny_link
                instance.save()
                form = NewsletterForm()
                context = {
                    "form": form
                }

    return render(
        request,
        "core/forms/push_newsletter.html",
        context_instance=RequestContext(
            request,
            context,
            [get_user]
        )
    )

@login_required
def save_audit(request):
    form = CommunicationForm(request.POST or None)
    context = {}
    if form.is_valid():
        instance = form.save(commit=False)
        instance.created_by = UserProfile.objects.get(username=request.user.username)
        instance.admin_checked = True
        instance.save()

        form = CommsAuditForm(initial={'sent': Communication.objects.get(pk=form.pk)})
        context = {
            "form": form
        }

    return render(
        request,
        "core/forms/comms_audit.html",
        context_instance=RequestContext(
            request,
            context,
            [get_user]
        )
    )

@login_required
def view_newsletter_email(request):
    queryset = Newsletter.objects.all()
    context = {
        "queryset": queryset
    }
    return render(
        request,
        "core/email/newsletter_email.html",
        context
    )

def view_newsletter(request):
    queryset = Newsletter.objects.all()
    context = {"queryset": queryset}
    return render(
        request,
        "core/newsletter.html",
        context
    )

def communication_publish(request, comm_id):
    comm = Communication.objects.get(pk=comm_id)
    context = {
        "comm": comm
    }
    return render(
        request,
        "core/comm_instance.html",
        context
    )

@login_required
def article_approval(request, article_id):
    comm_objs = Communication.objects.all()
    article = comm_objs.get(pk=article_id)

    # Build array of none admin checked articles
    queryset = []
    for i in comm_objs:
        if not i.admin_checked:
            queryset.append(i)
            print i.tags.all()

    if CommsAudit.objects.filter(sent_id=article.pk):
        return render(
            request,
            "core/errors/article_already_audited.html",
            context_instance=RequestContext(
                request,
                {"queryset": queryset},
                [get_user]
            )
        )

    # Build a dictionary of all the levels
    levels = {}
    k = 0
    for i, j in LEVEL:
        levels[k] = i
        k += 1

    if request.method == 'POST':
        form = CommsAuditForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            article.admin_checked = True
            article.save()
            instance.sent_id = article.pk
            instance.sent_by = UserProfile.objects.get(username=request.user.username)
            instance.save()
            if instance.audience.name == 'Newsletter':
                path = 'http://127.0.0.1:8000/external/' + str(article.pk)
                link = twitter_link(path, 'afc22c3b2a28c504f9bff9cfcc02f92612616251')
                news_obj = Newsletter.objects.create(audit=instance, link=link)
                news_obj.save()

            stats = get_stats()
            return render(request, "core/landing.html", context_instance=RequestContext(
                request,
                stats,
                [get_user]
            ))
    else:
        form = CommsAuditForm()
        context = {
            "queryset": queryset,
            "article": article,
            "form": form,
            "levels": levels,
        }

    return render(
        request,
        "core/article_approval.html",
        context_instance=RequestContext(
            request,
            context,
            [get_user]
        )
    )

@login_required
def export_approved_to_csv(request):
    objects = CommsAudit.objects.all()

    if request.method == 'POST':
        ids = request.POST.getlist('select')
        queryset = CommsAudit.objects.select_related('sent').filter(id__in=ids)
        response = audited_article_to_csv(queryset)
        return response

    return render(
        request,
        "core/export_csv.html",
        context_instance=RequestContext(
            request,
            {"objects": objects},
            [get_user]
        )
    )

@login_required
def export_all_to_csv(request):
    queryset = Communication.objects.all()
    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="all_stored_articles.csv"'
        writer = csv.writer(response)
        writer.writerow([
            smart_str(u'ID'),
            smart_str(u'Short Desc'),
            smart_str(u'Full Desc'),
            smart_str(u'BH Number'),
            smart_str(u'Value of Award'),
            smart_str(u'Value Awarded to NCL'),
            smart_str(u'Start Date'),
            smart_str(u'Duration'),
            smart_str(u'Individuals'),
            smart_str(u'External'),
            smart_str(u'Created By'),
            smart_str(u'Created On'),
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
                smart_str(i.created_by),
                smart_str(i.created_on),
                smart_str(i.source),
                smart_str(i.level)
            ])
        return response

    return render(
        request,
        "core/tables/view_comm.html",
        context_instance=RequestContext(
            request,
            {"queryset": queryset},
            [get_user]
        )
    )

@login_required
def unapproved_articles(request):
    queryset = Communication.objects.all()
    return render(
        request,
        "core/unapproved_articles.html",
        context_instance=RequestContext(
            request,
            {"queryset": queryset},
            [get_user]
        )
    )

@login_required
def edit_article(request, article_id, flag=None):
    article = Communication.objects.get(pk=article_id)
    source = Sources.objects.values()

    context = {
        "article": article,
        "source": source
    }
    return render(
        request,
        "core/edit.html",
        context_instance=RequestContext(
            request,
            context,
            [get_user]
        )
    )

@login_required
def delete_article(request, article_id):
    article = Communication.objects.get(pk=article_id)

    if request.method == 'POST':
        article.delete()
        tag_form = TagForm()
        notes_form = NotesForm()
        queryset = Communication.objects.select_related("individuals", "collaborators").all()
        tags = Tags.objects.all()
        notes = Notes.objects.all()
        source = Sources.objects.all()
        context = {
            "tag_form": tag_form,
            "notes_form": notes_form,
            "queryset": queryset,
            "tags": tags,
            "notes": notes,
            "source": source
        }
        return render(
            request,
            "core/tables/view_comm.html",
            context
        )

    context = {
        "article": article
    }

    return render(
        request,
        "core/delete.html",
        context_instance=RequestContext(
            request,
            context,
            [get_user]
        )
    )