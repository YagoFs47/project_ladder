var websocket;


function showSpinnerMatchup(orientation, idItem){

    if (orientation){
        let loader = document.createElement("span")
        loader.classList.add("loader")
        let element = document.querySelector(`li[id="${idItem}"] > span `)
        element.insertBefore(loader, element.firstChild)
    }
    
    else{
        let element = document.querySelector(`li[id="${idItem}"] > span > .loader`).remove()
    }   
        

}

function startConnectionWs(){
    websocket = new WebSocket("ws://127.0.0.1:8000/ws/home/")
    websocket.onclose = startConnectionWs;
    websocket.onopen = function(){
        console.log('abriu mano')
    }
}

function openMatchup(matchupId){
    fetch(
        `http://127.0.0.1:8000/api/markets?event_id=${matchupId}`,
        {
            headers:{
                "Content-Type": "application/json",
            }
        }
        ).then(
            (response)=>response.json()
        )
        .then(
            (data)=>{
                websocket.send(JSON.stringify({
                    message: {
                        'action': 'openMatchup', 
                        'marketId': data.id, 
                        'eventId': matchupId
                    }
                }));
            }
        )
}

function openMarketLayout(marketId, icon){
    const li = document.querySelector(`li[id='${marketId}']`);
    const marketDetail = li.querySelector("div.market-detail.hidden");
    const marketDetailActived = li.querySelector("div.market-detail.active");
    const marketLadder = li.querySelector("ul.market-ladder.hidden");
    const marketLadderActivacted = li.querySelector("ul.market-ladder.active");

    if(Boolean(marketDetail)){
        li.classList.add("active")
        marketDetail.classList.replace("hidden", "active")
        icon.classList.replace("bi-caret-down", "bi-caret-up")
        marketLadder.classList.replace("hidden", "active")
    }else{
        li.classList.remove("active")
        marketDetailActived.classList.replace("active", "hidden")
        marketLadderActivacted.classList.replace("active", "hidden")
        icon.classList.replace("bi-caret-up", "bi-caret-down")
    }
}

async function openMatchupLayout(matchupId, icon){


    const li = document.querySelector(`li[id='${matchupId}']`);
    const matchupDetail = li.querySelector("div.matchup-detail.hidden");
    const matchupDetailActived = li.querySelector("div.matchup-detail.active");
    console.log(li.getAttribute("data-matchup-id"))
    if(Boolean(matchupDetail)){
        showSpinnerMatchup(true, matchupId)
        getAllMarkets(li.getAttribute("data-matchup-id"), matchupDetail);
        li.classList.add("active")
        matchupDetail.classList.replace("hidden", "active")
        icon.classList.replace("bi-caret-down-fill", "bi-caret-up-fill")
    }else{
        
        li.classList.remove("active")
        matchupDetailActived.classList.replace("active", "hidden")
        icon.classList.replace("bi-caret-up-fill", "bi-caret-down-fill")
    }
}

function setMarketExtesion(marketId, eventId){
    websocket.send(JSON.stringify({
        message: {
            "action": "setMarket",
            "marketId": marketId,
            "eventId": eventId,
        }
    }));
}

function showSuggestionsBet(data, ladderUl){
    // Após clicar na ladder, será exibindo uma linha de green e red
    // referente a tal aposta
    let ladderItemsEmpty = ladderUl.parentElement.querySelectorAll("li.ladder-item.ladder-item-empty")
    console.log(data)
    let marketId;
    let eventId;
    let marketValue;
    let runnerId;
    let lucroBruto;
    let oddSelected;
    let stakeBack = 100;
    let oddEntradaLay = 100

    if (data.side == "back"){
        

        // ladderItemsEmpty.forEach(
        //     (itemElement)=>{
        //         marketId = itemElement.dataset.marketId;
        //         eventId = itemElement.dataset.eventId;
        //         runnerId = itemElement.dataset.runnerId;
        //         marketValue = itemElement.dataset.marketValue;
        //         oddLay = parseFloat(itemElement.dataset.oddValue.replace(",", "."));
        //         oddBack = parseFloat(data.oddValue.replace(",", "."))
        //         lucroBruto = stakeBack * (oddBack - 1)
        //         stakeLay = (lucroBruto + stakeBack) / oddLay
        //         console.log(lucroBruto, stakeBack, oddLay)
        //         itemElement.textContent = (stakeLay - stakeBack).toFixed(2);

        //     }
        // )
    }else{
        // PEGA O ELEMENTO PAI, E DEPOIS SELECIONA UMA LISTA DE FILHOS
        // let ladderItemsEmpty = ladderUl.parentElement.querySelectorAll("li.ladder-item.ladder-item-empty")
        // let ladderItemsOdds = ladderUl.parentElement.querySelectorAll("li.ladder-item.ladder-item-odd")
        // ladderItemsEmpty.forEach(
        //     (itemElement)=>{
        //         oddSelected = parseFloat(itemElement.dataset.oddValue.replace(",", "."));
        //         lucroBruto = oddEntradaLay / (oddSelected - 1)
        //         console.log(itemElement.textContent)
        //         // lucroBruto * (1 - oddSelected/)
        //     }
        // )

        // for(var c = 0; c < ladderItemsEmpty.length; c++){
        //     let possibleOddExit 
        // }

        
    }

    
}

