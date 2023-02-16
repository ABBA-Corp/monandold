from rest_framework import serializers
from customer.models import UserInfo
from .models import *



class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = '__all__'

        



class ProductSerializer(serializers.ModelSerializer):

    class Meta:

        model = Product

        fields = '__all__'





class OrderSerializer(serializers.ModelSerializer):

    class Meta:

        model = Order

        fields = '__all__'





class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:

        model = OrderDetail

        fields = '__all__'





class CardObjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    count = serializers.IntegerField()
    customer = serializers.CharField()
    product = serializers.CharField()


    def create(self, validated_data):
        userinfo = None
        try:
            userinfo = UserInfo.objects.filter(user_id=validated_data['customer']).first()
        except:
            pass
        if userinfo == None:
            Card = CardObject(
                id=validated_data['id'],
                customer_id=validated_data['customer'],
                product_id=validated_data['product'],
                count=validated_data['count'],
                condition=False,
            )
            Card.save()
        else:
            Card = CardObject(
                id=validated_data['id'],
                u_id=userinfo.u_id,
                customer_id=validated_data['customer'],
                product_id=validated_data['product'],
                count=validated_data['count'],
                condition=False,
            )
            Card.save()
        return Card




class LikeSerializer(serializers.ModelSerializer):

    class Meta:

        model = Like

        fields = '__all__'





