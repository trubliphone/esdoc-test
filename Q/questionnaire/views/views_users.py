from allauth.account.views import SignupView, LoginView, PasswordResetView, LogoutView
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render

from Q.questionnaire.forms.forms_users import QUserProfileForm
from Q.questionnaire.views.views_base import add_parameters_to_context
from Q.questionnaire.views.views_errors import q_error


class QLoginView(LoginView):
    redirect_field_name = "next"
    template_name = 'account/login.html'


class QLogoutView(LogoutView):
    redirect_field_name = "next"
    template_name = "account/logout.html"


class QSignupView(SignupView):
    redirect_field_name = "next"
    template_name = "account/signup.html"


def q_profile(request, username=None):
    context = add_parameters_to_context(request)
    next_page = context.get("next")

    current_user = request.user

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        if not username:
            msg = "Please specify a user."
        else:
            msg = "Unable to locate user '{0}'".format(username)
        return q_error(request, error_msg=msg)

    read_only = False
    if current_user.username != username:
        if not current_user.is_superuser:
            read_only = True
        # msg = "You do not have permission to edit this user."
        # return q_error(request, error_msg=msg)
    if user.is_superuser:
        msg = "You can't view the details of the site administrator.  What were you thinking?!?."
        return q_error(request, error_msg=msg)
    if not user.is_active:
        msg = "This user's account has been disabled."
        return q_error(request, error_msg=msg)

    user_form = QUserProfileForm(instance=user.profile)

    # if request.method == "GET":
    #
    #     user_form = QUserProfileForm(instance=user.profile)
    #
    # else:  # request.method == "POST":
    #
    #     import ipdb; ipdb.set_trace()
    #     data = request.POST
    #     user_form = QUserProfileForm(instance=user_profile, data=data)
    #     if user_form.is_valid():
    #
    #         msg = "Successfully changed user details."
    #         messages.add_message(request, messages.SUCCESS, msg)
    #
    #         user_profile = user_form.save()
    #         if user_profile is not None:
    #             if next_page:
    #                 return redirect(next_page)
    #
    #     else:
    #         msg = "Error changing user details."
    #         messages.add_message(request, messages.WARNING, msg)

    context = {
        "read_only": read_only,
        "user": user,
        "form": user_form,
    }
    return render(request, 'questionnaire/q_profile.html', context)
