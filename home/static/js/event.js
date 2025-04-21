let websocket;
var idMatchup = document.URL.split("/")[4]


function connectWebSocket(){
    websocket = new WebSocket("ws://127.0.0.1:8000/ws/home/")

    websocket.onclose = connectWebSocket;

    websocket.onopen = console.log("ABRIU");

};


function arrowOnClick(id) {
    // identificar o conteúdo
    let element = document.querySelector(`[id="${id}"]`)

    // saber se o User está fechando ou abrindo a odd
    if (element.querySelector("div").classList.contains('market-item-content-hidden')) { //abrindo
        
        element.querySelector("div").classList.replace('market-item-content-hidden', 'market-item-content')
        element.querySelector("ul.market-ladder-hidden").classList.replace("market-ladder-hidden", "market-ladder")
        

        document.querySelector(`[data-id-market="${id}"]`)
            .classList.replace(
            "bi-caret-down-fill",
            "bi-caret-up-fill")

    }else{ //fechando
        element.querySelector("div").classList.replace("market-item-content", "market-item-content-hidden")
        element.querySelector("ul.market-ladder").classList.replace("market-ladder", "market-ladder-hidden")
        

        document.querySelector(`[data-id-market="${id}"]`)
            .classList.replace(
                "bi-caret-up-fill",
                "bi-caret-down-fill")

    }
};


function changeLadders(ladders){
    console.log(ladders)
    let liS = document.querySelectorAll("li.market-item")
    for (let x = 0; x < liS.length; x++){

        // console.log(liS[x].querySelector("ul").children)
        liS[x].querySelector("ul").innerHTML = ladders[x].innerHTML
    }
};

function refreshLadders(matchupId){

    setInterval(()=>{
        fetch(
            `http://localhost:8000/home/${idMatchup}`,
            {
                method: "get"
            }
        ).then(
            (response)=> {return response.text()}
        ).then((html)=>{
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, "text/html");
            let laddersTable = doc.querySelectorAll("ul.market-ladder-hidden");
            changeLadders(laddersTable);

        })
    }, 15000);
}

function filterEventClickLadder(eventClick){
    let itemClicked = eventClick.target;
    if (!itemClicked.classList.contains("ladder-item-odd")){
        

        if(itemClicked.classList.contains("ladder-item-back")){
            itemClicked.textContent = "Clicado!";
            websocket.send(JSON.stringify(
                {
                    message: {
                        action: "set_money",
                        side: "back",
                        market_odd: itemClicked.getAttribute("data-market-value"),
                        market_id: itemClicked.getAttribute("data-market-id"),
                        id_matchup: idMatchup
                    }
                }
            ))

        }else if(itemClicked.classList.contains("ladder-item-lay")){
            itemClicked.textContent = "Clicado!";
            websocket.send(JSON.stringify(
                {
                    message: {
                        action: "set_money",
                        side: "lay",
                        market: itemClicked.getAttribute("data-market-value"),
                        market_id: itemClicked.getAttribute("data-market-id"),
                        id_matchup: idMatchup
                    }
                }
            ))

        }
        
    }
    // if (eventClick.target.classList.contains(""))
};

// Adicionar um evento de click em item da ladder
// para saber se o click foi num back ou lay
// e para saber onde plantar o dinheiro
function set_listener_item_ladders(){
    document.querySelectorAll(".ladder-item").forEach((item)=>{
        item.addEventListener("click", filterEventClickLadder)
    });
};


connectWebSocket();
set_listener_item_ladders();
refreshLadders();