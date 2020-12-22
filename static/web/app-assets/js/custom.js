function login(token) {
    var settings = {
        "url": "/api/login/",
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $("#csrf").val(),
        },
        "data": {
            "token": token,
        },
        error: function(response) {
            swal("Failed!", "Login not successful");
        },
        success: function(response) {
            var result_data = response["data"];
            for (var it in $.cookie()) $.removeCookie(it);
            document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });
            document.cookie = "signedIn=true; path=/";
            $.each(result_data, function(key, value) {
                $.cookie(key.toString(), value.toString());
                document.cookie = key.toString() + "=" + value.toString() + "; path=/";

            })
            window.location.href = "/web/dashboard/";

        }
    };

    $.ajax(settings).done(function(response) {

    });
}

function fblogin() {
    FB.login(function(response) {
        console.log(response)
        if (response.authResponse) {
            login(response.authResponse.accessToken);
        } else {
            swal("Failed!", "Login not successful");
        }
    });
}


function setprofile() {
    if ($.cookie("signedIn") == "true") {
        document.getElementById("uname").innerText = $.cookie("name");
        document.getElementById("uimage").src = $.cookie("profile_pic");
    }
}



function getpages() {
    var settings = {
        "url": "/api/pages/",
        "method": "GET",
        "timeout": 0,
        "headers": {
            "Authorization": "token " + $.cookie("token"),
            "X-CSRFToken": $("#csrf").val(),

        },
        success: function(response) {
            var element = $("#pagelist");
            element.empty();
            $.each(response.data, function(index, value) {
                var img = value.page_icon;
                if (img.length == 0) {
                    img = "static/web/app-assets/images/portrait/small/avatar-s-5.jpg"
                }


                var content = '<tr>' +
                    '<td>Facebook<br>' + value.page_id + '</td>' +
                    // '<td>' + value.page_id + '</td>' +
                    '<td>' +
                    '<ul class="list-unstyled users-list m-0  d-flex align-items-center">' +
                    '<li data-toggle="tooltip" data-popup="tooltip-custom" data-placement="bottom" data-original-title="' + value.title + '" class="avatar pull-up">' +
                    '<img class="media-object rounded-circle" src="' + img + '" alt="Avatar" height="30" width="30">' +
                    '</li>' +
                    '</ul>' +
                    value.title + '<br>' +
                    '</td>' +
                    '<td>' + value.details.email + '</td>' +
                    '<td>' + value.details.about + '</td>' +
                    '<td>' + value.details.website + '</td>' +
                    '<td>' + value.details.phone + '</td>' +
                    // '<td class="p-1">' +

                    // '</td>' +
                    // '<td>' + new Date(value.created_at) + '</td>' +
                    '<td>' +
                    '<button type="button" class="btn bg-gradient-primary mr-1 mb-1 waves-effect waves-light" onclick="updatepage(' + value.id + ')">Update</button>' +
                    '</td>' +
                    '</tr>';
                element.append(content);


            });


        }
    };

    $.ajax(settings).done(function(response) {

    });
}




function updatepage(id) {
    $("#pid").val(id);
    var settings = {
        "url": "/api/pages/" + id.toString() + "/",
        "method": "GET",
        "timeout": 0,
        "headers": {
            "Authorization": "token " + $.cookie("token"),
            "X-CSRFToken": $("#csrf").val(),
        },
        success: function(response) {
            $("#pmail").val(response.data.details.email);
            $("#pphone").val(response.data.details.phone);
            $("#pabout").val(response.data.details.about);
            $("#pweb").val(response.data.details.website);
            $("#ptitle").text(response.data.title + "(" + response.data.page_id + ")")
            $("#inlineForm").modal("toggle");
        }
    };

    $.ajax(settings).done(function(response) {

    });


}


$("#basicform").submit(function(event) {
    var settings = {
        "url": "/api/pages/8/",
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Authorization": "token " + $.cookie("token"),
            "X-CSRFToken": $("#csrf").val(),
        },
        "data": {
            "phone": $("#pphone").val(),
            "about": $("#pabout").val(),
            "email": $("#pmail").val(),
            "website": $("#pweb").val()
        },
        success: function(response) {
            $("#inlineForm").modal("toggle");
            swal("Page Updated!", "Details updated successfully!", "success");

        },
        error: function(response) {
            swal("Failed!", "Failed to update");
        }
    };

    $.ajax(settings).done(function(response) {
        getpages();
    });
    event.preventDefault();
});



function logout() {
    fbLogout()
    for (var it in $.cookie()) $.removeCookie(it);
    document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });
    document.location.href = "/";
}

function fbLogout() {
    FB.logout(function() {
        // document.getElementById('fbLink').setAttribute("onclick","fbLogin()");
        // document.getElementById('fbLink').innerHTML = '<img src="images/fb-login-btn.png"/>';
        // document.getElementById('userData').innerHTML = '';
        // document.getElementById('status').innerHTML = '<p>You have successfully logout from Facebook.</p>';
    });
}



$("#lform").submit(function(event) {
    var settings = {
        "url": "/api/pass-login/",
        "method": "POST",
        "timeout": 0,
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": $("#csrf").val(),
        },
        "data": {
            "username": $("#username").val(),
            "password": $("#password").val(),
        },
        error: function(response) {
            swal("Failed!", "Invalid Login Details");
        },
        success: function(response) {
            var result_data = response["data"];
            for (var it in $.cookie()) $.removeCookie(it);
            document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });
            document.cookie = "signedIn=true; path=/";
            $.each(result_data, function(key, value) {
                $.cookie(key.toString(), value.toString());
                document.cookie = key.toString() + "=" + value.toString() + "; path=/";

            })
            window.location.href = "/web/dashboard/";

        }
    };

    $.ajax(settings).done(function(response) {

    });
    event.preventDefault();
});