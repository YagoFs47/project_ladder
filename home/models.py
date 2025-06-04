from colorama import Fore, init
from django.db import models

init()

class StakeDefaultModel(models.Model):
    stake = models.DecimalField(
        max_digits=8, decimal_places=2, unique=True
        )
    
    def __str__(self):
        return f'Stake = {self.stake}'


class SessionsBolsaApostaModel(models.Model):
    """Modelo para armazenar as sessões do cliente na bolsa de apostas"""
    biab_customer = models.CharField(max_length=500, blank=True)  # ID do cliente na bolsa de apostas
    authorization = models.CharField(max_length=500, blank=True)  # Token de autorização do cliente na bolsa de apostas
    sb = models.CharField(max_length=500, blank=True)  # Token de sessão do cliente na bolsa de apostas
    device_token = models.CharField(max_length=500, blank=True)  # Token de sessão do cliente na bolsa de apostas

    def to_list(self):
        return [self.biab_customer, self.authorization, self.sb]


class MatchupModel(models.Model):

    id_matchup = models.CharField()
    matchup_name = models.CharField(max_length=150)
    status = models.CharField(max_length=30)
    is_running = models.BooleanField(default=False)
    team_a = models.CharField(max_length=30)
    team_b = models.CharField(max_length=30)
    time_elapsed = models.CharField(max_length=3)

    def to_json(self):
        return {
            "name": self.matchup_name,
            "id": self.id_matchup,
            "start": self.start,
            "status": self.status,
            "sport": self.sport,
            "is_running": self.is_running,
            "team_a": self.team_a,
            "team_b": self.team_b,
            "time_elapsed": self.time_elapsed
        }

    def __repr__(self):
        return f'[{Fore.GREEN}MATCHUP {self.matchup_name}{Fore.RESET}]'

    def __str__(self):
        return f'[{Fore.GREEN}MATCHUP {self.matchup_name}{Fore.RESET}]'


class EventIdModel(models.Model):
    event_id = models.CharField(max_length=50, unique=True)


class MarketIdModel(models.Model):
    market_id = models.CharField(max_length=50)
    event_id = models.ForeignKey(EventIdModel, on_delete=models.CASCADE)


class BetModel(models.Model):

    STATE_CHOICES = (
        ("waiting", "waiting"),
        ("matched", "matched"),
        ("matched_closed", "matched_closed"),
    )

    bet_id = models.CharField(max_length=30)
    event_id = models.CharField(max_length=30)
    market_id = models.CharField(max_length=30)
    runner_id = models.CharField(max_length=30)
    side = models.CharField(max_length=4)
    odd = models.DecimalField(max_digits=8, decimal_places=2)
    stake = models.DecimalField(max_digits=8, decimal_places=2)
    liquidity = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)
    stake_matched = models.DecimalField(max_digits=8, decimal_places=2)
    partial_stake = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=14, choices=STATE_CHOICES, default="waiting")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # closer = models.ForeignKey(ClosingBetModel, on_delete=models.DO_NOTHING, null=True, blank=True)  # FK para o fechamento da aposta

    # is_finished = models.BooleanField(default=False, blank=True)
    # try_close = models.BooleanField(default=False, blank=True)
    # True[não está mais em análise, desconsidera pois o usuário cancelou a operação, ou pq ela já foi correspondida e fechada]

    def __repr__(self):
        if self.side == "back":
            return f'[{Fore.GREEN}EVENT {self.event_id}{Fore.RESET}][{Fore.GREEN}MERCADO {self.market_id}{Fore.RESET}][{Fore.GREEN}RUNNER {self.runner_id}{Fore.RESET}][{Fore.GREEN}ODD {self.odd}{Fore.RESET}][{Fore.GREEN}STAKE {self.stake}{Fore.RESET}][{Fore.GREEN}STATUS {self.status}{Fore.RESET}][{Fore.BLUE}SIDE {self.side}{Fore.RESET}]'
        return f'[{Fore.GREEN}EVENT {self.event_id}{Fore.RESET}][{Fore.GREEN}MERCADO {self.market_id}{Fore.RESET}][{Fore.GREEN}RUNNER {self.runner_id}{Fore.RESET}][{Fore.GREEN}ODD {self.odd}{Fore.RESET}][{Fore.GREEN}STAKE {self.stake}{Fore.RESET}][{Fore.GREEN}STATUS {self.status}{Fore.RESET}][{Fore.RED}SIDE {self.side}{Fore.RESET}]'

    def __str__(self):
        if self.side == "back":
            return f'[{Fore.GREEN}EVENT {self.event_id}{Fore.RESET}][{Fore.GREEN}MERCADO {self.market_id}{Fore.RESET}][{Fore.GREEN}RUNNER {self.runner_id}{Fore.RESET}][{Fore.GREEN}ODD {self.odd}{Fore.RESET}][{Fore.GREEN}STAKE {self.stake}{Fore.RESET}][{Fore.GREEN}STATUS {self.status}{Fore.RESET}][{Fore.BLUE}SIDE {self.side}{Fore.RESET}]'
        return f'[{Fore.GREEN}EVENT {self.event_id}{Fore.RESET}][{Fore.GREEN}MERCADO {self.market_id}{Fore.RESET}][{Fore.GREEN}RUNNER {self.runner_id}{Fore.RESET}][{Fore.GREEN}ODD {self.odd}{Fore.RESET}][{Fore.GREEN}STAKE {self.stake}{Fore.RESET}][{Fore.GREEN}STATUS {self.status}{Fore.RESET}][{Fore.RED}SIDE {self.side}{Fore.RESET}]'

    def to_json(self):
        return {
            "event_id": self.event_id,
            "market_id": self.market_id,
            "runner_id": self.runner_id,
            "side": self.side,
            "odd": float(self.odd),
            "stake": float(self.stake),
            "status": self.status,
            "bet_id": self.bet_id
        }
    
    def to_bet_schema_model(self):
        return {
            "id": self.bet_id,
            "event-id": self.event_id,
            "market-id": self.market_id,
            "runner-id": self.runner_id,
            "side": self.side,
            "odds": float(self.odd),
            "stake": float(self.stake),
            "stake-matched": self.stake_matched,
            "partial_stake": self.partial_stake,
            "status": self.status,
            "created-at": self.created_at,
            "liquidity": self.liquidity
        }