from datetime import datetime, date

# import json
# from django.core.serializers.json import DjangoJSONEncoder
# from django.forms.models import model_to_dict

from accounts.models import Profile
from apps.volunteers.models import Volunteer, VolunteerSchedule


def database_context(request):
    profile = volun = volun_sch = None
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        if profile is not None and user.desig == "v":
            volun = Volunteer.objects.get(profile=profile)
        if volun is not None:
            volun_sch = VolunteerSchedule.objects.filter(volun=volun).first()

        # Student's dictionary for AJAX
        # students = Student.objects.all()
        # stu_dict = {}

        # for stu in students:
        # 	stu_dict[stu.id] = model_to_dict(stu)

        # stu_dict_json = json.dumps(stu_dict)

        # Volunteer's dictionary for AJAX
        # volunteers = Volunteer.objects.all()
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

        # return {
        #     'volunteer': volunteer,
        #     # 'volunteers': volunteers,
        #     # 'vol_dict_json' : vol_dict_json,
        #     'vol_schedule': vol_schedule,
        #     # 'vol_schedules': VolunteerSchedule.objects.all(),
        #     # 'schedules' : Schedule.objects.order_by('section__section_id'),
        #     # 'sch_dict_json' : sch_dict_json,
        #     # 'today_vol_att' : VolunteerAttendance.objects.filter(date=date.today()),
        #     # 'today_stu_att' : StudentAttendance.objects.filter(date=date.today()),
        #     # 'students' : students,
        #     # 'stu_dict_json' : stu_dict_json,
        # }

    return {
        "profile": profile,
        "volun": volun,
        "volun_sch": volun_sch,
    }
