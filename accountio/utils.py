def get_customer_slug(instance):
    return f"{instance.username}-{str(instance.uid).split('-')[0]}"
