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
                    "html": "Error occuerd while processing your request"
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
                    "html": "Error occuerd while processing your request"
                }, 2000);
            }
        }
    });
});


function create_new_wallet() {

    currency_code = document.getElementById("create-wallet-currency-type").value;
    username = document.getElementById("loggin-username").value;

    if ((currency_code == "")|| (currency_code == null) || (currency_code == undefined)) {
    	M.toast({
    	    "html": "Please select currency code"
    	}, 2000);
        return;
    }
    CSRF_TOKEN = getCSRFToken();
    $.ajax({
        url: '/create-wallet/',
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
        },
        data: {
            username: username,
            currency_code: currency_code,
        },
        success: function(response) {
            if (response["status"] == 200) {
                setTimeout(function() {
                    window.location.reload()
                }, 2000);

                M.toast({
                    "html": "Wallet Created"
                }, 2000);
            } 
            else {
                M.toast({
                    "html": "Error occuerd while processing your request"
                }, 2000);
            }
        }
    });
};


function add_money_to_wallet() {

    username = document.getElementById("loggin-username").value;
    add_money_amount = document.getElementById("add-money-amount").value;

    if ((add_money_amount == "")||(add_money_amount<0) || (add_money_amount==0)) {
    	M.toast({
    	    "html": "Please enter valid Amount"
    	}, 2000);
        return;
    }
    CSRF_TOKEN = getCSRFToken();
    $.ajax({
        url: '/add-money-to-wallet/',
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
        },
        data: {
            username: username,
            amount: add_money_amount,
        },
        success: function(response) {
            if (response["status"] == 200) {
                setTimeout(function() {
                    window.location.reload();
                }, 2000);

                M.toast({
                    "html": "Amount added to your Wallet!!!"
                }, 2000);
            }
            else {
                M.toast({
                    "html": "Error occuerd while processing your request"
                }, 2000);
            }
        }
    });
};


function send_money_to_wallet() {

    from_username = document.getElementById("loggin-username").value;
    to_username = document.getElementById("send-money-to-username").value;
    amount = document.getElementById("send-money-amount").value;

    if (to_username == "") {
    	M.toast({
    	    "html": "Please enter username"
    	}, 2000);
        return;
    }

    if ((amount == "")||(amount<0) || (amount==0)) {
    	M.toast({
    	    "html": "Please enter valid Amount"
    	}, 2000);
        return;
    }
    CSRF_TOKEN = getCSRFToken();
    $.ajax({
        url: '/send-money-to-user/',
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
        },
        data: {
            from_username: from_username,
            to_username: to_username,
            amount: amount,
        },
        success: function(response) {
            if (response["status"] == 200) {
                setTimeout(function() {
                    window.location.reload();
                }, 2000);

                M.toast({
                    "html": "Ammount is successfully sent to "+to_username+" !!!"
                }, 2000);
            } else if (response["status"] == 301) {
                M.toast({
                    "html": "Entered username not found. Please check and try again."
                }, 2000);
            } else if (response["status"] == 302) {
                M.toast({
                    "html": "Entered amount is greater than the total money in wallet. Please add money and try again"
                }, 2000);
            }
            else {
                M.toast({
                    "html": "Error occuerd while processing your request"
                }, 2000);
            }
        }
    });
};


function convert_currency() {
	document.getElementById("converted-currency-div").style.display = 'none'
    amount = document.getElementById("convert-currency-amount").value;
    from_currency_code = document.getElementById("convert-from-currency-code").value;
    to_currency_code = document.getElementById("convert-to-currency-code").value;

    if ((from_currency_code == "")|| (from_currency_code == null) || (from_currency_code == undefined)) {
    	M.toast({
    	    "html": "Please select currency code"
    	}, 2000);
        return;
    }
    if ((to_currency_code == "")|| (to_currency_code == null) || (to_currency_code == undefined)) {
    	M.toast({
    	    "html": "Please select currency code"
    	}, 2000);
        return;
    }
    if ((amount == "")||(amount<0) || (amount==0)) {
    	M.toast({
    	    "html": "Please enter valid Amount"
    	}, 2000);
        return;
    }
    CSRF_TOKEN = getCSRFToken();
    $.ajax({
        url: '/convert-currency/',
        type: "POST",
        headers: {
            'X-CSRFToken': CSRF_TOKEN,
        },
        data: {
            from_currency_code: from_currency_code,
            to_currency_code: to_currency_code,
            amount: amount,
        },
        success: function(response) {
            if (response["status"] == 200) {
            	html = '<div class="col s6 l6 m6 offset-m3 offset-l3 offset-s3"><p> '+from_currency_code.toUpperCase()+amount+' = '+to_currency_code.toUpperCase()+response['converted_amount']+'</p></div>'
            	document.getElementById("converted-currency-div").innerHTML = html
            	document.getElementById("converted-currency-div").style.display = 'block'
            }
            else {
                username_elmt.focus()
                M.toast({
                    "html": "Error occuerd while processing your request"
                }, 2000);
            }
        }
    });
};

