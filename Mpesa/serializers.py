import uuid
from django.urls import reverse
from rest_framework import serializers

from .validators import validate_possible_number
from .utils import MpesaGateWay
from .models import MpesaResponseBody

pay = MpesaGateWay()

class SendSTKPushSerializer(serializers.Serializer):
    phonenumber = serializers.CharField()

    def validate_phonenumber(self, attrs):
        phonenumber = attrs

        try:
            validate_possible_number(phonenumber, "KE")
        except:
            raise serializers.ValidationError(detail="Invalid Phone Number")
        
        if str(phonenumber)[0] == "+":
            phonenumber = phonenumber[1:]
        elif str(phonenumber)[0] == "0":
            phonenumber = "254" + phonenumber[1:]

        return phonenumber
        

    def create(self, validated_data):
        phonenumber = validated_data['phonenumber']
        order_id = uuid.uuid4() #Your order Id or parameter you'd want associated with a transactipn.
        amount = 10 #Your order total amount

        callback_url = reverse('callback', kwargs={'order_id': order_id}) #Callback includes the order id so each order callback data will be posted to a unique callback url
        payment = pay.stk_push(phonenumber=phonenumber, amount=amount, callback_url=callback_url)

        res = payment.json()

        return res
    

class MpesaResponseBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaResponseBody
        fields = "__all__"

    