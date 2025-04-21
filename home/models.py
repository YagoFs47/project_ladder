from django.db import models
from colorama import Fore, init
init()

# Create your models here.
# class ApostaModel(models.Model):

#     STATE_CHOICES = (
#         ("waiting", "waiting"),
#         ("matched", "matched"),
#         ("matched_closed", "matched_closed"),
#     )

#     event_id = models.CharField(max_length=30)
#     market_id = models.CharField(max_length=30)
#     runner_id = models.CharField(max_length=30)
#     side = models.CharField(max_length=4)
#     odd = models.DecimalField(max_digits=8, decimal_places=2)
#     stake = models.DecimalField(max_digits=8, decimal_places=2)
#     status = models.CharField(max_length=14, choices=STATE_CHOICES, default="waiting") # True[matched|correspondido]
#     # is_finished = models.BooleanField(default=False, blank=True) 
#     # try_close = models.BooleanField(default=False, blank=True)
#     # True[não está mais em análise, desconsidera pois o usuário cancelou a operação, ou pq ela já foi correspondida e fechada]


#     def __repr__(self):
#         if self.side == "back":
#             return f'[{Fore.GREEN}EVENT {self.event_id}{Fore.RESET}][{Fore.GREEN}MERCADO {self.market_id}{Fore.RESET}][{Fore.GREEN}RUNNER {self.runner_id}{Fore.RESET}][{Fore.GREEN}ODD {self.odd}{Fore.RESET}][{Fore.GREEN}STAKE {self.stake}{Fore.RESET}][{Fore.GREEN}STATUS {self.status}{Fore.RESET}][{Fore.BLUE}SIDE {self.side}{Fore.RESET}]'
#         return f'[{Fore.GREEN}EVENT {self.event_id}{Fore.RESET}][{Fore.GREEN}MERCADO {self.market_id}{Fore.RESET}][{Fore.GREEN}RUNNER {self.runner_id}{Fore.RESET}][{Fore.GREEN}ODD {self.odd}{Fore.RESET}][{Fore.GREEN}STAKE {self.stake}{Fore.RESET}][{Fore.GREEN}STATUS {self.status}{Fore.RESET}][{Fore.RED}SIDE {self.side}{Fore.RESET}]'
    
#     def __str__(self):
#         if self.side == "back":
#             return f'[{Fore.GREEN}EVENT {self.event_id}{Fore.RESET}][{Fore.GREEN}MERCADO {self.market_id}{Fore.RESET}][{Fore.GREEN}RUNNER {self.runner_id}{Fore.RESET}][{Fore.GREEN}ODD {self.odd}{Fore.RESET}][{Fore.GREEN}STAKE {self.stake}{Fore.RESET}][{Fore.GREEN}STATUS {self.status}{Fore.RESET}][{Fore.BLUE}SIDE {self.side}{Fore.RESET}]'
#         return f'[{Fore.GREEN}EVENT {self.event_id}{Fore.RESET}][{Fore.GREEN}MERCADO {self.market_id}{Fore.RESET}][{Fore.GREEN}RUNNER {self.runner_id}{Fore.RESET}][{Fore.GREEN}ODD {self.odd}{Fore.RESET}][{Fore.GREEN}STAKE {self.stake}{Fore.RESET}][{Fore.GREEN}STATUS {self.status}{Fore.RESET}][{Fore.RED}SIDE {self.side}{Fore.RESET}]'
    
#     def to_json(self):
#         return {
#             "event_id": self.event_id,
#             "market_id": self.market_id,
#             "runner_id": self.runner_id,
#             "side": self.side,
#             "odd": float(self.odd),
#             "stake": float(self.stake),
#         }

class ClosingBetModel(models.Model):

    STATE_CHOICES = (
        ("waiting", "waiting"),
        ("matched", "matched"),
        ("matched_closed", "matched_closed"),
    )
    event_id = models.CharField(max_length=30)
    market_id = models.CharField(max_length=30)
    runner_id = models.CharField(max_length=30)
    side = models.CharField(max_length=4)
    odd = models.DecimalField(max_digits=8, decimal_places=2)
    stake = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=14, choices=STATE_CHOICES, default="waiting") # True[matched|correspondido]
    

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
        } 

class OpeningBetModel(models.Model):

    STATE_CHOICES = (
        ("waiting", "waiting"),
        ("matched", "matched"),
        ("matched_closed", "matched_closed"),
    )

    event_id = models.CharField(max_length=30)
    market_id = models.CharField(max_length=30)
    runner_id = models.CharField(max_length=30)
    side = models.CharField(max_length=4)
    odd = models.DecimalField(max_digits=8, decimal_places=2)
    stake = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=14, choices=STATE_CHOICES, default="waiting") # True[matched|correspondido]
    closer = models.ForeignKey(ClosingBetModel, on_delete=models.DO_NOTHING, null=True, blank=True) # FK para o fechamento da aposta

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
        } 

class FlowModel(models.Model):

    ORIENTATIONS = (
        ("back", "back"),
        ("lay", "lay"),
    )

    orientation = models.CharField(max_length=4, choices=ORIENTATIONS) # back ou lay
    is_open = models.BooleanField(default=True) # True[aberto] False[fechado]