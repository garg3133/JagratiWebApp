
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

const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');

togglePassword.addEventListener('click', function (e) {

	// toggle the type attribute
	const type = password.getAttribute('type');
	
	if(type == "password"){
		password.setAttribute('type', "text");
		// toggle the eye slash icon
		togglePassword.src = "/static/accounts/icon/eye.svg"

		//Toggle the tooltip
		togglePassword.title = "Hide Password"
	}
	else{
		password.setAttribute('type', "password");
		// toggle the eye slash icon
		togglePassword.src = "/static/accounts/icon/eye-slash.svg"
		
		//Toggle the tooltip
		togglePassword.title = "Show Password"
	}

});