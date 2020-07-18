from .models import(
    Volunteer,
    Student,
    # Calendar,
    # Section,
    # Schedule,
    StudentSchedule,
    VolunteerSchedule,
    # ClassworkHomework,
    StudentAttendence,
    VolunteerAttendence,
)
from datetime import datetime, date
# import json
# from django.core.serializers.json import DjangoJSONEncoder
# from django.forms.models import model_to_dict

def database_context(request):
    if request.user.is_authenticated:
        # Logged in Volunteer's data
        obj = Volunteer.objects.filter(email=request.user)
        if obj.exists():
            volunteer = obj[0]
            obj2 = VolunteerSchedule.objects.filter(roll_no=volunteer)
            if obj2.exists():
                vol_schedule = obj2[0]
            else:
                vol_schedule = None
        else:
            volunteer = None
            vol_schedule = None

        # Student's dictionary for AJAX
        students = Student.objects.all()
        # stu_dict = {}
        
        # for stu in students:
        # 	stu_dict[stu.id] = model_to_dict(stu)

        # stu_dict_json = json.dumps(stu_dict)

        # Volunteer's dictionary for AJAX
        volunteers = Volunteer.objects.all()
        # vol_dict = {}
        
        # for vol in volunteers:
        # 	vol_dict[vol.id] = model_to_dict(vol)

        # vol_dict_json = json.dumps(vol_dict, cls=DjangoJSONEncoder)  # For encoding date

        # Schedule dictionary for AJAX
        # schedules = Schedule.objects.all()
        # sch_dict = {}
        
        # for sch in schedules:
        # 	sch_dict[sch.id] = model_to_dict(sch)

        # sch_dict_json = json.dumps(sch_dict)

        return {
            'volunteer': volunteer,
            'volunteers': volunteers,
            # 'vol_dict_json' : vol_dict_json,
            'vol_schedule': vol_schedule,
            'vol_schedules': VolunteerSchedule.objects.all(),
            # 'schedules' : Schedule.objects.order_by('section__section_id'),
            # 'sch_dict_json' : sch_dict_json,
            'today_vol_att' : VolunteerAttendence.objects.filter(date=date.today()),
            'today_stu_att' : StudentAttendence.objects.filter(date=date.today()),
            'students' : students,
            # 'stu_dict_json' : stu_dict_json,
        }

    else:
        return {}