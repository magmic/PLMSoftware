import json
import os
import smtplib
from .models import *
from datetime import datetime, timedelta, date
from django.contrib.auth import authenticate
from django.contrib.auth import login as my_log
from django.contrib.auth import logout as my_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import request
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import RequestContext, loader


def index(request):
	template = loader.get_template('index.html')
	return
	patient = None
	doc = None

	if request.user.is_authenticated():
		try:
			patient = request.user.patient
		except:
			try:
				doc = request.user.doctor
			except:
				context = RequestContext(request, {})
				return HttpResponse(template.render(context))
	else:
		if request.GET.get('next'):
			context = RequestContext(request, {
				'next': request.GET.get('next')
				})
			return HttpResponse(template.render(context))
		context = RequestContext(request, {})
		return HttpResponse(template.render(context))

	if doc:
		doc_pats = DoctorPatient.objects.filter(doctor=doc)
		context = RequestContext(request, {
			'doctor': doc,
			'doc_pats': doc_pats,
		})
	else:
		doc_pats = DoctorPatient.objects.filter(patient=patient)
		context = RequestContext(request, {
			'patient': patient,
			'doc_pats': doc_pats,
		})
	return HttpResponse(template.render(context))

@login_required
def patient_search(request):
	try:
		doc = request.user.doctor
	except:
		return HttpResponse(status=401)
	template = loader.get_template('polls/patient_search.html')

	search_by = request.GET.get("search_by")
	if search_by == "name":
		name = request.GET.get('search_val')

		patients = [i for i in Patient.objects.filter(visibility=1)] # Conversion to list for addition
		patients += [i.patient for i in DoctorPatient.objects.filter(doctor=doc)]
		filtered_patients = {}

		# Basic search for partial name. Need to add case unsensitivity
		for patient in patients:
			if name in patient.name:
				filtered_patients[patient] = patient.birth_date or datetime.now()

		context = RequestContext(request, {
			'patients': filtered_patients,
			})
		return HttpResponse(template.render(context))

	if search_by == "sec":
		sec = request.GET.get('search_val')
		try:
			sec = str(sec)
		except:
			context = RequestContext(request, {
				'patients': [],
				})
			return HttpResponse(template.render(context))

		patients = [i for i in Patient.objects.filter(visibility=1)] # Conversion to list for addition
		patients += [i.patient for i in DoctorPatient.objects.filter(doctor=doc)]
		filtered_patients = []

		# Basic search for partial social security number
		for patient in patients:
			if sec in str(patient.social_sec):
				filtered_patients.append(patient)

		context = RequestContext(request, {
			'patients': filtered_patients,
			})
		return HttpResponse(template.render(context))

	else:
		context = RequestContext(request, {
			'patients': [],
			})
		return HttpResponse(template.render(context))

@login_required
def doctor_search(request):
	try:
		pat = request.user.patient
	except:
		return HttpResponse(status=401)
	template = loader.get_template('polls/doctor_search.html')

	search_by = request.GET.get("search_by")
	if search_by == "country":
		country = request.GET.get('search_val')
		doctors = Doctor.objects.filter(country=country)
	elif search_by == "city":
		city = request.GET.get('search_val')
		doctors = Doctor.objects.filter(city=city)
	else:
		zip_code = request.GET.get('search_val')
		doctors = Doctor.objects.filter(zip_code=zip_code)

	doc_assoc = {}
	for doctor in doctors:
		if DoctorPatient.objects.filter(doctor=doctor,patient=pat):
			doc_assoc[doctor] = 1
		elif PendingAssoc.objects.filter(doctor=doctor,patient=pat):
			doc_assoc[doctor] = 2
		else:
			doc_assoc[doctor] = 0
	# doc_assoc = {doctor: 1 if DoctorPatient.objects.filter(doctor=doctor,patient=pat) else 2 if PendingAssoc.objects.filter(doctor=doctor,patient=pat) else 0 for doctor in doctors}
	context = RequestContext(request, {
		'doctors': doc_assoc,
		'patient': pat,
		})
	return HttpResponse(template.render(context))

@login_required
def add_doctor(request):
	try:
		pat = request.user.patient
	except:
		return HttpResponse(status=401)

	doc = Doctor.objects.filter(id=int(request.POST.get('doc')))
	if not doc:
		return HttpResponse(status=500)
	if DoctorPatient.objects.filter(doctor=doc[0],patient=pat) or PendingAssoc.objects.filter(doctor=doc[0],patient=pat):
		return HttpResponse(status=500)


	new_assoc = PendingAssoc.objects.get_or_create(doctor=doc[0],patient=pat,assoc_date=datetime.now())
	new_assoc[0].save()

	return HttpResponse(json.dumps({"success": "True"}))

@login_required
def remove_pending(request):
	try:
		pat = request.user.patient
	except:
		return HttpResponse(status=401)

	doc = Doctor.objects.filter(id=int(request.POST.get('doc')))
	if not doc:
		return HttpResponse(status=500)
	if DoctorPatient.objects.filter(doctor=doc[0],patient=pat) or not PendingAssoc.objects.filter(doctor=doc[0],patient=pat):
		return HttpResponse(status=500)


	PendingAssoc.objects.filter(doctor=doc[0],patient=pat)[0].delete()

	return HttpResponse(json.dumps({"success": "True"}))

