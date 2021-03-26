from datetime import date
from datetime import timedelta

import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required, user_passes_test, permission_required
)
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

# third-party
from openpyxl import load_workbook

from home.models import Calendar, Schedule
from home.views import has_authenticated_profile
from .models import Student, StudentAttendance, StudentSchedule

# GLOBAL VARIABLES
today_date = date.today()
today_day = today_date.strftime("%w")


# VIEWS FUNCTIONS

@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
def index(request):
    return HttpResponse('Hello there!')


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
def profile(request, pk):
    """View student profile."""
    profile = get_object_or_404(Student, id=pk)
    context = {
        'profile': profile
    }
    return render(request, 'students/profile.html', context)


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
@permission_required('students.add_student', raise_exception=True)
def new_student(request):
    """Add new student."""
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        school_class = request.POST['school_class']
        village = request.POST['village']
        contact_no = request.POST.get('contact_no')  # Non-required field
        guardian_name = request.POST['guardian_name']
        profile_image = request.FILES.get('profile_image')

        student = Student(
            first_name=first_name, last_name=last_name,
            gender=gender, profile_image=profile_image,
            school_class=school_class, village=village,
            contact_no=contact_no, guardian_name=guardian_name,
        )
        student.save()

        messages.success(request, "Student added successfully!")
        return redirect('students:new_student')

    return render(request, 'students/new_student.html', {'villages': Student.VILLAGE})


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
@permission_required('students.change_student', raise_exception=True)
def update_profile(request, pk):
    """Update student profile."""
    profile = get_object_or_404(Student, id=pk)
    villages = Student.VILLAGE

    context = {
        'profile': profile,
        'villages': villages,
    }

    if request.method == 'POST':
        profile.first_name = request.POST['first_name']
        profile.last_name = request.POST['last_name']
        profile.gender = request.POST['gender']
        profile.school_class = request.POST['school_class']
        profile.village = request.POST['village']
        profile.contact_no = request.POST['contact_no']
        profile.guardian_name = request.POST['guardian_name']
        if 'profile_image' in request.FILES:
            # Delete the previous profile image.
            profile.profile_image.delete(False)
            profile.profile_image = request.FILES.get('profile_image')
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('students:profile', pk=pk)

    return render(request, 'students/update_profile.html', context)


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
# @permissions_required
def attendance(request):
    """Student attendance page."""
    today_cal = Calendar.objects.filter(date=today_date)
    # TO BE REMOVED...
    # Update today's date in Calendar if not already there
    if today_cal.exists():
        today_cal = today_cal[0]
    else:
        today_cal_new = Calendar(date=today_date)
        today_cal_new.save()
        today_cal = Calendar.objects.get(date=today_date)
    # ...TILL HERE

    context = {
        'today_date': today_date,
    }

    if not today_cal.class_scheduled:
        context['no_class_today'] = True
        return render(request, 'students/attendance.html', context)

    today_stu_sch = StudentSchedule.objects.filter(day=today_day)
    today_stu_att = StudentAttendance.objects.filter(cal_date__date=today_date)

    if not today_stu_att.exists():
        # Create Empty Student Attendance Instances
        for stu_sch in today_stu_sch:
            stu_attendance = StudentAttendance(
                student=stu_sch.student, cal_date=today_cal)
            stu_attendance.save()
    elif today_stu_att.count() != today_stu_sch.count():
        # Some new students added in today's schedule (not necessarily present today)
        for stu_sch in today_stu_sch:
            if not today_stu_att.filter(student=stu_sch.student).exists():
                stu_attendance = StudentAttendance(
                    student=stu_sch.student, cal_date=today_cal)
                stu_attendance.save()

    context['stu_att_today'] = StudentAttendance.objects.filter(
        cal_date=today_cal, student__school_class__range=(1, 3)).order_by(
        'student__school_class', 'student__first_name', 'student__last_name')

    return render(request, 'students/attendance.html', context)


@login_required
@user_passes_test(
    has_authenticated_profile, redirect_field_name=None,
    login_url=reverse_lazy('accounts:complete_profile')
)
# @permissions_required
def ajax_fetch_students(request):
    """Fetch students based on class-group selected on student attendance page."""
    today_cal = Calendar.objects.get(date=today_date)
    data = {}
    stu_class = request.GET.get('stu_class', None)
    class_range_min, class_range_max = stu_class.split('-')

    stu_att_today = StudentAttendance.objects.filter(
        cal_date=today_cal, student__school_class__range=(
            class_range_min, class_range_max),
    ).order_by('student__school_class', 'student__first_name', 'student__last_name')

    for stu_att in stu_att_today:
        # key --> For sorting purpose.
        key = str(stu_att.student.school_class) + stu_att.student.get_full_name
        data[key] = [stu_att.id, stu_att.student.id, stu_att.student.get_full_name,
                     stu_att.student.school_class, stu_att.present]

    return JsonResponse(data)


@login_required
@user_passes_test(
    has_authenticated_profile, redirect_field_name=None,
    login_url=reverse_lazy('accounts:complete_profile')
)
# @permissions_required
def ajax_mark_attendance(request):
    """Mark/unmark student attendance."""
    stu_id = request.GET['std_id']
    is_present = request.GET['is_present']
    stu_att = StudentAttendance.objects.get(
        student__id=stu_id, cal_date=today_date)
    stu_att.present = True if is_present == 'true' else False
    stu_att.save()
    data = {'success': True}
    return JsonResponse(data)


def ajax_mark_homework(request):
    if request.method == 'POST' and request.is_ajax():
        stu_id = request.POST.get('stu_id')
        is_homework_done = request.POST.get('is_homework_done')
        student = StudentAttendance.objects.get(
            student__id=stu_id, cal_date=(today_date - timedelta(days = 1)))
        student.hw_done = True if is_homework_done == 'true' else False
        student.save()
        data = {'success': True}
        return JsonResponse(data)


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
# @permissions_required
def update_from_sheets(request):
    """Create Student model instances from excel sheet."""
    if request.method == 'POST':
        sheet = request.FILES['sheet']
        # Temporarily save the file
        fs = FileSystemStorage(location=settings.TEMP_ROOT)
        filename = fs.save(sheet.name, sheet)
        file_path = os.path.join(settings.TEMP_ROOT, filename)
        # Process the file
        wb_obj = load_workbook(file_path)
        sheet_obj = wb_obj.active
        max_row = sheet_obj.max_row

        for i in range(3, max_row + 1):
            first_name = sheet_obj.cell(row=i, column=2).value
            last_name = sheet_obj.cell(row=i, column=3).value
            school_class = sheet_obj.cell(row=i, column=4).value
            village = sheet_obj.cell(row=i, column=5).value
            guardian_name = sheet_obj.cell(row=i, column=6).value
            contact_no = sheet_obj.cell(row=i, column=7).value

            if not Student.objects.filter(first_name=first_name, last_name=last_name, school_class=school_class,
                                          village=village, guardian_name=guardian_name).exists():
                student = Student(first_name=first_name, last_name=last_name, school_class=school_class,
                                  village=village, guardian_name=guardian_name)
                if contact_no is not None:
                    student.contact_no = contact_no
                student.save()
                for day, day_name in Schedule.DAY:
                    print(day)
                    stu_sch = StudentSchedule(student=student,
                                              schedule=Schedule.objects.get(day=day, section__section_id='4A'))
                    stu_sch.save()
        # Delete the file
        os.remove(file_path)
        messages.success(request, "Data Updated Successfully")
        return redirect('students:index')

    return render(request, 'students/update_from_sheets.html')
