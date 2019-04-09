from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404

from users.models import Subscriber
from users.forms import RegistrationForm, LoginForm, UserUpdateForm, GeneralDescUpdate
from django.views import View
from django.contrib.auth import authenticate, login, get_user_model

from django.contrib import messages

from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from bootstrap_modal_forms.generic import (BSModalUpdateView, BSModalDeleteView)
from django.urls import reverse_lazy


##########################################################################################################
######################           LOGIN / REGISTRATION                #####################################
##########################################################################################################


######################################################################################
#   SIGN UP WITH EMAIL CONFIRMATION
######################################################################################

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import RegistrationForm
from .tokens import account_activation_token

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            password = form.cleaned_data['password']
            user.set_password(password)
            password_check = form.cleaned_data['password_check']
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('users/actions/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your blog account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render(request, 'users/actions/confirm_email.html', {})
    else:
        form = RegistrationForm()
    return render(request, 'users/registration.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        Subscriber.objects.create(user=user)
        return render(request, 'users/actions/confirm_email_valid.html', {})
    else:
        return render(request, 'users/actions/confirm_email_invalid.html', {})



# User = get_user_model()
#
#
# class RegistrationView(View):
# 	template_name = 'users/registration.html'
# 	form = RegistrationForm
# 	message_send = 'You have registered account.'
#
# 	def get(self, request, *args, **kwargs):
# 		form = self.form
# 		context = {'form': form}
# 		return render(self.request, self.template_name, context)
#
# 	def post(self, request, *args, **kwargs):
# 		form = self.form(request.POST or None)
# 		if form.is_valid():
# 			new_user = form.save(commit=False)
# 			username = form.cleaned_data['username']
# 			password = form.cleaned_data['password']
# 			new_user.set_password(password)
# 			password_check = form.cleaned_data['password_check']
# 			new_user.save()
# 			Subscriber.objects.create(user=User.objects.get(username=new_user.username))
#
# 			messages.success(self.request, self.message_send)
#
# 			return HttpResponseRedirect('../login')
# 		context = {'form': form}
# 		return render(self.request, self.template_name, context)



class LoginView(View):
	template_name = 'users/login.html'
	form = LoginForm
	message_send = 'You are logged in.'

	def get(self, request, *args, **kwargs):
		form = self.form
		context = {'form': form}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form(request.POST or None)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			log_user = User.objects.get(email = email)

			user = authenticate(username = log_user.username, password = password)
			if user:
				login(self.request, user)
				messages.success(self.request, self.message_send)
			return HttpResponseRedirect('/')
		context = {'form': form}
		return render(self.request, self.template_name, context)



##########################################################################################################
######################        PROFILE - Detail/Create/Update/Delete         ##############################
##########################################################################################################


class Profile( DetailView):

	model = get_user_model()
	template_name = 'users/profile.html'

	def get_context_data(self, *args, **kwargs):
		context = super(Profile, self).get_context_data(*args, **kwargs)
		context['subscriber'] = Subscriber.objects.get(user__id=self.kwargs.get('pk'))

		# для правильного отображения в шапке имени юзера и правильного перехода по мудакам
		context['user'] = self.request.user
		return context






class ProfileDeleteView(BSModalDeleteView):
    model = User
    template_name = 'users/actions/profile-delete.html'
    success_message = 'Success: Profile was deleted.'
    success_url = reverse_lazy('posts:base-view')



######################################################################################
######################################################################################

class GeneralUpdateView(BSModalUpdateView):
    model = Subscriber
    template_name = 'users/actions/profile-update2.html'
    form_class = GeneralDescUpdate
    success_message = 'Success: Subscriber was updated.'

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')




class PersonalUpdateView(BSModalUpdateView):
    model = User
    template_name = 'users/actions/profile-update2.html'
    form_class = UserUpdateForm
    success_message = 'Success: Personal Info was updated.'

    def get_success_url(self, **kwargs):
        return self.request.META.get('HTTP_REFERER')
