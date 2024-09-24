def get_invoice_item_slug(instance):
    return f"{str(instance.product.title)}-{instance.total}"


def get_invoice_slug(instance):
    return f"{instance.company_name}"


def get_invoice_item_connector_slug(instance):
    return f"{instance.invoice.company_name}-{str(instance.uid).split('-')[0]}"

def get_invoice_media_path_prefix(instance, filename):
    return f"media/invoices/{filename}"