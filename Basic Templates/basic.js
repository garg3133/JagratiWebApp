
window.onclick = function(e){
	// Donate us modal close
	if(e.target == don_modal){
		don_modal.style.display="none";
	}
}

// NAVBAR MEDIA QUERIES
let nav_media = window.matchMedia("(max-width:450px)");
nav_media_query(nav_media);
nav_media.addListener(nav_media_query);
function nav_media_query(nav_media){
	if(nav_media.matches){
		document.querySelector(".breadcrumb li+li").innerHTML="Alumni";
	}
	else{
		document.querySelector(".breadcrumb li+li").innerHTML="Alumni Association";
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
