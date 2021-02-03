from datetime import datetime, date

import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

# third-party
from openpyxl import load_workbook

from accounts.models import Profile
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
# @permissions_required
def new_student(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        school_class = request.POST['school_class']
        village = request.POST['village']
        contact_no = request.POST.get('contact_no')  # Non-required field
        guardian_name = request.POST['guardian_name']

        student = Student(
            first_name=first_name, last_name=last_name,
            gender=gender, school_class=school_class,
            village=village, contact_no=contact_no,
            guardian_name=guardian_name,
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
# @permissions_required
def attendance(request):
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
        'today_date' : today_date,
    }

    if today_cal.class_scheduled:
        if not StudentAttendance.objects.filter(cal_date__date=today_date).exists():
            # Create Empty Student Attendance Instances
            today_stu_sch = StudentSchedule.objects.filter(day=today_day)
            for stu_sch in today_stu_sch:
                stu_attendance = StudentAttendance(student=stu_sch.student, cal_date=today_cal)
                stu_attendance.save()

        elif StudentAttendance.objects.filter(cal_date__date=today_date).count() != StudentSchedule.objects.filter(day=today_day).count():
            # Some new students added in today's schedule (not necessarily present today)
            today_stu_sch = StudentSchedule.objects.filter(day=today_day)
            for stu_sch in today_stu_sch:
                if not StudentAttendance.objects.filter(student=stu_sch.student, cal_date=today_cal).exists():
                    stu_attendance = StudentAttendance(student=stu_sch.student, cal_date=today_cal)
                    stu_attendance.save()
    else:
        context['no_class_today'] = True
        return render(request, 'students/attendance.html', context)

    if request.method == 'POST':
        stu_array = request.POST.getlist('attended')
        selected_class = request.POST['selected_class']

        # class_range = selected_class.split('-')
        # class_range_min = class_range[0]
        # class_range_max = class_range[1]
        class_range_min, class_range_max = selected_class.split('-')

        # Mark everyone's absent
        stu_att_today = StudentAttendance.objects.filter(
            cal_date=today_cal, student__school_class__range=(class_range_min, class_range_max))
        for stu_att in stu_att_today:
            stu_att.present = False
            stu_att.save()

        for stu_id in stu_array:
            stu_att = StudentAttendance.objects.get(student__id=stu_id, cal_date=today_date)
            stu_att.present = True
            stu_att.save()

        messages.success(request, 'Attendance marked successfully!')
        return redirect('students:attendance')

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
def ajax_attendance(request):
    today_cal = Calendar.objects.get(date=today_date)
    data = {}
    stu_class = request.GET.get('stu_class', None)
    class_range_min, class_range_max = stu_class.split('-')

    stu_att_today = StudentAttendance.objects.filter(
        cal_date=today_cal, student__school_class__range=(class_range_min, class_range_max),
    ).order_by('student__school_class', 'student__first_name', 'student__last_name')

    for stu_att in stu_att_today:
        key = str(stu_att.student.school_class) + stu_att.student.get_full_name  # For sorting purpose.
        data[key] = [stu_att.student.id, stu_att.student.get_full_name, stu_att.student.school_class, stu_att.present]

    return JsonResponse(data)


@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
# @permissions_required
def update_from_sheets(request):

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

        for i in range(3, max_row+1):
            first_name = sheet_obj.cell(row=i, column=2).value
            last_name = sheet_obj.cell(row=i, column=3).value
            school_class = sheet_obj.cell(row=i, column=4).value
            village = sheet_obj.cell(row=i, column=5).value
            guardian_name = sheet_obj.cell(row=i, column=6).value
            contact_no = sheet_obj.cell(row=i, column=7).value

            if not Student.objects.filter(first_name=first_name, last_name=last_name, school_class=school_class, village=village, guardian_name=guardian_name).exists():
                student = Student(first_name=first_name, last_name=last_name, school_class=school_class, village=village, guardian_name=guardian_name)
                if contact_no is not None:
                    student.contact_no = contact_no
                student.save()
                for day, day_name in Schedule.DAY:
                    print(day)
                    stu_sch = StudentSchedule(student=student, schedule=Schedule.objects.get(day=day, section__section_id='4A'))
                    stu_sch.save()
        # Delete the file
        os.remove(file_path)
        messages.success(request, "Data Updated Successfully")
        return redirect('students:index')

    return render(request, 'students/update_from_sheets.html')

#update student profile

@login_required
@user_passes_test(
    has_authenticated_profile,
    login_url=reverse_lazy('accounts:complete_profile')
)
def update_profile(request, pk):
    profile = get_object_or_404(Student, id=pk)

    context = {
        'profile': profile,
    }

    if request.method == 'POST':

        profile.first_name = request.POST['first_name']
        profile.last_name = request.POST['last_name']
        profile.gender = request.POST['gender']
        profile.school_class = request.POST['school_class']
        profile.village = request.POST['village']
        profile.contact_no = request.POST['contact_no']
        profile.guardian_name = request.POST['guardian_name']
        profile.save()

        messages.success(request, 'Profile updated Successfully!')
        return redirect('students:index')

    return render(request, 'students/update_profile.html', context)


