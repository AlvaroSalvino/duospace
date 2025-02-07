// Dropdawm Do post
function toggleDropdown(postId) {
    const dropdown = document.getElementById('dropdown-' + postId);
    dropdown.classList.toggle('show');
}

// Função para curtir/descurtir uma postagem
const toggleLike = (postId, button) => {
    fetch(`/curtir/${postId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `post_id=${postId}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            const heartIcon = button.querySelector('i');

            // Atualizar o ícone de coração
            if (data.liked) {
                heartIcon.classList.remove('uil-heart');
                heartIcon.classList.add('bxs-heart');
                heartIcon.style.color = '#ff0101';
            } else {
                heartIcon.classList.remove('bxs-heart');
                heartIcon.classList.add('uil-heart');
                heartIcon.style.color = '';
            }

            // Atualizar contador de curtidas se existir
            const likeCount = button.querySelector('.like-count');
            if (likeCount) {
                likeCount.textContent = data.likes;
            }
        } else {
            console.error('Erro ao curtir a postagem');
        }
    })
    .catch(error => {
        console.error('Erro: ', error);
    });
};

// Função para obter o CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Adicionar evento de clique aos botões de curtir
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const postId = button.dataset.postId;
            toggleLike(postId, button);
        });
    });
});
