from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='get_name_radio')
def get_name_radio(dictionary, key):
    event_id = dictionary.get(key)

    return f"market-name-{event_id}"


@register.filter(name='available_amount')
def available_amount(dictionary, key):
    amount = dictionary.get(key)
    return f"R${float(amount):.0f}"


@register.filter(name="get_exists_market")
def get_exists_market(markets):
    return bool(markets)
