// Sidebar
const menuItems = document.querySelectorAll('.menu-item'); //selects all the divs with the class menu-item

// Messages
const messagesNotification = document.querySelector('#messages-notification');
const messages = document.querySelector('.messages');
const message = messages.querySelectorAll('.message');
const messageSearch = document.querySelector('#message-search');

// Theme
const theme = document.querySelector('#theme');
const themeModal = document.querySelector('.customize-theme');
const fontSizes = document.querySelectorAll('.choose-size span');
var root = document.querySelector(':root');
const colourPalette = document.querySelectorAll('.choose-colour span');
const bg1 = document.querySelector('.bg-1');
const bg2 = document.querySelector('.bg-2');
const bg3 = document.querySelector('.bg-3');

// Posts
const openPostModalBtn = document.querySelector('#open-post-modal');
const postModal = document.querySelector('.create-post-modal');

// Coding the Messages on the Sidebar

// remove active class from all menu items
const changeActiveItem = () => {
    menuItems.forEach(item => {
        item.classList.remove('active');
    })
}

// Seleção dos itens do menu
const notificationsButton = document.querySelector('#notifications');
const notificationsPopup = document.querySelector('.notifications-popup');
const notificationCount = document.querySelector('#notifications .notification-count');

// Adiciona evento de clique para cada item do menu
menuItems.forEach(item => {
    item.addEventListener('click', (event) => {
        changeActiveItem();
        item.classList.add('active');

        if (item.id !== 'notifications') {
            notificationsPopup.style.display = 'none';
        }
    });
});

// Evento para exibir ou ocultar o pop-up de notificações
notificationsButton.addEventListener('click', (event) => {
    event.stopPropagation(); // Impede que o clique feche o pop-up imediatamente

    if (notificationsPopup.style.display === 'block') {
        notificationsPopup.style.display = 'none';
        notificationsButton.classList.remove('active');
    } else {
        notificationsPopup.style.display = 'block';
        notificationsButton.classList.add('active');
        if (notificationCount) {
            notificationCount.style.display = 'none';
        }
    }
});

// Fechar o pop-up de notificações ao clicar fora dele
document.addEventListener('click', (event) => {
    const home = document.querySelector('#home');
    lerNotificacao();
    if (!notificationsButton.contains(event.target) && !notificationsPopup.contains(event.target)) {
        notificationsPopup.style.display = 'none';
        home.classList.add('active');
        notificationsButton.classList.remove('active');
    }
});

// End of Coding the Messages on the Sidebar

// Coding the Messages section.

// searches chats
const searchMessage = () => {
    const val = messageSearch.value.toLowerCase();
    //console.log(val);
    message.forEach(chat => {
        let name = chat.querySelector('h5').textContent.toLowerCase();
        if(name.indexOf(val) != -1){
            chat.style.display = 'flex';
        } else{
            chat.style.display = 'none';
        }
    })
} 

// search chat
messageSearch.addEventListener('keyup', searchMessage);

// highlight messages card when messages menu item is clicked
messagesNotification.addEventListener('click', () => {
    messages.style.boxShadow = '0 0 1rem var(--colour-primary)'; //when messages button is clicked add box shadow over messages section
    messagesNotification.querySelector('.notification-count').style.display = 'none';
    setTimeout(() => {
        messages.style.boxShadow = 'none';
    }, 2000);
})

// End of Coding the Messages section.

// Posts

// Abrir modal de postagem
const openPostModal = () => {
    postModal.style.display = 'grid';
};

// Fechar modal ao clicar fora
const closePostModal = (e) => {
    if (e.target.classList.contains('create-post-modal')) {
        postModal.style.display = 'none';
    }
};

// Eventos
openPostModalBtn.addEventListener('click', openPostModal);
postModal.addEventListener('click', closePostModal);

// End of Coding the Posts section.

// Theme/Display Customization

// open modal
const openThemeModal = () => {
    themeModal.style.display = 'grid';
}

// close modal
const closeThemeModal = (e) => {
    if(e.target.classList.contains('customize-theme')) {
        themeModal.style.display = 'none';
    }
}

themeModal.addEventListener('click', closeThemeModal);

theme.addEventListener('click', openThemeModal);

// change font size

// removes active class from span or fonts size selectors
const removeSizeSelector = () => {
    fontSizes.forEach(size => {
        size.classList.remove('active');
    })
}


fontSizes.forEach(size => {
    size.addEventListener('click', () => {
        removeSizeSelector();
        let fontSize;
        let fonte;  // Variável para armazenar a fonte
        size.classList.toggle('active');

        if(size.classList.contains('font-size-1')) {
            fontSize = '10px';
            fonte = 'fonte-1';  // Definindo um nome para a fonte
            root.style.setProperty('----sticky-top-left', '5.4rem');
            root.style.setProperty('----sticky-top-right', '5.4rem');
        } else if (size.classList.contains('font-size-2')) {
            fontSize = '13px';
            fonte = 'fonte-2';
            root.style.setProperty('----sticky-top-left', '5.4rem');
            root.style.setProperty('----sticky-top-right', '-7rem');
        } else if (size.classList.contains('font-size-3')) {
            fontSize = '16px';
            fonte = 'fonte-3';
            root.style.setProperty('----sticky-top-left', '-2rem');
            root.style.setProperty('----sticky-top-right', '-17rem');
        } else if (size.classList.contains('font-size-4')) {
            fontSize = '19px';
            fonte = 'fonte-4';
            root.style.setProperty('----sticky-top-left', '-5rem');
            root.style.setProperty('----sticky-top-right', '-25rem');
        } else if (size.classList.contains('font-size-5')) {
            fontSize = '22px';
            fonte = 'fonte-5';
            root.style.setProperty('----sticky-top-left', '-12rem');
            root.style.setProperty('----sticky-top-right', '-35rem');
        }

        // change font size of the root html element
        document.querySelector('html').style.fontSize = fontSize;

        // Enviar a nova fonte para o backend via AJAX
        enviarFonte(fonte);
    })
})


