# standard library
from calendar import calendar
from datetime import date
from multiprocessing import context
import calendar

# Django
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
# from django.template.loader import render_to_string
from django.urls import reverse_lazy

# local Django
from accounts.models import Profile
from home.models import Calendar, Schedule
from home.views import has_authenticated_profile, is_volunteer
from .models import (
    UpdateScheduleRequest, Volunteer,
    VolunteerAttendance, VolunteerSchedule,
)

User = get_user_model()


# VIEWS FUNCTIONS

@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
def index(request):
    volunteers = Volunteer.objects.order_by('batch', 'profile__first_name')
    context={
        "volunteers": volunteers
    }
    return render(request, 'volunteers/index.html', context)  


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
def profile(request, pk):
    volunteer = get_object_or_404(Volunteer, id=pk)
    volun_schedule = VolunteerSchedule.objects.filter(volun=volunteer).order_by('day')
    context = {
        'volunteer': volunteer,
        'self_profile': volunteer.profile.user == request.user,
        'volun_schedule' : volun_schedule,
    }
    return render(request, 'volunteers/profile.html', context)


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
@user_passes_test(
    is_volunteer, redirect_field_name=None,
    login_url=reverse_lazy('home:dashboard')
)
@permission_required('volunteers.change_volunteerattendance', raise_exception=True)
def attendance(request):
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
        'today_date': date.today(),
    }

    if not today_cal.class_scheduled:
        context['no_class_today'] = True
        return render(request, 'volunteers/attendance.html', context)

    if not VolunteerAttendance.objects.filter(cal_date__date=date.today()).exists():
        # Create Empty Volunteer Attendance Instances
        today_vol_sch = VolunteerSchedule.objects.filter(
            day=date.today().strftime("%w"))
        for vol_sch in today_vol_sch:
            vol_attendance = VolunteerAttendance(
                volun=vol_sch.volun, cal_date=today_cal)
            # TODO: Use bulk_create command instead.
            vol_attendance.save()

    context['today_vol_att'] = VolunteerAttendance.objects.filter(
        cal_date=today_cal).order_by('volun__roll_no')

    return render(request, 'volunteers/attendance.html', context)


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
@user_passes_test(
    is_volunteer, redirect_field_name=None,
    login_url=reverse_lazy('home:dashboard')
)
@permission_required('volunteers.change_volunteerattendance', raise_exception=True)
def ajax_mark_attendance(request):
    """Mark/unmark volunteer attendance."""
    today_cal = Calendar.objects.get(date=date.today())
    vol_id = request.GET['volun_id']
    is_present = request.GET['is_present']
    vol_att = VolunteerAttendance.objects.get(
        volun__id=vol_id, cal_date=today_cal)
    print(vol_att)
    vol_att.present = True if is_present == 'true' else False
    vol_att.save()
    data = {'success': True}
    return JsonResponse(data)


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
@user_passes_test(
    is_volunteer, redirect_field_name=None,
    login_url=reverse_lazy('home:dashboard')
)
@permission_required('volunteers.change_volunteerattendance', raise_exception=True)
def ajax_add_extra_vol(request):
    """Mark/unmark volunteer attendance."""
    today_cal = Calendar.objects.get(date=date.today())
    roll_no = request.GET['roll_no']

    volun = Volunteer.objects.filter(roll_no__iexact=roll_no).first()
    if not volun:
        data = {'success': False, 'error': 'Volunteer not found.'}
        return JsonResponse(data)

    vol_att = VolunteerAttendance.objects.filter(
        volun=volun, cal_date=today_cal)
    if vol_att.exists():
        data = {'success': False, 'error': 'Volunteer already present in the list.'}
        return JsonResponse(data)

    # Create a new VolunteerAttendance instance
    VolunteerAttendance.objects.create(
        volun=volun, cal_date=today_cal, present=True, extra=True)

    data = {
        'success': True,
        'roll_no': volun.roll_no,
        'name': volun.profile.get_full_name,
        'volun_id': volun.id
    }
    return JsonResponse(data)


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
# @permissions_required
def volunteers_list(request):
    context = {
        'day': Schedule.DAY,
    }
    return render(request, 'volunteers/volunteers_list.html', context)


