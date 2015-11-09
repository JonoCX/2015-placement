from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import *

admin.site.register(Communication, SimpleHistoryAdmin)
admin.site.register(Sources, SimpleHistoryAdmin)
admin.site.register(CommsAudit, SimpleHistoryAdmin)
admin.site.register(Audience, SimpleHistoryAdmin)
admin.site.register(UserProfile, SimpleHistoryAdmin)
admin.site.register(Tags, SimpleHistoryAdmin)
admin.site.register(Notes, SimpleHistoryAdmin)