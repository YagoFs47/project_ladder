

function createConnection(){
    const socket = new WebSocket(
        `/ws?typeChannel=matchups`,
    );

    socket.addEventListener("message", (event)=>{
        console.log(event.data)
    })

}

function closeLayout(icon, partida_layout){
    partida_layout.classList.remove("open")
    icon.classList.replace("bi-arrows-angle-contract", "bi-arrows-angle-expand")
    partida_layout.querySelector(".markets-list").remove();
}

function addListenerOnMarketClick(listMarkets){
    // Adiciona um evento de click ao clickar no mercado para
    // abrir um nova página e gerar um ladder 

    listMarkets.querySelectorAll("li").forEach((li)=>{
        li.addEventListener("click", (event)=>{
            window.open(`/ladders/${event.target.dataset.eventId}/${event.target.dataset.marketId}`,)
            console.log(event.target.dataset)
        })
    })
}

async function openLayout(icon, partida_layout){  
    partida_layout.classList.add("open")
    icon.classList.replace("bi-arrows-angle-expand", "bi-arrows-angle-contract")
    let eventId = partida_layout.dataset.eventId
    // Buscar os mercados daquele jogo
    fetch(
        `/api/markets/${eventId}`,
        {
            method: "GET",
            headers: {
                Accept: "text/html",
                "Content-Type": "application/json",
            },
        }

    ).then((response)=>response.text()).then(
        (html)=>{
            // partida_layout.innerHTML += html
            const parser = new DOMParser()
            const doc = parser.parseFromString(html, "text/html")
            const listMarkets = doc.body.querySelector("ul")
            // const marketsList = partida_layout.querySelector(".markets-list")
            // if (marketsList){
            //     partida_layout.replaceChild(marketsList, newMarketsList)
            //     return;
            // }

            addListenerOnMarketClick(listMarkets)
            partida_layout.insertAdjacentElement("beforeend", listMarkets)

        }
    )


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
    let partidas = document.querySelectorAll(".title-block")
    partidas.forEach(partida => {
        partida.addEventListener("click", controlLayoutMatchup)
    });

    // icons.forEach(icon => {
    //     icon.addEventListener("click", controlLayoutMatchup)
    // });
}

addListenerExpandLayoutMatchup();
createConnection();