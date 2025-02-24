document.addEventListener("DOMContentLoaded", function () {
    let pagina = 2; // Começamos a partir da segunda página, pois a primeira já foi carregada.
    let carregando = false; // Flag para evitar múltiplas requisições simultâneas.
    
    function carregarMaisPosts() {
        if (carregando) return; // Evita múltiplos carregamentos simultâneos.
        
        const scrollPos = window.innerHeight + window.scrollY;
        const pageHeight = document.documentElement.scrollHeight;

        if (scrollPos >= pageHeight - 100) { // Quando o usuário chega perto do final da página.
            carregando = true;
            
            fetch(`/carregar-posts?pagina=${pagina}`)
                .then(response => response.json())
                .then(data => {
                    if (data.posts.length > 0) {
                        adicionarPostsAoFeed(data.posts);
                        pagina++; // Avança para a próxima página.
                    } else {
                        window.removeEventListener("scroll", carregarMaisPosts); // Para de ouvir o evento se não houver mais posts.
                    }
                    carregando = false;
                })
                .catch(error => {
                    console.error("Erro ao carregar posts:", error);
                    carregando = false;
                });
        }
    }

    function adicionarPostsAoFeed(posts) {
        const feedContainer = document.querySelector(".feeds");
        
        posts.forEach(post => {
            const postElement = document.createElement("div");
            postElement.classList.add("feed");
            postElement.innerHTML = `
                <div class="head">
                    <div class="user">
                        <div class="profile-photo">
                            <img src="${post.perfil.imagem_perfil ? post.perfil.imagem_perfil : '/static/assets/images/img/user.png'}" alt="Usuário">
                        </div>
                        <div class="info">
                            <h3>${post.titulo}</h3>
                            <small>${post.data_postagem} - <span class="capitalise">${post.tempo_decorrido} atrás</span></small>
                        </div>
                    </div>
                </div>
                <div class="photo">
                    ${post.imagem ? `<img src="${post.imagem}" alt="Post imagem">` : ""}
                </div>
                <div class="action-buttons">
                    <div class="interaction-buttons">
                        <span class="like-button" data-post-id="${post.id}" style="cursor: pointer;">
                            ${post.curtido ? "<i class='bx bxs-heart' style='color:#ff0101'></i>" : "<i class='uil uil-heart'></i>"}
                        </span>
                        <span class="open-comentario-modal" data-post-id="${post.id}" style="cursor: pointer;">
                            <i class="uil uil-comment-dots"></i>
                        </span>
                        <span><i class="uil uil-share-alt"></i></span>
                    </div>
                    <div class="bookmark">
                        <span class="bookmark-button" data-post-id="${post.id}" style="cursor: pointer;">
                            ${post.marcado ? "<i class='bx bxs-bookmark-star'></i>" : "<i class='uil uil-bookmark-full'></i>"}
                        </span>
                    </div>
                </div>
                <div class="caption">
                    <p><b>${post.perfil.nome}</b> ${post.texto}</p>
                </div>
                ${post.comentarios_count > 0 ? `<div class="comments text-muted open-view-comentario-modal" data-post-id="${post.id}">
                    Ver ${post.comentarios_count} ${post.comentarios_count === 1 ? "comentário" : "comentários"}
                </div>` : ""}
            `;

            feedContainer.appendChild(postElement);
        });
    }

    window.addEventListener("scroll", carregarMaisPosts);
});
