
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');


signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
	document.querySelectorAll('.form-error')[1].innerHTML="";
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
	document.querySelectorAll('.form-error')[0].innerHTML="";
});
