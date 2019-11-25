from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import(
	Volunteer,
	Student,
	Schedule,
	Volunteer_schedule,
	Student_schedule,
	Cw_hw,
	Calendar,
	Volunteer_attended_on,
	Student_attended_on,
)
from django.http import HttpResponse
from datetime import datetime, date

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	return render(request, 'home/index.html')

def dashboard(request):
	if request.user.is_authenticated:
		email = request.user

		if not Volunteer.objects.filter(email=email).exists():
			return redirect('set_profile')
		
		if request.method == 'POST':
			if request.POST.get('submit') == 'class-info':
				class_info_date_str		= request.POST['class-info-date']
				class_info_section		= request.POST['class-info-section']
				
				class_info_date = datetime.strptime(class_info_date_str, '%Y-%m-%d').date()
				class_info_day = class_info_date.strftime("%A")

				calendar = Calendar.objects.filter(date = class_info_date)
				if calendar.exists():
					if calendar[0].class_scheduled is True:
						schedule = Schedule.objects.filter(day = class_info_day, section = class_info_section)
						if schedule.exists():
							if class_info_date > date.today():
								students_attended = "Not yet updated!"
							else:
								students_attended = Student_attended_on.objects.filter(date = calendar[0])
								if class_info_date == date.today() and not students_attended.exists():
									students_attended = "Not yet updated!"
								elif not students_attended.exists():
									students_attended = "No student present."
							cw_hw = Cw_hw.objects.filter(date = class_info_date, section = schedule[0])
							if cw_hw.exists():
								context = {
									#dash-main
									'schedule' : schedule,
									'students_attended' : students_attended,
									'cw_hw' : cw_hw[0],
									'selected_date' : class_info_date,
									'selected_schedule' : class_info_section,
									'choices': Schedule.SECTION,

									#dash-update
									'last_4_year': datetime.now().year - 4,
								}
								return render(request, 'home/dashboard.html', context)
							else:
								context = {
									#dash-main
									'schedule' : schedule,
									'students_attended' : students_attended,
									'cw_hw' : {
										'cw' : "Not yet updated!",
										'hw' : "Not yet updated!",
									},
									'selected_date' : class_info_date,
									'selected_schedule' : class_info_section,
									'choices': Schedule.SECTION,

									#dash-update
									'last_4_year': datetime.now().year - 4,
								}
								return render(request, 'home/dashboard.html', context)
						else:
							context = {
								#dash-main
								'no_schedule_found' : "yup!",
								'selected_date' : class_info_date,
								'selected_schedule' : class_info_section,
								'choices': Schedule.SECTION,

								#dash-update
								'last_4_year': datetime.now().year - 4,
							}
							return render(request, 'home/dashboard.html', context)  # The chosen section is not taught on the chosen day
					else:
						context = {
							#dash-main
							'calendar' : calendar[0],
							'no_class_scheduled' : "haan",
							'selected_date' : class_info_date,
							'selected_schedule' : class_info_section,
							'choices': Schedule.SECTION,

							#dash-update
							'last_4_year': datetime.now().year - 4,
						}
						return render(request, 'home/dashboard.html', context)
				else:
					context = {
						#dash-main
						'no_class_found' : "bilkul_nhi",
						'selected_date' : class_info_date,
						'selected_schedule' : class_info_section,
						'choices': Schedule.SECTION,

						#dash-update
						'last_4_year': datetime.now().year - 4,
					}
					return render(request, 'home/dashboard.html', context)
			elif request.POST.get('submit') == 'update-profile':
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

				volun = Volunteer.objects.get(email = request.user)
				update_error = ""
				toast = ""
				if roll_no:
					if volun.roll_no != roll_no:
						duplicate_roll_check = Volunteer.objects.filter(roll_no = roll_no)
						if duplicate_roll_check.exists():
							update_error = "A volunteer with entered roll no. already exists."
							toast = "Profile update failed!"
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

				if update_error == "":
					volun.save()
					toast = "Profile updated Successfully!"


				context = {
					#dash-main
					'class_info_submitted' : "nooooo!",
					'choices': Schedule.SECTION,

					#dash-update
					'update_error' : update_error,
					'last_4_year': datetime.now().year - 4,
					'toast': toast,
				}
				return render(request, 'home/dashboard.html', context)
		else:
			context = {
				#dash-main
				'class_info_submitted' : "nopes",
				'choices': Schedule.SECTION,

				#dash-update
				'last_4_year': datetime.now().year - 4,
			}
			return render(request, 'home/dashboard.html', context)
	return redirect('home')

def volunteerInformation(request):
	if request.user.is_authenticated:
		schedules = Schedule.objects.all()
		email = request.user
		if Volunteer.objects.filter(email=email).exists():
			return redirect('dashboard')
		if request.method == 'POST':
			# roll = str(email)
			# rollnum = roll.split('@')[0]
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
			# sch_id          = request.POST['schedule']
			# sch_day         = Schedule.objects.get(id = sch_id).day
			vol_obj = Volunteer(
				email           = email,
				roll_no         = roll_no,
				first_name      = first_name,
				last_name       = last_name,
				gender          = gender,
				city            = city,
				state           = state,
				dob             = dob,
				contact_no      = contact_no,
				pincode         = pincode,
				programme       = programme,
				batch           = batch,
				alt_email       = alt_email,     
				street_address1 = street_address1,
				street_address2 = street_address2,
			)
			vol_obj.save()
			# sch_obj = Volunteer_schedule(
			# 	roll_no         = Volunteer.objects.get(roll_no = roll_no),
			# 	day             = sch_day,
			# 	schedule        = Schedule.objects.get(id = sch_id),
			# )
			
			# sch_obj.save()
			
			return redirect('dashboard')
		
		return render(request, 'home/set_profile.html', {
			'cur_year': datetime.now().year - 4,
			# 'schedule': schedules,
			})
	else:
		return redirect('login_signup')

		