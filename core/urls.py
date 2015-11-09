__author__ = 'student'

from django.conf.urls import url, patterns
from views import views, update_views, table_views
from forms import *
import feed

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^landing/', views.index, name='index'),

    # Forms
    url(r'^communication/$', views.communication, name="communication"),
    url(r'^user-profile/', views.userProfile, name='userprofile'),
    url(r'^comms-audit/(?P<audience_id>\d+)/', views.commsAudit, name='commsaudit'),
    url(r'^audience/', views.audience, name="audience"),
    url(r'^sources/', views.sources, name="source"),
    url(r'^tags/', views.tags, name="tags"),
    url(r'^notes/', views.notes, name="notes"),
    url(r'^audit/', views.save_audit, name="save_audit"),
    url(r'^add-to-newsletter/', views.push_to_newsletter, name="push_to_newsletter"),

    # Tables
    url(r'^view-comms/', table_views.view_communcation, name='view_comms'),
    url(r'^view-audience/', table_views.view_audience, name="view_audience"),
    url(r'^view-source/', table_views.view_sources, name="view_sources"),
    url(r'^view-user-profile/', table_views.view_user_profiles, name="view_user_profile"),
    url(r'^view-comms-audit/', table_views.view_comms_audit, name="view_comms_audit"),
    url(r'^view-notes/', table_views.view_notes, name="view_notes"),
    url(r'^view-tags/', table_views.view_tags, name="view_tags"),
    url(r'^view-newsletter/', table_views.view_newsletter_table, name="view_newsletter_table"),
    url(r'^audit-trail/', table_views.audit_trail, name="view_audit_trail"),

    url(r'^comms-feed/', feed.CommunicationFeed()),
    url(r'^newsletter-email/', views.view_newsletter_email, name="newsletter_email"),
    url(r'^newsletter/', views.view_newsletter, name="newsletter"),
    url(r'^export-approved-csv/', views.export_approved_to_csv, name='export_approved_to_csv'),
    url(r'^export-all-csv/', views.export_all_to_csv, name='export_all_to_csv'),
    url(r'^unapproved-articles', views.unapproved_articles, name='unapproved_articles'),
    url(r'^edit/(?P<article_id>\w+)', views.edit_article, name='edit_article'),
    url(r'^delete/(?P<article_id>\w+)', views.delete_article, name='delete_article'),

    # View a single instance of a communication (viewable by public)
    url(r'^external/(?P<comm_id>\w+)/', views.communication_publish, name="communication_publish"),
    url(r'^approve/(?P<article_id>\w+)', views.article_approval, name="article_approval"),

    # Update table data
    url(r'^user-profile/update', update_views.user_profile_update, name="update_user"),
    url(r'^communication/update/', update_views.communication_update, name="update_comm"),

    url(r'^logout', views.logout, name="logout"),
]
