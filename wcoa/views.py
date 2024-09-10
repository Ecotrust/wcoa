from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.defaults import page_not_found as dj_page_not_found
from portal.base.views import search as portal_seach
from visualize.views import show_planner
from django.views.decorators.clickjacking import xframe_options_exempt
from accounts import views as accounts_views

try:
    from django.urls import reverse, reverse_lazy
except (ModuleNotFoundError, ImportError) as e:
    from django.core.urlresolvers import reverse, reverse_lazy

def index(request):
    return HttpResponse("Hello, world. You're at the wcoa index.")

def show_wcoa_planner(request, template='wcoa/visualize/planner.html'):
    return show_planner(request, template)

@xframe_options_exempt
def show_wcoa_embedded_map(request, template='wcoa/visualize/embedded.html'):
    return show_planner(request, template)

def page_not_found(request, exception=None, template='wcoa_404.html'):
    return dj_page_not_found(request, exception, template)

def search(request, template='wcoa_search_results.html'):
    return portal_seach(request, template)

##########################################################
######             accounts             ##################
##########################################################

def show_wcoa_account_index(request, template='wcoa/accounts/index.html', login_template='wcoa/accounts/login.html'):
    return accounts_views.index(request, template=template, login_template=login_template)

class edit_account(accounts_views.UserDetailView):
    template_name = 'wcoa/accounts/user_detail_form.html'
    success_url = reverse_lazy('show_wcoa_account_indexs')

class ChangePasswordView(accounts_views.ChangePasswordView):
    template_name = 'wcoa/accounts/change_password_form.html'
    success_url = reverse_lazy('show_wcoa_account_indexs')

def forgot(request, template='wcoa/accounts/forgot/forgot.html', wait_template='wcoa/accounts/forgot/wait_for_email.html'):
    return accounts_views.forgot(request, template=template, wait_template=wait_template)

def forgot_reset(request, code, reset_template='wcoa/accounts/forgot/reset.html', success_template='wcoa/accounts/forgot/reset_successful.html'):
    return accounts_views.forgot_reset(request, code, reset_template=reset_template, success_template=success_template)

def register(request, template='wcoa/accounts/register.html', success_template='wcoa/accounts/success.html', error_template='wcoa/accounts/registration_error.html'):
    return accounts_views.register(request, template, success_template, error_template)

##########################################################
######             groups               ##################
##########################################################

def show_wcoa_mapgroups(request, template='wcoa/mapgroups/mapgroup_list.html'):
    from mapgroups.views import MapGroupListView
    return MapGroupListView.as_view(template_name=template)(request)

def create_wcoa_mapgroup(request, template='wcoa/mapgroups/mapgroup_form.html'):
    from mapgroups.views import MapGroupCreate
    return MapGroupCreate.as_view(template_name=template)(request)

def show_wcoa_edit_mapgroups(request, *args, **kwargs):
    template='wcoa/mapgroups/mapgroup_edit.html'
    from mapgroups.views import MapGroupEditView
    return MapGroupEditView.as_view(template_name=template)(request, *args, **kwargs)

def show_wcoa_detail_mapgroups(request, *args, **kwargs):
    template='wcoa/mapgroups/mapgroup_detail.html'
    from mapgroups.views import MapGroupDetailView
    return MapGroupDetailView.as_view(template_name=template)(request, *args, **kwargs)


# import ipdb; ipdb.set_trace()
from wagtail.admin.views.chooser import BaseLinkFormView, shared_context
from .forms import NewTabLinkChooserForm
from wagtail.admin.modal_workflow import render_modal_workflow

class NewTabLinkView(BaseLinkFormView):
    form_prefix = "newtab-link-chooser"
    form_class = NewTabLinkChooserForm
    template_name = "wagtailadmin/chooser/newtab_link.html"
    step_name = "newtab_link"
    link_url_field_name = "url"

    # def render_form_response(self):
    #     return render_modal_workflow(
    #         self.request,
    #         self.template_name,
    #         None,
    #         shared_context(
    #             self.request,
    #             {
    #                 "form": self.form,
    #                 "allow_newtab_link": request.GET.get("allow_newtab_link"),
    #             },
    #         ),
    #         json_data={"step": self.step_name},
    #     )

    # def render_chosen_response(self, result):
    #     return render_modal_workflow(
    #         self.request,
    #         None,
    #         None,
    #         None,
    #         json_data={"step": "newtab_link_chosen", "result": result},
    #     )
        

# class ExternalPlusLinkView(ExternalLinkView):
    # import ipdb; ipdb.set_trace()
    # form_prefix = "ext-link-chooser"
    # form_class = ExternalPlusLinkChooserForm
    # template_name = "wagtailadmin/chooser/newtab_link.html"
    # step_name = "external_link"
    # link_url_field_name = "url"

    # def render_chosen_response(self, result):
    #     return render_modal_workflow(
    #         self.request,
    #         None,
    #         None,
    #         None,
    #         json_data={"step": "newtab_link_chosen", "result": result},
    #     )