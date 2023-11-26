function update_post_follower_following_navbar(what_to_load){
    var followers_btn = document.getElementById('followers_btn');
    var following_btn = document.getElementById('following_btn');
    if (what_to_load == "followers") {
        followers_btn.classList.add("active", "fol-fol");
        following_btn.classList.remove("active", "fol-fol");
    } else if (what_to_load == "following") {
        following_btn.classList.add("active", "fol-fol");
        followers_btn.classList.remove("active", "fol-fol");
    }
}

function load_follow_ers_ing(what_to_load) {
    // make corresponding active in card navbar
    update_post_follower_following_navbar(what_to_load);

    data = {
        user: false,
        what_to_load: what_to_load,
    }

    requestDataMetadata = {
        method: "POST",
        headers: { "content-type": "application/json", "X-CSRFToken": csrfToken },
        body: JSON.stringify(data)
    }

    const url_var = document.location.origin;
    console.log(url_var);

    fetch(`${url_var}/load_follow/`, requestDataMetadata)
        .then(response => response.json())
        .then(data => {
            console.log(data.success, true);
            if (data.success) {
                s = '';
                data.users_data.forEach(user => {
                    s += `
                    <div class="card post-shadow mb-2" style="border: 2px solid black;">
                        <div class="row d-flex justify-content-between">
                            <div class="col-3 container-fluid">`

                    if (user.profile_photo_url) {
                        s += `
                                <img src="${user.profile_photo_url}" alt="Generic placeholder image"
                                    class="img-fluid img-thumbnail my-1 ms-1" id="profile_pic"
                                    style="width: 70px; height: 70px;">`
                    } else {
                        s += `
                                <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-profiles/avatar-1.webp"
                                    alt="Generic placeholder image" class="img-fluid img-thumbnail my-1 ms-1"
                                    id="profile_pic" style="width: 70px; height: 70px;">`
                    }
                    s += `
                            </div>
                            <div class="col-5 text-center mt-4">
                                <p class="d-inline-block text-truncate row" style="max-width: 120px;">
                                    ${user.name}
                                </p>
                            </div>
                            <div class="col-2 card-body mt-2">
                                <button class="btn btn-outline-dark btn-sm" onclick="FollowUser('${user.name}')"
                                id="${user.name}_follow_btn">${user.my_follow_status}</button>
                            </div>
                        </div>
                    </div>`
                });
                document.getElementById('follow_viewer').innerHTML = s;
            } else {
                alert("Follow action failed!");
                document.getElementById('follow_viewer').innerHTML = "Try Again!";
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('follow_viewer').innerHTML = "Error!";
        });
}