// removes active class from span or colour selectors
const changeActiveColourClass = () => {
    colourPalette.forEach(colourPicker => {
        colourPicker.classList.remove('active');
    })
}

// change primary colours
colourPalette.forEach(colour => {

    colour.addEventListener('click', () => {
        let cor;
        changeActiveColourClass();

        if(colour.classList.contains('colour-1')){
            primaryHue = 252;
            cor = 'cor-1';
        } else if(colour.classList.contains('colour-2')) {
            primaryHue = 52;
            cor = 'cor-2';
        } else if(colour.classList.contains('colour-3')) {
            primaryHue = 352;
            cor = 'cor-3';
        } else if(colour.classList.contains('colour-4')) {
            primaryHue = 152;
            cor = 'cor-4';
        } else if(colour.classList.contains('colour-5')) {
            primaryHue = 202;
            cor = 'cor-5';
        }
        colour.classList.add('active');

        root.style.setProperty('--primary-colour-hue', primaryHue);
        enviarCor(cor);
    })
})

// changing theme backgorund values
let lightColourLightness;
let whiteColourLightness;
let darkColourLightness;

// change background colour
const changeBG = () => {
    root.style.setProperty('--light-colour-lightness', lightColourLightness);
    root.style.setProperty('--white-colour-lightness', whiteColourLightness);
    root.style.setProperty('--dark-colour-lightness', darkColourLightness);
}

// Função para enviar a cor para o backend via AJAX
const enviarCor = (cor) => {
    fetch('/alterarcor/', {  // Ajuste a URL conforme necessário
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')  // Assumindo que você tem a função getCookie para CSRF
        },
        body: `cor=${cor}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Cor alterada para: ', data.cor);
        } else {
            console.error('Erro ao alterar cor');
        }
    })
    .catch(error => {
        console.error('Erro: ', error);
    });
}

// Função para enviar a background para o backend via AJAX
const lerNotificacao = (lida) => {
    fetch('/ler_notificacoes/', {  // Ajuste a URL conforme necessário
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')  // Assumindo que você tem a função getCookie para CSRF
        },
        body: `background=${lida}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Todas as notificações foram lidas: ', data.lida);
        } else {
            console.error('Erro ao ler notificações');
        }
    })
    .catch(error => {
        console.error('Erro: ', error);
    });
}


// Função para enviar a background para o backend via AJAX
const enviarBackground = (background) => {
    fetch('/alterarbackground/', {  // Ajuste a URL conforme necessário
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')  // Assumindo que você tem a função getCookie para CSRF
        },
        body: `background=${background}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Background alterada para: ', data.background);
        } else {
            console.error('Erro ao alterar background');
        }
    })
    .catch(error => {
        console.error('Erro: ', error);
    });
}

// Função para enviar a fonte para o backend via AJAX
const enviarFonte = (fonte) => {
    fetch('/alterarfonte/', {  // Ajuste a URL conforme necessário
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')  // Assumindo que você tem a função getCookie para CSRF
        },
        body: `fonte=${fonte}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Fonte alterada para: ', data.fonte);
        } else {
            console.error('Erro ao alterar a fonte');
        }
    })
    .catch(error => {
        console.error('Erro: ', error);
    });
}

// Função para obter o CSRF token (necessária para requisições POST)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Mudança de tema

bg1.addEventListener('click', () => {
    // Troca de cor para o padrão
    lightColourLightness = '100%';
    whiteColourLightness = '100%';
    darkColourLightness = '15%';

    // Altera a cor no banco via AJAX
    enviarBackground('light');

    // Adiciona classes ativas
    bg1.classList.add('active');
    bg2.classList.remove('active');
    bg3.classList.remove('active');
    changeBG();
});

bg2.addEventListener('click', () => {
    darkColourLightness = '95%';
    whiteColourLightness = '20%';
    lightColourLightness = '15%';

    // Altera a cor no banco via AJAX
    enviarBackground('dim');

    bg2.classList.add('active');
    bg1.classList.remove('active');
    bg3.classList.remove('active');
    changeBG();
});

bg3.addEventListener('click', () => {
    darkColourLightness = '95%';
    whiteColourLightness = '10%';
    lightColourLightness = '0%';

    // Altera a cor no banco via AJAX
    enviarBackground('lights-out');

    bg3.classList.add('active');
    bg1.classList.remove('active');
    bg2.classList.remove('active');
    changeBG();
});