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

$(window).scroll(function() {
    if ($(window).scrollTop() > 20) {
        $('#sticky').addClass('floatingNav');
    } else {
        $('#sticky').removeClass('floatingNav');
    }
});

window.onclick = function(e){
	// Donate us modal close
	if(e.target == don_modal){
		don_modal.style.display="none";
	}
}

// Donate Us Modal Close
const don_modal = document.getElementById("don-modal");
function donate_us(){
	don_modal.style.display="block";
}
const modal_cl = document.getElementById("don-close");
modal_cl.onclick = function(){
	don_modal.style.display="none";
}


