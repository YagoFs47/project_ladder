


function closeLayout(icon, partida_layout){
    partida_layout.style.height = "30px"
    icon.classList.replace("bi-arrows-angle-contract", "bi-arrows-angle-expand")
}

function openLayout(icon, partida_layout){  
    partida_layout.style.height = "300px"
    icon.classList.replace("bi-arrows-angle-expand", "bi-arrows-angle-contract")
}

function controlLayoutMatchup(event){
    hash_control_layout = {
        true: openLayout,
        false: closeLayout
    }

    let partidaNodeElement = event.target.closest(".partida")
    let icon = partidaNodeElement.querySelector(".title-block").querySelector("i")

    hash_control_layout[icon.classList[1] == "bi-arrows-angle-expand"](icon, partidaNodeElement)
}

function addListenerExpandLayoutMatchup(){
    // Adiciona um evento na icone da partida que faz abrir o card
    // para pode exibir os mercados daquela partida

    let icons = document.querySelectorAll(".bi-arrows-angle-expand")
    let partidas = document.querySelectorAll(".partida")
    partidas.forEach(partida => {
        partida.addEventListener("click", controlLayoutMatchup)
    });

    // icons.forEach(icon => {
    //     icon.addEventListener("click", controlLayoutMatchup)
    // });
}

addListenerExpandLayoutMatchup();