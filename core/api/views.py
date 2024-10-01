from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *


class SellerSignup(APIView):
    def post(self, request):
        mobile_number = request.data.get("mobileNumber")
        account, created = Account.objects.get_or_create(mobile_number=mobile_number)

        refresh = RefreshToken.for_user(account)

        return Response(
            {"token": str(refresh.access_token), "account_id": account.id},
            status=status.HTTP_201_CREATED,
        )


class CreateStoreView(APIView):
    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            store = serializer.save(seller=request.user)
            store.link = store.name.lower().replace(" ", "-") + "-" + str(store.id)
            store.save()
            return Response(
                {"storeId": store.id, "storeLink": store.link},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadInventoryView(APIView):
    def post(self, request):
        category_name = request.data.get("category")
        category, created = Category.objects.get_or_create(name=category_name)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(category=category, store=request.user.store)
            return Response(
                {
                    "productId": serializer.instance.id,
                    "productName": serializer.instance.name,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoreDetailsView(APIView):
    def get(self, request, store_link):
        store = Store.objects.get(link=store_link)
        serializer = StoreSerializer(store)
        return Response(serializer.data)


class StoreCatalogView(APIView):
    def get(self, request, store_link):
        store = Store.objects.get(link=store_link)
        categories = Category.objects.filter(product__store=store).distinct()
        response = []
        for category in categories:
            products = Product.objects.filter(category=category, store=store)
            products_data = ProductSerializer(products, many=True).data
            response.append({"category": category.name, "products": products_data})
        return Response(response)


class StoreDetailsView(APIView):
    def get(self, request, store_link):
        try:
            store = Store.objects.get(link=store_link)
            serializer = StoreSerializer(store)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Store.DoesNotExist:
            return Response(
                {"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND
            )


class StoreCatalogView(APIView):
    def get(self, request, store_link):
        try:
            store = Store.objects.get(link=store_link)
            categories = Category.objects.filter(product__store=store).distinct()
            response = []
            for category in categories:
                products = Product.objects.filter(category=category, store=store)
                products_data = ProductSerializer(products, many=True).data
                response.append(
                    {
                        "category": CategorySerializer(category).data,
                        "products": products_data,
                        "product_count": products.count(),
                    }
                )
            return Response(response, status=status.HTTP_200_OK)

        except Store.DoesNotExist:
            return Response(
                {"error": "Store not found"}, status=status.HTTP_404_NOT_FOUND
            )


class CartView(APIView):
    def post(self, request):
        session_id = request.data.get("session_id")
        product_id = request.data.get("product_id")
        qty = request.data.get("qty")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        cart, _ = Cart.objects.get_or_create(session_id=session_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if qty > 0:
            cart_item.quantity = qty
            cart_item.save()
        else:
            cart_item.delete()

        return Response(
            {"message": "Cart updated successfully"}, status=status.HTTP_200_OK
        )


class PlaceOrderView(APIView):
    def post(self, request):
        mobile_number = request.data.get("mobileNumber")
        cart_data = request.data.get("cart")
        customer, _ = Customer.objects.get_or_create(mobile_number=mobile_number)

        total_price = 0
        for item in cart_data["items"]:
            product_id = item["product"]
            qty = item["quantity"]
            product = Product.objects.get(id=product_id)
            total_price += product.sale_price * qty

        order = Order.objects.create(
            customer=customer, store_id=cart_data["store_id"], total_price=total_price
        )

        return Response({"orderId": order.id}, status=status.HTTP_201_CREATED)
