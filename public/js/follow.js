function FollowUser(user) {
    action_decider = document.getElementById(user + '_follow_btn').innerText;
    console.log(user, action_decider);
    data = {
        some_user: user,
        action_decider: action_decider,
    }

    requestDataMetadata = {
        method: "POST",
        headers: { "content-type": "application/json", "X-CSRFToken": csrfToken },
        body: JSON.stringify(data)
    }
    const url_var = document.location.origin;
    console.log(url_var);

    fetch(`${url_var}/follow_request/`, requestDataMetadata)
        .then(response => response.json())
        .then(data => {
            console.log(data.success, true);
            if (data.success) {
                document.getElementById(user + '_follow_btn').innerText = data.follow_status_text;
                document.getElementById('following_warning').innerHTML = '<i class="bi bi-exclamation-circle text-danger-emphasis "></i>'
            } else {
                alert("Follow action failed!");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

