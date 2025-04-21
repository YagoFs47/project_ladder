from typing import List, Dict

hash_oposition_side: Dict[str, str] = {
    "back": "lay",
    "lay": "back"
}

def generate_odds_back_lay():
    odds = []
    cont: float = 1.0
    somatorio: float = 0.01
    while cont < 1000:

        data = {"odd": None, "back": "", "lay": "", "available_amount": ""}
        cont = round(somatorio + cont, 2)
        data['odd'] = round(cont, 2)
        odds.append(data.copy())
        
        if cont >= 100:
            somatorio = 10

        elif cont >= 50:
            somatorio = 5

        elif cont >= 20:
            somatorio = 1
        
        elif cont >= 10:
            somatorio = .5
        
        elif cont >= 4:
            somatorio = 0.1

        elif cont >= 3:
            somatorio = 0.05
        
        elif cont >= 2:
            somatorio = 0.02

    return odds

def compair_odd(dict_odd, price, market):
    if dict_odd["odd"] == price['odds']:
        dict_odd[price['side']] = price['available-amount']
        dict_odd['available_amount'] = price['available-amount']

def generate_matriz_ladder(markets):
    for market in markets: # para cada mercado
        odds_ladder: List[dict] = generate_odds_back_lay() # gera uma ladder vazia

        #precisamos preencher a ladder com as odds que estão atuando naquele mercado
        #para isso preciso varrer as odds do mercado e introduzir elas na ladder
        for dict_odd in odds_ladder: # para cada odd da ladder
            for price in market["runners"][1]["prices"]: # para cada odd do mercado
                compair_odd(dict_odd, price, market)

        #aqui eu inverto a ordem que esta de forma crescente para ordem decrescente
        # FROM DESC TO ASC
        market['ladder'] = list(reversed(odds_ladder.copy()))