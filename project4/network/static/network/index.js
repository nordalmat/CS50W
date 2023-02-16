document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#all').addEventListener('click', all_posts);
    document.querySelector('#brand').addEventListener('click', all_posts);
    document.querySelector('#new').addEventListener('click', new_post);

    document.querySelector('#new-form').addEventListener('submit', submit_post);

    all_posts();
});

function getCookie(name){

    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

function all_posts() {

    document.querySelector('#new-view').style.display = 'none';
    document.querySelector('#all-view').style.display = 'block';

}

function new_post() {

    document.querySelector('#all-view').style.display = 'none';
    document.querySelector('#new-view').style.display = 'block';

    document.querySelector('#new-body').value = '';

}

function submit_post(event) {
    
    event.preventDefault();

    const body = document.querySelector('#new-body').value;

    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            body: body
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        all_posts();
    });
}

function likeDislikeButton(id, liked_posts) {

    console.log(id)
    var button = document.getElementById(`${id}`)
    if(liked_posts.indexOf(id) > -1) {
        var liked = true;
    } else {
        var liked = false;
    }

    if(liked === true) {
        fetch(`/remove_like/${id}`)
        .then(response => response.json())
        .then(result => {
            console.log(result)
            button.classList.toggle("fa-solid")
            button.classList.toggle("fa-regular")
        })
    } else {
        fetch(`/add_like/${id}`)
        .then(response => response.json())
        .then(result => {
            console.log(result)
            button.classList.toggle("fa-regular")
            button.classList.toggle("fa-solid")
        });
    }
}

function submitModal(id) {
    
    console.log(id)
    const body = document.getElementById(`textarea_${id}`).value;
    const card = document.getElementById(`body_${id}`);
    const modal = document.getElementById(`modal_edit_post_${id}`);
    fetch(`/edit/${id}`, {
        method: 'POST',
        headers: {'Content-type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')},
        body: JSON.stringify({
            body: body
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);

        // Hiddens modal after submit
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');

        const modalBackdrop = document.getElementsByClassName('modal-backdrop');
        for(let i=0; i<modalBackdrop.length; i++){
            document.body.removeChild(modalBackdrop[i]);
        }
        card.innerHTML = body;
    });
}
