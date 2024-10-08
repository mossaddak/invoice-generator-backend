def get_product_slug(instance):
    return f"{instance.title}-{str(instance.uid).split('-')[0]}"


def get_product_media_path_prefix(instance, filename):
    return f"media/product/{filename}"