@login_required
@user_passes_test(
    has_authenticated_profile, redirect_field_name=None,
    login_url=reverse_lazy('accounts:complete_profile')
)
# @permissions_required
def ajax_volunteers_list(request):
    data = {}
    vol_list_day = request.GET.get('vol_list_day', None)
    if not vol_list_day:
        return JsonResponse(data)

    vol_to_show = VolunteerSchedule.objects.filter(day=vol_list_day)

    for vol_sch in vol_to_show:
        section_id = vol_sch.schedule.section.section_id
        section_name = vol_sch.schedule.section.name

        volun_id = vol_sch.volun_id
        volun_roll_no = vol_sch.volun.roll_no
        volun_name = vol_sch.volun.profile.get_full_name

        # Use 'section_id' as key to display volunteers sorted by 'section_id'
        # and 'roll_no' to make every key unique.
        key = str(section_id) + str(volun_roll_no)
        data[key] = [volun_id, volun_roll_no, volun_name, section_name]

    return JsonResponse(data)


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
@user_passes_test(
    is_volunteer, redirect_field_name=None,
    login_url=reverse_lazy('home:dashboard')
)
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    volun = Volunteer.objects.get(profile=profile)

    context = {
        'profile': profile,
        'volun': volun,
    }

    if request.method == 'POST':
        roll_no = request.POST['roll_no']
        if volun.roll_no != roll_no:
            duplicate_roll_check = Volunteer.objects.filter(roll_no=roll_no)
            if duplicate_roll_check.exists():
                context['update_error'] = "A volunteer with entered roll no. already exists."
                messages.error(request, 'Profile update failed!')
                return render(request, 'volunteers/update_profile.html', context)
            else:
                volun.roll_no = roll_no

        profile.first_name = request.POST['first_name']
        profile.last_name = request.POST['last_name']
        profile.gender = request.POST['gender']
        profile.alt_email = request.POST['alt_email']
        profile.street_address1 = request.POST['street_address1']
        profile.street_address2 = request.POST['street_address2']
        profile.pincode = request.POST['pincode']
        profile.city = request.POST['city']
        profile.state = request.POST['state']
        profile.contact_no = request.POST['contact_no']
        if 'profile_image' in request.FILES:
            # Delete the previous profile image.
            profile.profile_image.delete(False)
            profile.profile_image = request.FILES.get('profile_image')
        profile.save()

        volun.batch = request.POST['batch']
        volun.programme = request.POST['programme']
        volun.dob = request.POST['dob']
        volun.save()

        messages.success(request, 'Profile updated Successfully!')
        return redirect('volunteers:update_profile')

    return render(request, 'volunteers/update_profile.html', context)


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
@user_passes_test(
    is_volunteer, redirect_field_name=None,
    login_url=reverse_lazy('home:dashboard')
)
def update_schedule(request):
    volun = Volunteer.objects.get(profile__user=request.user)
    last_pending_req = UpdateScheduleRequest.objects.filter(
        volun=volun, approved=False, declined=False, by_admin=False, cancelled=False)

    if request.method == 'POST':
        if request.POST.get('submit') == 'update-schedule':
            new_day = request.POST['day']
            new_section_id = request.POST['section']

            schedule = Schedule.objects.get(
                day=new_day, section__section_id=new_section_id)
            # Cancel last pending request.
            if last_pending_req.exists():
                last_pending_req = last_pending_req[0]
                last_pending_req.cancelled = True
                last_pending_req.save()
            # Create new request
            update_req = UpdateScheduleRequest(
                volun=volun, new_schedule=schedule)
            prev_vol_sch = VolunteerSchedule.objects.filter(volun=volun)
            if prev_vol_sch.exists():
                update_req.previous_schedule = prev_vol_sch[0].schedule
            update_req.save()

            messages.success(
                request, 'Schedule update requested successfully!')
            return redirect('volunteers:update_schedule')

        elif request.POST.get('submit') == 'cancel-last-req':
            if last_pending_req.exists():
                last_pending_req = last_pending_req[0]
                last_pending_req.cancelled = True
                last_pending_req.save()
                messages.success(
                    request, 'Last request cancelled successfully!')
            else:
                messages.error(request, 'No pending requests.')
            return redirect('volunteers:update_schedule')

    context = {
        'day': Schedule.DAY,
        'update_req': UpdateScheduleRequest.objects.filter(volun=volun).order_by('-date'),
        'last_pending_req': last_pending_req.exists(),
    }
    return render(request, 'volunteers/update_schedule.html', context)


@login_required
@user_passes_test(
    has_authenticated_profile, redirect_field_name=None,
    login_url=reverse_lazy('accounts:complete_profile')
)
@user_passes_test(
    is_volunteer, redirect_field_name=None,
    login_url=reverse_lazy('home:dashboard')
)
def ajax_update_schedule(request):
    sch_day = request.GET.get('sch_day', None)
    data = {}
    schedule = Schedule.objects.filter(
        day=sch_day).order_by('section__section_id')

    for sch in schedule:
        data[sch.section.section_id] = sch.section.name

    return JsonResponse(data)

@login_required
@user_passes_test(
    has_authenticated_profile, redirect_field_name=None,
    login_url=reverse_lazy('accounts:complete_profile')
)
@user_passes_test(
    is_volunteer, redirect_field_name=None,
    login_url=reverse_lazy('home:dashboard')
)
def leaderboard(request):
    cur_month = date.today().month
    cur_year = date.today().year
    
    volunteers = VolunteerAttendance.objects.filter(cal_date__date__month=cur_month, cal_date__date__year=cur_year, present = 1) | VolunteerAttendance.objects.filter(cal_date__date__month=cur_month, cal_date__date__year=cur_year, extra = 1)
    volunteers = volunteers.values('volun_id', 'volun__roll_no', 'volun__profile__first_name', 'volun__profile__last_name').annotate(total_attendance=Count('cal_date')).order_by('-total_attendance')

    return render(request, 'volunteers/leaderboard.html', { 'volunteers': volunteers, 'cur_month': calendar.month_abbr[cur_month], 'cur_year': cur_year })