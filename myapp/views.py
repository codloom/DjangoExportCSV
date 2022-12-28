from django.core.paginator import Paginator
from django.shortcuts import render
import csv
import datetime
from django.http import HttpResponse
from myapp.forms import ProductForm

from myapp.models import Product, ProductImage

def product_list(request):
    
    obj = request.GET.get('obj')
    print(obj) 
    if obj:  
        product_list = Product.objects.filter(name__icontains=obj)  
    else:
        product_list = Product.objects.all()   
        
    paginator = Paginator(product_list, 3) # mostra 3 produtos por pagina
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'list.html', {'page_obj': page_obj})



from django.shortcuts import redirect

def form_product(request):
    form = ProductForm()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            
            files = request.FILES.getlist('products')
            if files:
                for f in files:
                    ProductImage.objects.create(
                        product=product, 
                        image=f)
            return redirect('product-list')  
                 
    return render(request, 'form-create.html', {'form': form})


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Products' + \
        str(datetime.datetime.now())+'.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Nome','Preço','Descrição','Imagens']) # head Titulo
    
    obj = request.GET.get('obj')
    print(obj)

    # products = Product.objects.all() # lista todos os produtos 
    if obj:  
        products = Product.objects.filter(name__icontains=obj)  
    else:
        products = Product.objects.all()

    for product in products: 
        image_product = [el.image.url for el in product.products.all()] # todas as imagens do produto
  
        writer.writerow([product.name, product.price,
            product.description,image_product])
    
    return response