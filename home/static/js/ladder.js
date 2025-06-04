let eventId;
let marketId;
let runnerId;


eventId = document.URL.split("/")[4];
marketId = document.URL.split("/")[5];
const HASH_OPOSITION = {
    "back": "lay",
    "lay": "back"
}

function addListenerDefaultStakes(){
    let defaultSelected = 0
    document.querySelectorAll("li.stake-default-item").forEach(li=>{
        li.addEventListener("click", event=>{
            document.querySelectorAll("li.stake-default-item").forEach(li2=>{
                li2.classList.remove('selected')
            })
            
            let = stakeSelected = parseFloat(event.target.textContent.trim().replace(",", "."))

            if(defaultSelected != stakeSelected){
                li.classList.add("selected")
            }

        })
    })
}

function createConnection(){
    const socket = new WebSocket(
        `/ws?eventId=${eventId}&marketId=${marketId}&typeChannel=ladder`,
    );

    socket.addEventListener("message", (event)=>{
        cont = 0 
        ladderData = JSON.parse(event.data)
        let suggestions = document.querySelectorAll(`li.ladder-item-suggestion`)
        let bets = document.querySelectorAll(`li.ladder-item-money`)
        let backs = document.querySelectorAll(`li.ladder-item-back`)
        let odds = document.querySelectorAll(`li.ladder-item-odd`)
        document.querySelectorAll(`li.ladder-item-lay`).forEach((lay)=>{
            // li.textContent = '0';
            // backs[cont].textContent = '0';
            let currentOdd = ladderData.prices[cont]
            setOddPricePlayer(currentOdd, backs[cont], lay)
            setSuggetion(currentOdd, suggestions[cont])
            setBet(ladderData.prices[cont].stake, bets[cont])
            setStateOdd(ladderData.prices[cont].status, odds[cont])
            cont++
            })
        })
    // })
}

function setStateOdd(status, oddElement){
    if (
        status == "open" && (oddElement.classList.contains("closed") || oddElement.classList.contains("suspended"))){
            oddElement.classList.remove("closed", "suspended")
            oddElement.classList.add("open")
    }else if(status == "suspended" || status == "closed" && oddElement.classList.contains("open")){
        oddElement.classList.remove("open")
        oddElement.classList.add("closed")
    }
}

function setBet(stake, betElement){
    if(!betElement.classList.contains("contains-stake") && stake != 0){
        betElement.classList.add("contains-stake")
    }
    betElement.textContent = stake;
}

function setOddPricePlayer(dataOdd, back, lay){


    back.classList.remove("odd_color_back")
    lay.classList.remove("odd_color_lay")

    if (dataOdd.lay_color){
        lay.classList.add(dataOdd.lay_color)
    }
    if (dataOdd.back_color){
        back.classList.add(dataOdd.back_color)
    }

    back.textContent = dataOdd.back;
    lay.textContent = dataOdd.lay;
    
}

function setSuggetion(data, element){
    element.classList.remove(
            "suggestion-middle", 
            "suggestion-positive", 
            "suggestion-negative"
        );
    
    element.textContent = `${data.liquidity_on_hedge} |+| ${data.liquidity}`;

    if(data.tot_liquidity < 0){      
        element.classList.add("suggestion-negative");

    }else if(data.tot_liquidity == 0){

        element.classList.add("suggestion-middle");
    }else{
        element.classList.add("suggestion-positive");
    }
    element.setAttribute("data-stake-value", data.necessary_stake)
    element.setAttribute("data-side", data.side_to_apply_stake)
}

function showCreatedBetOnLadder(odd, stake){
    document.querySelector(`li.ladder-item-money[data-odd-value='${odd}']`).textContent = stake;
}

async function sendBet(payload){
    response = await fetch(
        "/api/bet/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: payload
        }
    )
}

async function onCLickLadder(li){
    // Recebe o WebElement aonde ocorreu o click na ladder
    let marketId;
    let eventId;
    let marketValue;
    let oddValue;
    let side;
    let runnerId;
    let stake;

    
    marketId = li.dataset.marketId;
    eventId = li.dataset.eventId;
    runnerId = li.dataset.runnerId;
    marketValue = li.dataset.marketValue;
    oddValue = li.dataset.oddValue;
    side = li.dataset.side;

    // guardian 1
    if (side == "None" || side == "null"){
        return;
    }
    
    let stakeSelected = document.querySelector("li.stake-default-item.selected")
    if (stakeSelected){
        stake = parseFloat(stakeSelected.textContent.trim().replace(",", "."))
    }else if (!li.classList.contains("ladder-item-suggestion") && !li.dataset.stakeValue){
        return;
    }

    if (li.classList.contains("ladder-item-suggestion") && li.dataset.stakeValue){
        stake = parseFloat(li.dataset.stakeValue.replace(",", ".")).toFixed(2);
    }

    // TODO: Criar lógica para pegar os valores já criados;
    await sendBet(
        JSON.stringify(
            {   
            "runner_id": runnerId,
            "market_id": marketId,
            "event_id": eventId,
            "odd": parseFloat(oddValue.replace(",", ".")),
            "stake": stake,
            'side': side,
            "keep_in_play": false
            }
        )
    )

    if (response.status == 200){
            showCreatedBetOnLadder(oddValue, stake)
        }
    }

function addLadderListenClick(){
    document.querySelector('#ladder-items').addEventListener("click", (event)=>{
        if (!(event.target.classList.contains("ladder-item-odd") == 1)){
           onCLickLadder(event.target)
        }
    })
}

function scroolToMoney(){
    document.querySelectorAll(".ladder-item-back").forEach(li=>{
        if(li.textContent.trim() != "0"){
            li.scrollIntoView()
            }
        }
    )
}

createConnection();
scroolToMoney();
addLadderListenClick();
addListenerDefaultStakes();
