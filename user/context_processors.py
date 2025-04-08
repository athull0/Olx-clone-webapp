from .models import Category

def categories_processor(request):
    return {'cat':Category.objects.all()}