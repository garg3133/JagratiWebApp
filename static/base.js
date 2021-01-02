function rotate_menu(x)
{
	x.classList.toggle("change");
}

function nav_button()
{
	var x = document.getElementById("nav");

	if (x.className === "navbar")
		x.className += " responsive";
	else
		x.className = "navbar";
}

$(window).scroll(function() {
    if ($(window).scrollTop() > 20) {
        $('#sticky').addClass('floatingNav');
    } else {
        $('#sticky').removeClass('floatingNav');
    }
});

