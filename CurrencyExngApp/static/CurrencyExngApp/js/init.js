$('select').formSelect();
$('.modal').modal();

function getCSRFToken() {
    return $('input[name="csrfmiddlewaretoken"]').val();
}

function stripHTML(htmlString) {
    return htmlString.replace(/<[^>]+>/g, '');
}

document.body.addEventListener('keypress', function(e) {
    if ((e.target.id == "username") || (e.target.id == "password")) {
        if (e.keyCode == 13) {
            $("#login-btn").click();
        }
    }
    if ((e.target.id == "register-username") || (e.target.id == "register-password") || (e.target.id == "register-retype-password")) {
        if (e.keyCode == 13) {
            $("#register-btn").click();
        }
    }
});

$(document).on("click", "#login-btn", function(e) {

    username_elmt = document.getElementById("username");
    username = username_elmt.value;
    password_elmt = document.getElementById("password");
    password = password_elmt.value;

    if (username == "") {
    	M.toast({
    	    "html": "Please enter username"
    	}, 2000);
        return;
    }
    if (password == "") {
    	M.toast({
    	    "html": "Please enter password"
    	}, 2000);
        return;
    }
    CSRF_TOKEN = getCSRFToken();
    $.ajax({
        url: '/authentication/',
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
        },
        data: {
            username: username,
            password: password,
        },
        success: function(response) {

            if (response["status"] == 200) {
                setTimeout(function() {
                    window.location = '/home/';
                }, 2000);

                M.toast({
                    "html": "Welcome "+username
                }, 2000);
            } else if (response["status"] == 301) {
                username_elmt.focus()
                M.toast({
                    "html": "Entered username not found. Please check and try again."
                }, 2000);
            } else if (response["status"] == 302) {
                password_elmt.value = "";
                password_elmt.focus()
                M.toast({
                    "html": "You have entered wrong password. Please check and try again."
                }, 2000);
            } 
            else {
                username_elmt.focus()
                M.toast({
                    "html": "Error occuerd while processing"
                }, 2000);
            }
        }
    });
});

$(document).on("click", "#register-btn", function(e) {

    username_elmt = document.getElementById("register-username");
    username = username_elmt.value;
    password_elmt = document.getElementById("register-password");
    password = password_elmt.value;
    retype_password = document.getElementById("register-retype-password").value;

    if (username == "") {
    	M.toast({
    	    "html": "Please enter username"
    	}, 2000);
        return;
    }
    if (password == "") {
    	M.toast({
    	    "html": "Please enter password"
    	}, 2000);
        return;
    }
    if (password != retype_password) {
    	M.toast({
    	    "html": "Your password and confirmation password do not match."
    	}, 2000);
        return;
    }
    CSRF_TOKEN = getCSRFToken();
    $.ajax({
        url: '/register/',
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
        },
        data: {
            username: username,
            password: password,
        },
        success: function(response) {
            if (response["status"] == 200) {
                setTimeout(function() {
                    window.location = '/login/';
                }, 2000);

                M.toast({
                    "html": "Registration Completed!!!"
                }, 2000);
            } else if (response["status"] == 301) {
                password_elmt.focus()
                M.toast({
                    "html": "Entered username not found. Please check and try again."
                }, 2000);
            } 
            else {
                username_elmt.focus()
                M.toast({
                    "html": "Error occuerd while processing"
                }, 2000);
            }
        }
    });
});