function getCalcOfServer(data, event){
    console.log(data, event)
}


function sendEventClickLadder(event){
    let marketId;
    let eventId;
    let marketValue;
    let oddValue;
    let side;
    let runnerId;

    
    marketId = event.dataset.marketId;
    eventId = event.dataset.eventId;
    runnerId = event.dataset.runnerId;
    marketValue = event.dataset.marketValue;
    oddValue = event.dataset.oddValue;
    side = event.dataset.side;

    fetch(
        "http://127.0.0.1:8000/api/markets/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(
                {   
                    "event_id": eventId,
                    "market_id": marketId,
                    "runner_id": runnerId,
                    "odd": parseFloat(oddValue.replace(",", ".")),
                    "stake": 1.00,
                    'side': side
                }
            )
        }
    )

    event.textContent = "100";
    // getCalcOfServer(event.dataset, event)
    showSuggestionsBet(event.dataset, event)

    
    // fetch(
    //     "http://127.0.0.1:8000/api/bets/",
    //     {
    //         headers:{
    //             "Content-Type": "application/json"
    //         },
    //         method: "POST",
    //         body: JSON.stringify(
    //             {
    //                 "marketId": marketId,
    //                 "marketValue": marketValue,
    //                 "eventId": eventId,
    //                 "oddValue": oddValue,
    //                 "side": side,
    //                 "runnerId": runnerId,
    //                 "action": "setMoney",
    //                 }
    //             )
    //         }
    //     ).then(
    //         (response)=>{
    //             console.log(response)
    //         }
    //     )

    // websocket.send(JSON.stringify({
    //     message: {
    //         "marketId": marketId,
    //         "marketValue": marketValue,
    //         "eventId": eventId,
    //         "oddValue": oddValue,
    //         "side": side,
    //         "runnerId": runnerId,
    //         "action": "setMoney",
    //     }
    // }));
};

function setNewOddLadder(marketElement, marketData){
    let ladder = marketElement.querySelector("ul.market-ladder")
    let ladderItemsBack = ladder.querySelectorAll("li.ladder-item-back")
    let ladderItemsLay = ladder.querySelectorAll("li.ladder-item-lay")
    // { odd: 1.83, back: "", lay: "", available_amount: "" }
    for (let index=0; index < marketData.ladder.length; index++){
     
        ladderItemsBack[index].textContent = marketData.ladder[index].lay
        ladderItemsLay[index].textContent = marketData.ladder[index].back
        
    }

}

async function refreshAllData(){
    console.log("refreshing...")
    
    // para cada jogo aberto

    document.querySelectorAll("li.matchup-item.active").forEach(
        async (partida)=>{
            let partidaId = partida.dataset.matchupId;
            let matchupMarkets = partida.querySelector('ul.matchup-markets')
            let mercados = matchupMarkets.querySelectorAll("li.market-item")
            let mercados_ids = "";
            // pega os ids dos mercados
            mercados.forEach(
                (mercado)=>{
                    // seleciona a ladder de cada mercado
                    mercados_ids += mercado.dataset.marketId + ",";
                    // pega todas os items de dentro da ladder
                }
            )

            response = await fetch(`http://127.0.0.1:8000/api/markets/prices?event_id=${partidaId}&market_ids=${mercados_ids}`)
            data_json = await response.json();
            
            for(let c = 0; c < mercados.length; c++){
                setNewOddLadder(mercados[c], data_json.event_info.markets[c])
            }
        }
    )

};

async function getAllMarkets(matchupId, matchupDetail){
    fetch(
        `http://127.0.0.1:8000/api/markets?event_id=${matchupId}`,
        {
            mode: "cors",
            headers: {
                "content-type": "text/html"
            }
        }
    ).then(
        (response)=>response.text()
    ).then(
        (textHTML)=>{
            showSpinnerMatchup(false, matchupId)
            const parser = new DOMParser();
            const doc = parser.parseFromString(textHTML, "text/html")
            matchupDetail.innerHTML = doc.body.innerHTML;

        }
    )
};

startConnectionWs();

// document.querySelectorAll("i.show-detail-matchup").forEach(
//     (icon)=>{
//         icon.addEventListener("click", (eventIconClick)=>{
            
//         })
//     }
// );

setInterval(refreshAllData, 5000)



