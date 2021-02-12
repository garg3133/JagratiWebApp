from django.shortcuts import render, redirect

from .models import Feedback

# Create your views here.


def index(request):
    submitted = ""
    if request.method == "POST":
        anonymous_array = request.POST.getlist("anonymousCheck")
        name = request.POST["name"]
        roll_no = request.POST["rollNo"]
        email = request.POST["email"]
        feedback = request.POST["feedback"]
        if len(anonymous_array) != 0:
            feedback = Feedback(name="Anonymous", feedback=feedback)
            feedback.save()
        else:
            feedback = Feedback(
                name=name, roll_no=roll_no, email=email, feedback=feedback
            )
            feedback.save()
        return redirect("feedbacks:feedback_submitted")

    context = {
        "logout_redirect_site": request.path,
        "login_redirect_site": request.path,
    }
    return render(request, "feedbacks/index.html", context)


def feedback_submitted(request):
    return render(request, "feedbacks/feedback_submitted.html")
