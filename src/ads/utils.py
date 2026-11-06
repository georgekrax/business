import random, string

def unique_ad_id_generator(instance):
    new_ad_id = ''.join(random.choice(string.digits) for _ in range(20))

    Klass = instance.__class__
    qs = Klass.objects.filter(ad_id=new_ad_id)
    if qs.exists():
        return unique_ad_id_generator(instance)
    return new_ad_id