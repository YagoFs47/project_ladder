from django.contrib import admin
from home.models import ClosingBetModel, OpeningBetModel, MatchupModel, FlowModel


# Register your models here.
admin.site.register(ClosingBetModel)
admin.site.register(OpeningBetModel)
admin.site.register(MatchupModel)
admin.site.register(FlowModel)

