function update_post_follower_following_navbar(what_to_load){
    var followers_btn = document.getElementById('followers_btn');
    var following_btn = document.getElementById('following_btn');
    var posts_btn = document.getElementById('posts_btn');
    if(what_to_load == "followers"){
        followers_btn.classList.add("active", "fol-fol");
        following_btn.classList.remove("active", "fol-fol");
        posts_btn.classList.remove("active", "fol-fol");
    }else if(what_to_load == "following"){
        followers_btn.classList.remove("active", "fol-fol");
        following_btn.classList.add("active", "fol-fol");
        posts_btn.classList.remove("active", "fol-fol");
    }else if(what_to_load == "posts"){
        followers_btn.classList.remove("active", "fol-fol");
        following_btn.classList.remove("active", "fol-fol");
        posts_btn.classList.add("active", "fol-fol");
    }
}

function load_follow_ers_ing(user, what_to_load){
    // make corresponding active in card navbar
    update_post_follower_following_navbar(what_to_load);
    let data = {
        user: user,
        what_to_load: what_to_load,
    }

    let requestDataMetadata = {
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
                let s = '';
                data.users_data.forEach(user => {
                    s += `
                    <div class="card post-shadow mb-2" style="border: 2px solid black;">
                        <div class="row d-flex justify-content-around">
                            <div class="col-3 container-fluid">`

                                if (user.profile_photo_url){
                                s += `
                                <img src="${ user.profile_photo_url }" alt="Generic placeholder image"
                                    class="img-fluid img-thumbnail my-1 ms-1" id="profile_pic"
                                    style="width: 70px; height: 70px;">`
                                }else{
                                s += `
                                <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-profiles/avatar-1.webp"
                                    alt="Generic placeholder image" class="img-fluid img-thumbnail my-1 ms-1"
                                    id="profile_pic" style="width: 70px; height: 70px;">`
                                }
                                s += `
                            </div>
                            <div class="col-7 text-start mt-4">
                                <p class="d-inline-block text-truncate row" style="max-width: 120px;">
                                    ${ user.name }
                                </p>
                            </div>
                            <div class="col-1 card-body mt-2">
                                <button class="btn btn-outline-dark btn-sm" onclick="FollowUser('${user.name}')"
                                id="${ user.name }_follow_btn">${ user.my_follow_status }</button>
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

function load_post(user){
    // var followers_btn = document.getElementById('followers_btn');
    // var following_btn = document.getElementById('following_btn');
    // var posts_btn = document.getElementById('posts_btn');
    // posts_btn.classList.add("active", "fol-fol");
    // followers_btn.classList.remove("active", "fol-fol");
    // following_btn.classList.remove("active", "fol-fol");
    update_post_follower_following_navbar(what_to_load="posts");

    let data = {
        user: user
    }
    
    let requestDataMetadata = {
        method: "POST",
        headers: { "content-type": "application/json", "X-CSRFToken": csrfToken },
        body: JSON.stringify(data)
    }
    const url_var = document.location.origin;
    console.log(url_var);

    fetch(`${url_var}/load_posts/`, requestDataMetadata)
        .then(response => response.json())
        .then(data => {
            console.log(data.success, true);
            if (data.success) {
                let s = '';
                data.posts.forEach(postData => {
                    s += `
                    <div class="container my-2" data-bs-theme="dark" style="width: 530px;">
                        <div class="card post-shadow">`;
                            if(postData.post_image)
                            s += `
                            <img src="${ postData.post_image }" class="card-img p-1" alt="image">`
                            s += `
                            <div class="card-body">
                                <h5 class="card-title">${ postData.post_title}</h5>
                                <p class="card-text">${ postData.post_content }</p>
                            </div>
                            <hr>
                            <div class="card-body row">
                                <div class="col-4 d-flex justify-content-center">
                                    <i class="bi bi-send"></i>
                                </div>
                                <div class="col-4 d-flex justify-content-center">
                                    <i class="bi bi-chat"></i>
                                    <i class="bi bi-chat fol"><a href="/post/${postData.pk}"></a></i>
                                </div>
                                <div class="col-4 d-flex justify-content-center">`
                                    if(postData.is_liked){
                                        s += `
                                        <i class="bi bi-heart-fill fol" style="color: red;" onclick="like_post('${ postData.pk }')"
                                            id="${ postData.pk }_post_like"></i>
                                        <span id="${ postData.pk }_post_like_count">${ postData.likes }</span>`
                                    }else{
                                        s += `
                                        <i class="bi bi-heart fol" style="color: red;" onclick="like_post('${ postData.pk }')"
                                            id="${ postData.pk }_post_like"></i>
                                        <span id="${ postData.pk }_post_like_count">${ postData.likes }</span>`
                                    }
                                    s += `
                                </div>
                            </div>
                        </div>
                    </div>`
                })
                document.getElementById("show_content").innerHTML = s;
            } else {
                document.getElementById("show_content").innerHTML = "Try Again!";
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById("show_content").innerHTML = "Error!";
        });
}