# standard library
from calendar import monthrange
from datetime import date, datetime

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

# local Django
from accounts.models import Profile
from apps.misc.models import Initiative
from apps.students.models import StudentAttendance
from apps.volunteers.models import Volunteer, VolunteerAttendance
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


def new_index(request):
    if request.user.is_authenticated:
        return redirect('home:dashboard')
    initiatives = Initiative.objects.all()
    return render(request, 'new_home/index.html', {'initiatives': initiatives})

def calendar(request):
    if request.user.is_authenticated:
        return render(request, 'calendar.html')
    return render(request, 'calendar.html')


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
        schedule = Schedule.objects.filter(
            day=query_day, section__section_id=query_section)
        if schedule.exists():
            schedule = schedule[0]
        else:
            return redirect('home:dashboard')

        context = {
            'selected_date': query_date,
            'selected_section': query_section,
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
        cw_hw = ClassworkHomework.objects.filter(
            cal_date=calendar, section__section_id=query_section).first()
        context['cw_hw'] = cw_hw

        # Subject Scheduled
        subject_scheduled = schedule.get_subject_display()
        context['subject_scheduled'] = subject_scheduled

        # All subjects
        context['subjects'] = Schedule.SUBJECT

        # Students Attendance
        student_attendance = StudentAttendance.objects.filter(
            cal_date=calendar, present=True).order_by('student__school_class')
        context['student_attendance'] = student_attendance

        if student_attendance.exists():
            stu_att_village = {}
            stu_att_village['G'] = stu_att_village['M'] = stu_att_village['C'] = 0
            stu_att_village['A'] = stu_att_village['S'] = 0

            for stu_att in student_attendance:
                stu_att_village[stu_att.student.village] += 1

            # Mehgawan Side
            stu_att_village['MS'] = (stu_att_village['M'] + stu_att_village['C']
                                     + stu_att_village['A'] + stu_att_village['S'])

            context['stu_att_village'] = stu_att_village

        # Volunteers Attendance
        volun_attendance = VolunteerAttendance.objects.filter(
            cal_date=calendar, present=True).order_by('volun__roll_no')
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

        subject_taught = request.POST['subject_taught']

        # Update CW-HW
        cw = request.POST['cw']
        hw = request.POST['hw']
        comment = request.POST['comment']

        cw_hw = ClassworkHomework.objects.filter(
            cal_date=cal_date, section=section)
        if cw_hw.exists():
            cw_hw = cw_hw[0]
        else:
            cw_hw = ClassworkHomework(
                cal_date=cal_date, section=section, cw='', hw='', comment='')

        if cw:
            cw_hw.cw += f'{cw}\n - {profile.get_full_name}, {volun.roll_no}\n\n'
        if hw:
            cw_hw.hw += f'{hw}\n - {profile.get_full_name}, {volun.roll_no}\n\n'
        if comment:
            cw_hw.comment += f'{comment}\n - {profile.get_full_name}, {volun.roll_no}\n\n'

        if cw or hw or comment:
            cw_hw.subject_taught = subject_taught
            messages.success(request, 'CW_HW update successful!')
        else:
            messages.error(
                request, "Please enter something in CW, HW or comment.")

        cw_hw.save()

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

    all_sections = Section.objects.order_by('section_id')
    active_sections = all_sections.exclude(schedule=None)

    schedule = Schedule.objects.order_by(
        'day', 'section__section_id', 'subject')

    context = {
        'days': days,
        'subjects': subjects,
        'all_sections': all_sections,
        'active_sections': active_sections,
        'schedule': schedule,
    }

    return render(request, 'home/class_schedule.html', context)


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
def calendar(request):
    return render(request, 'home/calendar.html', {'today_date': date.today().strftime('%Y-%m-%d')})


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
def ajax_fetch_calendar(request):
    month = int(request.GET.get('month', date.today().month))
    year = int(request.GET.get('year', date.today().year))
    last_day_of_month = monthrange(year, month)[1]

    data = {}

    # Get class schedule for month
    class_schedule_dict = {}
    class_schedule = Schedule.objects.all()
    days_in_schedule = class_schedule.values_list('day', flat=True)
    for day in days_in_schedule:
        day_schedule = Schedule.objects.filter(day=day)
        day_str = str(day)
        class_schedule_dict[day_str] = []

        for schedule in day_schedule:
            class_schedule_dict[day_str].append({
                'section': schedule.section.name,
                'subject': schedule.get_subject_display()
            })

    # Prepare data dict to be sent for requested month
    month_calendar = Calendar.objects.filter(date__month=month, date__year=year).order_by('date')
    for cal in month_calendar:
        if cal.class_scheduled:
            data[cal.date.day] = {
                'status': 'class_scheduled',
                'schedule': class_schedule_dict.get(cal.date.strftime('%w'), None)
            }
        else:
            data[cal.date.day] = {
                'status': 'no_class_scheduled',
                'remark': cal.remark
            }

    for day in range(1, last_day_of_month+1):
        if day not in data:
            data[day] = {
                'status': 'no_calendar'
            }

    # Mark today in calendar
    today_date = date.today()
    if month == today_date.month and year == today_date.year:
        data[today_date.day]['today'] = True

    # Other data
    data['today_date'] = today_date.strftime('%Y-m-%d')
    data['last_day_of_month'] = last_day_of_month
    data['ind_of_first_day'] = datetime(year, month, 1).strftime('%w')

    return JsonResponse(data)