@login_required
def remove_doctor(request):
	try:
		pat = request.user.patient
	except:
		return HttpResponse(status=401)

	doc = Doctor.objects.filter(id=int(request.POST.get('doc')))
	if not doc:
		return HttpResponse(status=500)
	if not DoctorPatient.objects.filter(doctor=doc[0],patient=pat) or PendingAssoc.objects.filter(doctor=doc[0],patient=pat):
		return HttpResponse(status=500)


	DoctorPatient.objects.filter(doctor=doc[0],patient=pat)[0].delete()

	return HttpResponse(json.dumps({"success": "True"}))

def register_patient(request):
	if request.user.is_authenticated():
		return redirect("../../")
	else:
		template = loader.get_template('polls/register_patient.html')
		context = RequestContext(request, {})
		return HttpResponse(template.render(context))


def register_doctor(request):
	if request.user.is_authenticated():
		return redirect("../../")
	else:
		template = loader.get_template('polls/register_doctor.html')
		context = RequestContext(request, {})
		return HttpResponse(template.render(context))


def account_confirm(request):
	if request.user.is_authenticated():
		return redirect("../../")
	
	template = loader.get_template('polls/account_confirm.html')
	
	if request.POST.get('pass') != request.POST.get('c_pass'):
		context = RequestContext(request, {
			'error': 'Password and confirmation don\'t match.'
			})
		return HttpResponse(template.render(context))

	if User.objects.filter(email=request.POST.get('email')):
		context = RequestContext(request, {
			'error': 'This email is already taken.'
			})
		return HttpResponse(template.render(context))

	if request.POST.get('type') == 'patient':

		fields = ['user', 'pass', 'c_pass', 'email', 'firstname', 'name', 'day', 'month', 'year', 'sec']

		for field in fields:
			if not request.POST.get(field) or request.POST.get(field) == '':
				context = RequestContext(request, {
					'error': 'Please complete all the fields.'
					})
				return HttpResponse(template.render(context))

		if Patient.objects.filter(social_sec=request.POST.get('sec')):
			context = RequestContext(request, {
				'error': 'This social security number is already taken.'
				})
			return HttpResponse(template.render(context))

		try:
			new_user = User.objects.create_user(
				username=request.POST.get('user'),
				email=request.POST.get('email'),
				password=request.POST.get('pass'),
				first_name=request.POST.get('firstname'),
				last_name=request.POST.get('name')
			)
			new_user.save()

			new_pat = Patient.objects.create(
				user=new_user,
				firstname=request.POST.get('firstname'),
				name=request.POST.get('name'),
				social_sec=request.POST.get('sec'),
				birth_date=date(int(request.POST.get('year')), int(request.POST.get('month')), int(request.POST.get('day'))),
				sex=int(request.POST.get('sex')),
				visibility=1 if request.POST.get('visibility') else 0
			)
			new_pat.save()
		except:
			context = RequestContext(request, {
				'error': 'Uh oh. Something went wrong when creating your account.'
				})
			return HttpResponse(template.render(context))

	elif request.POST.get('type') == 'doctor':

		fields = ['user', 'pass', 'c_pass', 'email', 'firstname', 'name', 'country', 'city', 'zip']

		for field in fields:
			if not request.POST.get(field) or request.POST.get(field) == '':
				context = RequestContext(request, {
					'error': 'Please complete all the fields.'
					})
				return HttpResponse(template.render(context))

		try:
			# gmail_user = "problembasedworkshop@gmail.com"
			# gmail_pwd = "ruminationdevappspot"
			# FROM = 'problembasedworkshop@gmail.com'
			# TO = ['matthieu.crampon@gmail.com'] #must be a list
			# SUBJECT = "ACCOUNT REQUEST"
			# TEXT = """
			new_user = User.objects.create_user(
				username=request.POST.get('user'),
				email=request.POST.get('email'),
				password=request.POST.get('pass'),
				first_name=request.POST.get('firstname'),
				last_name=request.POST.get('name')
			)
			new_user.save()

			new_doc = Doctor.objects.create(
				user=new_user,
				country=request.POST.get('country'),
				city=request.POST.get('city'),
				zip_code=request.POST.get('zip'),
			)
			new_doc.save()
			# """

			# # Prepare actual message
			# message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
			# """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

			# server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
			# server.ehlo()
			# server.starttls()
			# server.login(gmail_user, gmail_pwd)
			# server.sendmail(FROM, TO, message)
			# server.close()			
		except:
			context = RequestContext(request, {
				'error': 'Uh oh. Something went wrong when creating your account.'
				})
			return HttpResponse(template.render(context))

	else:
		context = RequestContext(request, {
			'error': 'Uh oh. Something went wrong when creating your account.'
			})
		return HttpResponse(template.render(context))
	context = RequestContext(request, {
		'success': True
		})
	return HttpResponse(template.render(context))