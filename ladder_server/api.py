from ninja import NinjaAPI
from home.api.routers import router as markets_router
from home.api.routers_data import router as bet_router

app = NinjaAPI()

app.add_router("/markets", markets_router)
app.add_router("/bet", router=bet_router)

