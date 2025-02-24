document.addEventListener("DOMContentLoaded", function () {
    // Abrir o modal e definir o post_id
    document.querySelectorAll(".open-comentario-modal").forEach(button => {
        button.addEventListener("click", function () {
            let postId = this.getAttribute("data-post-id");
            document.getElementById("post-id").value = postId; // Define o ID do post no campo oculto
            document.querySelector(".create-comentario-modal").style.display = "block";
        });
    });

    // Fechar o modal ao clicar fora dele (opcional)
    document.querySelector(".create-comentario-modal").addEventListener("click", function (e) {
        if (e.target === this) {
            this.style.display = "none";
        }
    });

    // Enviar o comentário via AJAX
    document.getElementById("comentario-form").addEventListener("submit", function (e) {
        e.preventDefault();

        let postId = document.getElementById("post-id").value;
        let texto = document.getElementById("texto").value;
        let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        if (texto.trim() === "") {
            alert("O comentário não pode estar vazio.");
            return;
        }

        fetch(`/post/${postId}/comentar/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrfToken
            },
            body: `texto=${encodeURIComponent(texto)}`
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    document.getElementById("texto").value = ""; // Limpa o campo de texto
                    document.querySelector(".create-comentario-modal").style.display = "none"; // Fecha o modal
                } else {
                    alert(data.mensagem);
                }
            })
            .catch(error => console.error("Erro ao enviar o comentário:", error));
    });
});


// End of Coding the Comentários section.

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

                // // Atualizar contador de curtidas se existir
                // const likeCount = button.querySelector('.like-count');
                // if (likeCount) {
                //     likeCount.textContent = data.likes;
                // }
            } else {
                console.error('Erro ao curtir a postagem');
            }
        })
        .catch(error => {
            console.error('Erro: ', error);
        });
};

// Função para curtir/descurtir uma postagem
const toggleBookmark = (postId, button) => {
    fetch(`/marcar/${postId}/`, {
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
                if (data.marcado) {
                    heartIcon.classList.remove('uil-bookmark-full');
                    heartIcon.classList.add('bxs-bookmark-star');
                    heartIcon.style.color = '';
                } else {
                    heartIcon.classList.remove('bxs-bookmark-star');
                    heartIcon.classList.add('uil-bookmark-full');
                    heartIcon.style.color = '';
                }

            } else {
                console.error('Erro ao marcar a postagem');
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

// Adicionar evento de clique aos botões de marcar
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.bookmark-button').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const postId = button.dataset.postId;
            toggleBookmark(postId, button);
        });
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // Seleciona todos os botões de abrir comentários
    document.querySelectorAll(".open-comentario-modal").forEach(button => {
        button.addEventListener("click", function () {
            let postId = this.getAttribute("data-post-id"); // Obtém o ID do post clicado
            document.getElementById("post-id").value = postId; // Define o ID do post no campo oculto

            // Faz a requisição AJAX para buscar os comentários do post
            fetch(`/comentarios/${postId}/`)
                .then(response => response.json())
                .then(data => {
                    let comentariosDiv = document.querySelector(".comentarios");
                    comentariosDiv.innerHTML = ""; // Limpa os comentários antigos

                    if (data.comentarios.length > 0) {
                        data.comentarios.forEach(comentario => {
                            let commentHTML = `
                                <div class="comentario">
                                    <div class="profile-photo" style="margin-bottom: .5rem;">
                                        <img src="${comentario.imagem_perfil}" alt="Usuário">
                                    </div>
                                    <strong>${comentario.perfil}</strong> <small style="font-size: 0.6rem;"> ${comentario.data}</small> <br>
                                    ${comentario.texto}
                                </div>
                            `;
                            comentariosDiv.innerHTML += commentHTML;
                        });
                    } else {
                        comentariosDiv.innerHTML = "<p>Sem comentários ainda.</p>";
                    }
                })
                .catch(error => console.error("Erro ao buscar comentários:", error));

            // Abre o modal (caso tenha uma função para isso)
            document.querySelector(".create-comentario-modal").style.display = "block";
            document.querySelector(".create-comentario-modal").style.alignContent = "center"; // Para centralizar o conteúdo em múltiplas linhas, se houver
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Abrir o modal de visualizar comentários
    document.querySelectorAll(".open-view-comentario-modal").forEach(button => {
        button.addEventListener("click", function () {
            let postId = this.getAttribute("data-post-id");
            document.getElementById("post-id").value = postId; // Define o ID do post no campo oculto

            // Buscar os comentários via AJAX (opcional, se não forem carregados diretamente no template)
            fetch(`/comentarios/${postId}/`)
                .then(response => response.json())
                .then(data => {
                    let comentariosContainer = document.querySelector(".view-comentario-modal .comentarios");
                    comentariosContainer.innerHTML = ""; // Limpa os comentários anteriores

                    if (data.comentarios.length > 0) {
                        data.comentarios.forEach(comentario => {
                            let commentElement = document.createElement("div");
                            commentElement.classList.add("comentario"); // Adiciona a classe "comentario"

                            // Criar a div da foto do perfil com o style adicional
                            let profilePhoto = document.createElement("div");
                            profilePhoto.classList.add("profile-photo");
                            profilePhoto.style.marginBottom = ".5rem";  // Adiciona o margin-bottom

                            // Se houver uma URL da foto no objeto "comentario", adicione-a
                            if (comentario.imagem_perfil) {
                                profilePhoto.innerHTML = `<img src="${comentario.imagem_perfil}" alt="Foto de ${comentario.perfil}">`;
                            } else {
                                profilePhoto.innerHTML = `<img src="/assets/images/img/user.png" alt="Foto padrão">`;
                            }

                            // Adicionar a foto do perfil e o texto do comentário diretamente à div "comentario"
                            commentElement.appendChild(profilePhoto);
                            commentElement.innerHTML += `<strong>${comentario.perfil}</strong> <small style="font-size: 0.6rem;"> ${comentario.data}</small><br>`;
                            commentElement.innerHTML += `${comentario.texto}`;

                            comentariosContainer.appendChild(commentElement);
                        });
                    } else {
                        comentariosContainer.innerHTML = "<p>Sem comentários.</p>";
                    }

                    document.querySelector(".view-comentario-modal").style.display = "block";
                    document.querySelector(".view-comentario-modal").style.alignContent = "center"; // Para centralizar o conteúdo em múltiplas linhas, se houver
                });
        });
    });

    // Fechar o modal ao clicar fora dele
    document.querySelector(".view-comentario-modal").addEventListener("click", function (e) {
        if (e.target === this) {
            this.style.display = "none";
        }
    });
});
