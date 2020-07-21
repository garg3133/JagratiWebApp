# standard library
# import json
from datetime import datetime, date

# third-party
# from openpyxl import load_workbook

# Django
# from django.conf import settings
from django.contrib import messages
# from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.sites.shortcuts import get_current_site
# from django.core import serializers
# from django.core.mail import send_mail
# from django.core.serializers.json import DjangoJSONEncoder
# from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# from django.template.defaulttags import register
# from django.template.loader import render_to_string
# from django.urls import reverse
# from django.utils.encoding import force_bytes
# from django.utils.html import strip_tags
# from django.utils.http import urlsafe_base64_encode

# local Django
# from accounts.tokens import account_activation_token
from accounts.models import Profile
from home.models import(
    Calendar, ClassworkHomework, Schedule, Section,
    Student, StudentAttendence, StudentSchedule,
)
from .models import (
    Designation, UpdateScheduleRequest, Volunteer,
    VolunteerAttendence, VolunteerSchedule,
)


# NON-VIEWS FUNCTIONS
def user_has_profile(user):
    return Profile.objects.filter(user=user).exists()


# VIEWS FUNCTIONS

@login_required
@user_passes_test(user_has_profile, redirect_field_name=None, login_url='/dashboard/')
def index(request):
    return HttpResponse('Hello there!')

@login_required
@user_passes_test(user_has_profile, redirect_field_name=None, login_url='/dashboard/')
def profile(request):
    return HttpResponse('Hello there!')

@login_required
@user_passes_test(user_has_profile, redirect_field_name=None, login_url='/dashboard/')
# @permissions_required
def attendence(request):
    today_cal = Calendar.objects.filter(date=date.today())
    # TO BE REMOVED...
    # Update today's date in Calendar if not already there
    if today_cal.exists():
        today_cal = today_cal[0]
    else:
        today_cal_new = Calendar(date=date.today())
        today_cal_new.save()
        today_cal = Calendar.objects.get(date=date.today())
    # ...TILL HERE

    context = {
        'today_date' : date.today(),
    }

    if today_cal.class_scheduled:
        if not VolunteerAttendence.objects.filter(cal_date__date=date.today()).exists():
            # Create Empty Volunteer Attendence Instances
            today_vol_sch = VolunteerSchedule.objects.filter(day=date.today().strftime("%A"))
            for vol_sch in today_vol_sch:
                vol_attendance = VolunteerAttendence(volun=vol_sch.volun, cal_date=today_cal)
                vol_attendance.save()
    else:
        context['no_class_today'] = True
        return render(request, 'volunteers/attendence.html', context)

    if request.method == 'POST':
        vol_array = request.POST.getlist('volunteered')
        extra_vol_array = request.POST.getlist('extra-vol')

        # Mark everyone's absent
        vol_att_today = VolunteerAttendence.objects.filter(cal_date=today_cal)
        for vol_att in vol_att_today:
            vol_att.present = False
            vol_att.save()

        for vol_id in vol_array:
            volun = Volunteer.objects.get(id=vol_id)
            vol_att = VolunteerAttendence.objects.get(volun=volun, cal_date=today_cal)
            vol_att.present = True
            vol_att.save()

        for extra_vol_roll in extra_vol_array:
            volun = Volunteer.objects.filter(roll_no=extra_vol_roll)
            if volun.exists():
                extra_vol_att = VolunteerAttendence.objects.filter(volun=volun[0], cal_date=today_cal)
                if extra_vol_att.exists():
                    extra_vol_att = extra_vol_att[0]
                    extra_vol_att.present = True
                else:
                    extra_vol_att = VolunteerAttendence(volun=volun[0], cal_date=today_cal, present=True, extra=True)
                extra_vol_att.save()

        messages.success(request, 'Attendence marked successfully!')
        return redirect('volunteers:attendence')

    context['today_vol_att'] = VolunteerAttendence.objects.filter(cal_date=today_cal).order_by('volun__roll_no')
    return render(request, 'volunteers/attendence.html', context)

@login_required
@user_passes_test(user_has_profile, redirect_field_name=None, login_url='/dashboard/')
# @permissions_required
def volunteers_list(request):
    context = {
        'day': Schedule.DAY,
    }
    return render(request, 'volunteers/volunteers_list.html', context)

@login_required
@user_passes_test(user_has_profile, redirect_field_name=None, login_url='/dashboard/')
# @permissions_required
def ajax_volunteers_list(request):
    data = {}
    vol_list_day = request.GET.get('vol_list_day', None)
    if not vol_list_day:
        return JsonResponse(data)

    vol_to_show = VolunteerSchedule.objects.filter(day=vol_list_day)
    # setion_id used as key to display volunteers sorted by section_id and roll_no to make every key unique
    for vol_sch in vol_to_show:
        key = str(vol_sch.schedule.section.section_id) + str(vol_sch.volun.roll_no)
        data[key] = [vol_sch.volun.roll_no, vol_sch.volun.profile.get_full_name, vol_sch.schedule.section.name]

    return JsonResponse(data)

@login_required
@user_passes_test(user_has_profile, redirect_field_name=None, login_url='/dashboard/')
def update_profile(request):
    volun = Volunteer.objects.filter(email=request.user)
    if volun.exists():
        volun = volun[0]
    else:
        return redirect('set_profile')

    context = {
        #dash-update
        'last_5_year': datetime.now().year - 5,
    }
    
    if request.method == 'POST':
        roll_no         = request.POST['roll_no']
        first_name      = request.POST['first_name']
        last_name       = request.POST['last_name']
        gender          = request.POST['gender']
        alt_email       = request.POST['alt_email']
        batch           = request.POST['batch']
        programme       = request.POST['programme']
        street_address1 = request.POST['street_address1']
        street_address2 = request.POST['street_address2']
        pincode         = request.POST['pincode']
        city            = request.POST['city']
        state           = request.POST['state']
        dob             = request.POST['dob']
        contact_no      = request.POST['contact_no']
        profile_image	= request.FILES.get('profile_image')

        if roll_no:
            if volun.roll_no != roll_no:
                duplicate_roll_check = Volunteer.objects.filter(roll_no=roll_no)
                if duplicate_roll_check.exists():
                    context1 = {
                        'update_error': "A volunteer with entered roll no. already exists."
                    }
                    context.update(context1)
                    messages.error(request, 'Profile update failed!')
                    return render(request, 'home/update_profile.html', context)
                else:
                    volun.roll_no = roll_no
        if first_name:
            volun.first_name = first_name
        if last_name:
            volun.last_name = last_name
        volun.gender = gender
        volun.batch = batch
        volun.programme = programme
        volun.dob = dob
        if contact_no:
            volun.contact_no = contact_no
        if alt_email:
            volun.alt_email = alt_email
        if street_address1:
            volun.street_address1 = street_address1
        if street_address2:
            volun.street_address2 = street_address2
        if city:
            volun.city = city
        if state:
            volun.state = state
        if pincode:
            volun.pincode = pincode
        if 'profile_image' in request.FILES:
            # delete the previous one 
            volun.profile_image.delete(False)
            volun.profile_image = profile_image

        volun.save()

        messages.success(request, 'Profile updated Successfully!')
        return HttpResponseRedirect(reverse('update_profile'))

    return render(request, 'home/update_profile.html', context)
