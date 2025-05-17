let eventId;
let marketId;
let runnerId;

var element = document.querySelector(".ladder-item").dataset;
eventId = element.eventId;
marketId = element.marketId;
const HASH_OPOSITION = {
    "back": "lay",
    "lay": "back"
}

function createConnection(){
    const socket = new WebSocket(
        `/ws?eventId=${eventId}&marketId=${marketId}&typeChannel=ladder`,
    );

    socket.addEventListener("message", (event)=>{
        
        document.querySelectorAll(`li.ladder-item-lay`).forEach((li)=>{
            li.textContent = '';
        })
        document.querySelectorAll(`li.ladder-item-back`).forEach((li)=>{
            li.textContent = '';
        })
        // console.log(JSON.parse(event.data))
        JSON.parse(event.data).runners[1].prices.forEach((price)=>{
            // console.log(price)
            let odd = `${price.odds}`.replace(".", ',')
            if (odd.search(",") < 0){
                odd = `${price.odds},0`
            }
            // console.log(odd)
            let available_amount = price['available-amount'].toFixed(2)
            let side = price.side
            document.querySelector(`li.ladder-item-${HASH_OPOSITION[side]}[data-odd-value='${odd}']`).textContent = available_amount;
        })
    })

}

function onCLickLadder(li){
    // Recebe o WebElement aonde ocorreu o click na ladder
    let marketId;
    let eventId;
    let marketValue;
    let oddValue;
    let side;
    let runnerId;

    
    marketId = li.dataset.marketId;
    eventId = li.dataset.eventId;
    runnerId = li.dataset.runnerId;
    marketValue = li.dataset.marketValue;
    oddValue = li.dataset.oddValue;
    side = li.dataset.side;

    fetch(
        "/api/bet/",
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
                    "odds": parseFloat(oddValue.replace(",", ".")),
                    "stake": 1.00,
                    'side': side,
                    "keep_in_play": false
                }
            )
        }
    )
    }

function addLadderListenClick(){
    document.querySelector('#ladder-items').addEventListener("click", (event)=>{
        if (!(event.target.classList.contains("ladder-item-odd") == 1)){
           onCLickLadder(event.target)
        }
    })
}

createConnection();
addLadderListenClick()

