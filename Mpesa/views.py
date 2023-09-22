from django.forms.models import model_to_dict
from rest_framework import views, response, status

from .serializers import SendSTKPushSerializer, MpesaResponseBodySerializer
from .models import MpesaResponseBody, Transaction

class SendSTKPushView(views.APIView):
    def post(self, request, format=None):
        serializer = SendSTKPushSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.save()
            return response.Response(res, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MpesaCallbackView(views.APIView):
    def post(self, request, order_id, format=None):
        body = request.data

        if body:
            mpesa = MpesaResponseBody.objects.create(order_id=order_id, body=body) #Save Mpesa Response Body with order ID.
        
            mpesa_body = model_to_dict(mpesa)['body']

            transactions = Transaction.objects.create(
                order_id=order_id,
                amount=mpesa_body['Body']['stkCallback']['CallbackMetadata']['Item'][0]["Value"],
                receipt_no=mpesa_body['Body']['stkCallback']['CallbackMetadata']['Item'][1]["Value"],
                phonenumber=mpesa_body['Body']['stkCallback']['CallbackMetadata']['Item'][-1]["Value"],
            )

            return response.Response({"message": "Callback received and processed successfully."})
        return response.Response({"failed": "Transaction Failed"}, status=status.HTTP_400_BAD_REQUEST)

                
    def get(self, request, order_id, format=None):
        try:
            mpesa_response = MpesaResponseBody.objects.get(order_id=order_id)
        except MpesaResponseBody.DoesNotExist:
            return response.Response({"Error": "Response does not exist"})
        
        serializer = MpesaResponseBodySerializer(mpesa_response)
        serialized_data = serializer.data
        return response.Response({"response": serialized_data})