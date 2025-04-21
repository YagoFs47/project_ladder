
// let websocket = new WebSocket("ws://127.0.0.1:8000/ws/home/")

setInterval(refreshAllData, 15000)

function refreshAllData(){
    fetch("http://localhost:8000/home/").then(
        (response) => response.text()
    ).then(
        (html)=>{
            document.body.innerHTML = html
        }
    )
}

function openMatchup(id){
    console.log("fecthing...")
    fetch(
        `http://localhost:8000/api/markets/${id}`,
        {
            method: "get",
        }
    ).then(
        (response) => response.json()
    ).then((data)=>{
        window.open(`https://bolsadeaposta.bet.br/b/exchange/sport/soccer/event/${id}/market/${data.markets[0].id}`, "_blank")
        window.open(`http://localhost:8000/home/${id}`, "_blank")
    });

        // {
        //     message: {
        //         action: "new_page", 
        //         id_matchup: id,
        //         page_direction: "home_page"
        //     }
        // }

};