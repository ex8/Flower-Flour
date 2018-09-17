from django.shortcuts import render, get_object_or_404
from custom_cakes.models import Cake, CustomCakeConfig


def gallery_list(request):
    config = CustomCakeConfig.objects.get(id=1)
    cakes = Cake.objects.filter(available=True)
    return render(request, 'custom_cakes/list.html', context={
        'config': config,
        'cakes': cakes
    })


def gallery_detail(request, id):
    config = CustomCakeConfig.objects.get(id=1)
    cake = get_object_or_404(Cake, id=id)
    similar_cakes = Cake.objects.order_by('?').exclude(id=id)[:3]
    return render(request, 'custom_cakes/detail.html', {
        'config': config,
        'cake': cake,
        'similar_cakes': similar_cakes
    })
