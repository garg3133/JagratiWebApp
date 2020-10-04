//Nav bar variables
const nav_height= "131px";

//Nav button controls

/*function nav_button(){
	var a = document.getElementById("inavbar2");
	a.style.padding="2px 5px 5px";
	a.style.height=nav_height;
	var a = document.getElementById("inav-button-close");
	a.style.display="block";
	var a = document.getElementById("inav-button");
	a.style.display="none";
}
function nav_button_close(){
	var a = document.getElementById("inavbar2");
	a.style.padding="0";
	a.style.height="0";
	var a = document.getElementById("inav-button-close");
	a.style.display="none";
	var a = document.getElementById("inav-button");
	a.style.display="block";
}
*/
function rotate_menu(x) {
  x.classList.toggle("change");
}
function nav_button() {
  var x = document.getElementById("nav");
  if (x.className === "navbar") {
    x.className += " responsive";
  } else {
    x.className = "navbar";
  }
}
function for_media_query(x){
	if (x.matches){
		document.getElementById("inavbar2").style.padding="0";
		document.getElementById("inavbar2").style.height="0px";
		document.getElementById("inav-button").style.display="block";
		document.getElementById("inav-button-close").style.display="none";

		document.querySelector(".disable_arrows").style.display="none";
	}
	else{
		document.getElementById("inavbar2").style.padding="0";
		document.getElementById("inavbar2").style.height="0px";
		document.getElementById("inav-button").style.display="none";
		document.getElementById("inav-button-close").style.display="none";

		document.querySelector(".disable_arrows").style.display="block";
	}
}

var x=window.matchMedia("(max-width:760px)");
for_media_query(x);
x.addListener(for_media_query);  /*Whenever value of x is changed, for_media_query is called.*/



window.onclick = function(e){
	// Navbar closes if clicks anywhere else
	if(!(e.target.matches('.navbut') || e.target.matches('.menu-icon'))){
		if(document.getElementById("inavbar2").style.height==="131px"){
			nav_button_close();
		}
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

//Google Map API
function myMap() {
	var mapProp= {
	  center:new google.maps.LatLng(23.1782409,80.0252362),
	  zoom:15,
	};
	var map = new google.maps.Map(document.getElementById("googleMap"),mapProp);
	var marker = new google.maps.Marker({position: mapProp.center});
	marker.setMap(map); 
}

// SHOWCASE TEXT
const show_p_txt = "give way to changing life of needy children Education";
let i=0;
show_p();
function show_p(){	
	if(i < show_p_txt.length){
		document.getElementById("show-p").innerHTML += show_p_txt.charAt(i);
		i++;
		setTimeout(show_p, 50); //speed is in milliseconds
	}
}