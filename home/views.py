# standard library
from datetime import datetime, date

# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

# local Django
from accounts.models import Profile
from apps.students.models import Student, StudentAttendance, StudentSchedule
from apps.volunteers.models import Volunteer, VolunteerAttendance, VolunteerSchedule
from .models import Calendar, ClassworkHomework, Schedule, Section


# NON-VIEWS FUNCTIONS

def has_authenticated_profile(user):
    """User has a profiles and is authenticated by admin.
       Necessary to access any page on site bar home page."""
    return user.auth is True and Profile.objects.filter(user=user).exists()

def is_volunteer(user):
    """To be used in views accessible to volunteers only."""
    return user.desig == 'v'


# VIEW FUNCTIONS

def index(request):
    if request.user.is_authenticated:
        return redirect('home:dashboard')
    return render(request, 'home/index.html')


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
def dashboard(request):
    # TO BE REMOVED...
    # Update today's date in Calendar if not already there
    today_cal = Calendar.objects.filter(date=date.today())
    if today_cal.exists():
        today_cal = today_cal[0]
    else:
        today_cal_new = Calendar(date=date.today())
        today_cal_new.save()
        today_cal = Calendar.objects.get(date=date.today())
    # ...TILL HERE

    # Dashboard Query
    # HTTP Request is always GET
    query_date_str = request.GET.get('d', '')
    query_section = request.GET.get('s', '')

    if query_date_str and query_section:
        query_date = datetime.strptime(query_date_str, '%Y-%m-%d').date()
        query_day = query_date.strftime("%w")
        calendar = Calendar.objects.filter(date=query_date)

        # If the section is not taught on selected day
        # (URL parameters are altered manually)
        schedule = Schedule.objects.filter(day=query_day, section__section_id=query_section)
        if not schedule.exists():
            return redirect('home:dashboard')

        context = {
            'selected_date' : query_date,
            'selected_section' : query_section,
        }
        # If calendar instance for that day is not created
        if not calendar.exists():
            context['calendar_not_updated'] = True
            return render(request, 'home/dashboard.html', context)

        calendar = calendar[0]
        # If No Class is Scheduled on that day
        if not calendar.class_scheduled:
            context['no_class_scheduled'] = True
            context['calendar_remark'] = calendar.remark
            return render(request, 'home/dashboard.html', context)

        # Classwork/Homework info
        cw_hw = ClassworkHomework.objects.filter(cal_date=calendar, section__section_id=query_section).first()
        context['cw_hw'] = cw_hw

        # Students Attendance
        student_attendance = StudentAttendance.objects.filter(cal_date=calendar, present=True).order_by('student__school_class')
        context['student_attendance'] = student_attendance

        if student_attendance.exists():
            stu_att_village = {}
            stu_att_village['G'] = stu_att_village['M'] = stu_att_village['C'] = 0
            stu_att_village['A'] = stu_att_village['S'] = 0

            for stu_att in student_attendance:
                stu_att_village[stu_att.student.village] += 1
            # Mehgawan Side
            stu_att_village['MS'] = stu_att_village['M'] + stu_att_village['C'] + stu_att_village['A'] + stu_att_village['S']

            context['stu_att_village'] = stu_att_village

        # Volunteers Attendance
        volun_attendance = VolunteerAttendance.objects.filter(cal_date=calendar, present=True).order_by('volun__roll_no')
        context['volun_attendance'] = volun_attendance

        return render(request, 'home/dashboard.html', context)

    elif query_date_str or query_section:
        # If only one parameter is provided
        return redirect('home:dashboard')

    return render(request, 'home/dashboard.html')


@login_required
@user_passes_test(
    has_authenticated_profile, redirect_field_name=None,
    login_url=reverse_lazy('accounts:complete_profile')
)
@user_passes_test(
    is_volunteer, redirect_field_name=None,
    login_url=reverse_lazy('home:dashboard')
)
# @permission_required
def update_cwhw(request):
    if request.method == 'POST':
        """ This POST Request won't be Generated (because there will be no means to generated it in the template) if
            1. Selected Date is not present in Calendar. (Already checked for above)
            2. Selected Day (from Date) and Section not present in Schedule. (Already checked for above and
                submit button will be disabled until AJAX is loaded completely)
            3. No Class Scheduled on Selected Date. (Already checked for above)
            4. User is not a Volunteer.
        """
        profile = Profile.objects.get(user=request.user)
        volun = Volunteer.objects.get(profile=profile)

        # Date and section selected before pressing submit button
        date_str = request.POST['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        cal_date = Calendar.objects.get(date=date)

        section_id = request.POST['section']
        section = Section.objects.get(section_id=section_id)

        # Update CW-HW
        cw = request.POST['cw']
        hw = request.POST['hw']
        comment = request.POST['comment']

        cw_hw = ClassworkHomework.objects.filter(cal_date=cal_date, section=section)
        if cw_hw.exists():
            cw_hw = cw_hw[0]
        else:
            cw_hw = ClassworkHomework(cal_date=cal_date, section=section, cw='', hw='', comment='')

        if cw:
            cw_hw.cw += f'{cw}\n - {profile.get_full_name}, {volun.roll_no}\n\n'
        if hw:
            cw_hw.hw += f'{hw}\n - {profile.get_full_name}, {volun.roll_no}\n\n'
        if comment:
            cw_hw.comment += f'{comment}\n - {profile.get_full_name}, {volun.roll_no}\n\n'

        cw_hw.save()

        messages.success(request, 'CW_HW update successful!')
        redirect_url = reverse('home:dashboard') + f'?d={date}&s={section_id}'
        return HttpResponseRedirect(redirect_url)

    return redirect('home:dashboard')


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
def ajax_dashboard(request):
    date_str = request.GET.get('class_date', None)
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    day = date.strftime("%w")
    data = {}
    schedule = Schedule.objects.filter(day=day).order_by('section__section_id')

    for sch in schedule:
        data[sch.section.section_id] = sch.section.name

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
def class_schedule(request):
    days = Schedule.DAY
    subjects = Schedule.SUBJECT
    data = {}
    #sections = Schedule.objects.order_by('section__section_id')
    schedule = Schedule.objects.order_by('day', 'section__section_id', 'subject' )
    sections = Section.objects.exclude(schedule=None).order_by('section_id')

    #print(sections)
    #for section in sections:
        #data[section.section.section_id] = section.section.name 
    
    context={
        'days': days,
        'subjects': subjects,
        #'sections': data,
        'sections': sections,
        'schedule': schedule
}
   
    return render(request, 'home/class_schedule.html',context)    