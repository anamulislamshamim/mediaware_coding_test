from django.views import generic
from django.views.generic import ListView, CreateView, UpdateView

from rest_framework.views import APIView
from rest_framework.response import Response

from product.serializers import ProductSerializer, ProductImageSerializer

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from product.models import Variant, Product


class ProductView(ListView):
    template_name = 'products/list.html'
    model = Product
    context_object = 'product_list'
    paginate_by = 3
    queryset = Product.objects.all().order_by('-created_at')
    
    # def get_queryset(self):
    #     filter_string = {}
    #     print('from get_queryset: ', self.request.GET)
    #     for key in self.request.GET:
    #         if self.request.GET.get(key):
    #             filter_string[f"{key}__icontains"] = self.request.GET.get(key)
    #     print(filter_string)
    #     return Product.objects.filter(**filter_string)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['product'] = True
    #     context['request'] = ''
    #     if self.request.GET:
    #         context['request'] = self.request.GET['title__icontains']
    #     return context


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    
    
class AddProductView(APIView):
    
    def post(self, request, *args, **kwargs):
        posts_serializer = ProductSerializer(data=request.data.get('product'))
        product_image_serializer = ProductImageSerializer(data={"product": posts_serializer.initial_data, "file_path": request.data.get('image')[0].get('path')})
        
        print({"product": posts_serializer, "file_path": request.data.get('image')[0].get('path')})

        if product_image_serializer.is_valid():
            product_image_serializer.save()
        
        if posts_serializer.is_valid():
            posts_serializer.save()
            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    


