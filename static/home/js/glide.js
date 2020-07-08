var glide = new Glide('.glide',{
  			type: 'slider',
  			focusAt: 'center',
  			perView: 2,
  			autoplay: 2000,
  			gap: 30,
  			breakpoints: {
  				760:{
  					perView: 1,

  				}
  			}
  		})

var ele = document.querySelectorAll(".glide__slides li")
var ele1 = document.querySelectorAll(".glide__slide--clone")
// ele1[1].classList.add("llll")
// ele1[2].classList.add("rrrr")
console.log(ele1)

glide.on(['mount.after', 'run'], function () {
  var a = glide.index
  // var l= a==0?8:a-1
  // var r= a==8?0:a+1
  // console.log(ele[l]);
  // console.log(ele[r]);
  for(let i=0; i<9; i++){
  	ele[i].classList.remove("rrrr");
  	ele[i].classList.remove("llll");
  }
  if(a!=0) ele[a-1].classList.add("llll");
  // ele[l].classList.remove("rrrr");
  // ele[r].classList.remove("llll");
  if(a!=8) ele[a+1].classList.add("rrrr");
  // ele[a].classList.remove("rrrr");
  // ele[a].classList.remove("llll");

})

glide.mount()

// 
for(let i=0; i<9; i++){	
	document.querySelectorAll(".card")[i].addEventListener('touchstart', function(e) {
		e.preventDefault();
		document.querySelectorAll(".card")[i].classList.add("card_hover");
		document.querySelectorAll(".card1")[i].classList.add("card1_hover");
		document.querySelectorAll(".card_h2")[i].classList.add("h_hover");
	}, false);
	document.querySelectorAll(".card")[i].addEventListener('touchend', function() {
		document.querySelectorAll(".card")[i].classList.remove("card_hover");
		document.querySelectorAll(".card1")[i].classList.remove("card1_hover");
		document.querySelectorAll(".card_h2")[i].classList.remove("h_hover");
	}, false);
}
// console.log(document.querySelector("#initiatives h2"));