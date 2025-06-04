from ninja import NinjaAPI

from home.api.manage_apostas import router as default_stake
from home.api.routers import router as markets_router
from home.api.routers_data import router as bet_router

app = NinjaAPI()

app.add_router("/default-stakes", default_stake)
app.add_router("/markets", markets_router)
app.add_router("/bet", router=bet_router)
