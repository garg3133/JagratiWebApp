//Nav button controls
const navbar_toggler = document.querySelector('.navbar-toggler i');
const left_nav = document.querySelector('.navbar .left-nav .navbar-nav');

function toggleNav() {
	document.querySelector('.left-nav').classList.toggle('open');
	navbar_toggler.classList.toggle('fa-bars');
	navbar_toggler.classList.toggle('fa-times');
	left_nav.classList.toggle('nav-collapsed');
}

navbar_toggler.addEventListener('click', function() {
	toggleNav();
});


window.onclick = function(e){
	// Navbar closes if clicks anywhere else
	if (!e.target.closest('.navbar')) {
		if (navbar_toggler.classList.contains('fa-times')) toggleNav();
	}

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

// SHOWCASE TEXT
const show_p_txt = "Give way to changing the lives of needy children through Education";
let i=0;
show_p();
function show_p(){	
	if(i < show_p_txt.length){
		document.getElementById("show-p").innerHTML += show_p_txt.charAt(i);
		i++;
		setTimeout(show_p, 50); //speed is in milliseconds
	}
}

