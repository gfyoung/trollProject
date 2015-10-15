from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Download


class TrollAdminSite(AdminSite):
    site_header = "Trolloler Administration"
    site_title = "Trolloler Admin"
    index_title = "Trolling Behind the Scenes"
    index_template = "trollSiteAdmin/index.html"
    login_template = "trollSiteAdmin/login.html"
    logout_template = "trollSiteAdmin/logout.html"
    password_change_template = "trollSiteAdmin/passwordChangeForm.html"
    password_change_done_template = "trollSiteAdmin/passwordChangeDone.html"


class DownloadAdmin(admin.ModelAdmin):
    change_form_template = "trollSiteAdmin/changeForm.html"
    change_list_template = "trollSiteAdmin/changeList.html"
    delete_confirmation_template = "trollSiteAdmin/deleteConfirmation.html"
    delete_selected_confirmation_template =\
        "trollSiteAdmin/deleteSelectedConfirmation.html"
    object_history_template = "trollSiteAdmin/objectHistory.html"
    list_display = ("target_os", "filename", "description")
    list_filter = ("target_os", "filename", "description")

adminSite = TrollAdminSite(name="admin")
adminSite.register(Download, DownloadAdmin)
