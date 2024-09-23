def get_invoice_item_slug(instance):
    return f"{str(instance.product.title)}-{instance.total}"

def get_invoice_slug(instance):
    return f"{instance.company_name}"