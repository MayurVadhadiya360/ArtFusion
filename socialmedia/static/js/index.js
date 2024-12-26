function followUser(element, username) {
    const action = element.dataset.action;
    let data = {
        "username": username,
        "action": action,
    };

    requestDataMetadata = {
        method: "POST",
        headers: { "content-type": "application/json", "X-CSRFToken": csrfToken },
        body: JSON.stringify(data)
    };

    fetch(follow_user_url, requestDataMetadata)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (action === "follow") {
                    element.textContent = 'Following';
                    element.dataset.action = 'unfollow';
                } else if (action === "unfollow") {
                    element.textContent = 'Follow';
                    element.dataset.action = 'follow';
                }
            }
            else {
                if (typeof showMessage === 'function') {
                    if (data.msg) showMessage(data.msg);
                }
            }
        })
        .catch(error => {
            console.error('Error(followUser):', error);
        });
}

function like_post(post_pk) {
    let post_like_icon = document.getElementById(`${post_pk}_post_like`);
    let post_like_count_element = document.getElementById(`${post_pk}_post_like_count`);

    let action_like = post_like_icon.classList.contains('bi-heart');

    let data = {
        post_pk: post_pk,
        action: action_like ? "like" : "unlike",
    };

    let requestDataMetadata = {
        method: "POST",
        headers: { "content-type": "application/json", "X-CSRFToken": csrfToken },
        body: JSON.stringify(data)
    };

    fetch(like_post_url, requestDataMetadata)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (action_like) {
                    post_like_icon.classList.remove('bi-heart');
                    post_like_icon.classList.add('bi-heart-fill');

                    let newlikeCount = parseInt(post_like_count_element.dataset.likecount) + 1;
                    post_like_count_element.dataset.likecount = newlikeCount.toString();
                    post_like_count_element.textContent = (newlikeCount > 0) ? newlikeCount.toString() : "";
                }
                else {
                    post_like_icon.classList.remove('bi-heart-fill');
                    post_like_icon.classList.add('bi-heart');

                    let newlikeCount = parseInt(post_like_count_element.dataset.likecount) - 1;
                    post_like_count_element.dataset.likecount = newlikeCount.toString();
                    post_like_count_element.textContent = (newlikeCount > 0) ? newlikeCount.toString() : "";
                }
            }
            else {
                if (typeof showMessage === 'function') {
                    if (data.msg) showMessage(data.msg);
                }
            }

        })
        .catch(error => {
            console.error('Error(like_post):', error);
        });
}


