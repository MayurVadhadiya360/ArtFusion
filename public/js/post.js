function view_whole_post(post_pk){

}

function like_post(post_pk) {
    let post_like = document.getElementById(`${post_pk}_post_like`);
    let post_like_count = document.getElementById(`${post_pk}_post_like_count`);

    let like = false;

    if(post_like.classList.contains("bi-heart")){
        like = true;
    }

    let data = {
        post_pk: post_pk,
        like: like,
    }

    let requestDataMetadata = {
        method: "POST",
        headers: { "content-type": "application/json", "X-CSRFToken": csrfToken },
        body: JSON.stringify(data)
    }

    fetch(like_post_url, requestDataMetadata)
        .then(response => response.json())
        .then(data => {
            console.log("data.success", data.success);
            if (data.success) {
                if(like){
                    post_like.classList.remove('bi-heart');
                    post_like.classList.add('bi-heart-fill');
                    post_like_count.innerText = Number(post_like_count.innerText)+1;
                }else{
                    post_like.classList.remove('bi-heart-fill');
                    post_like.classList.add('bi-heart');
                    post_like_count.innerText = Number(post_like_count.innerText)-1;
                }
            } else {
                if(data.not_logged_in){
                    alert("Please Login first!")
                }else{
                    alert("Like action failed!");
                }
            }
        })
        .catch(error => {
            alert("Error!");
            console.error('Error:', error);
        });
}