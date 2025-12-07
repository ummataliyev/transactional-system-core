"""
Transaction API view
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.wallets.models.transaction import Transaction
from apps.wallets.serializers.transaction import TransactionSerializer


class TransactionHistoryAPIView(APIView):
    """
    API endpoint to retrieve the last 50 transactions for a given wallet.

    Query parameter:
        - wallet_id (int, required): ID of the wallet to fetch transactions for.

    :param request: DRF request object
    :type request: rest_framework.request.Request
    :return: JSON response containing serialized transactions or an error message
    :rtype: rest_framework.response.Response
    """
    permission_classes = [IsAuthenticated]

    wallet_id_param = openapi.Parameter(
        'wallet_id',
        openapi.IN_QUERY,
        description="ID of the wallet to fetch transactions for",
        type=openapi.TYPE_INTEGER,
        required=True
    )

    @swagger_auto_schema(
        operation_description="Retrieve the last 50 transactions for a specific wallet",
        manual_parameters=[wallet_id_param],
        responses={
            200: TransactionSerializer(many=True),
            400: openapi.Response(
                'Bad Request',
                examples={'application/json': {'error': 'wallet_id parameter is required'}}
            )
        }
    )
    def get(self, request):
        """
        GET method to fetch the last 50 transactions for a specified wallet.

        :param request: DRF request object
        :type request: rest_framework.request.Request
        :return: JSON response containing a list of serialized transactions or error message
        :rtype: rest_framework.response.Response
        """
        wallet_id = request.query_params.get('wallet_id')

        if not wallet_id:
            return Response(
                {'error': 'wallet_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        transactions = Transaction.objects.filter(
            sender_id=wallet_id
        ) | Transaction.objects.filter(
            recipient_id=wallet_id
        )

        transactions = transactions.order_by('-created_at')[:50]
        serializer = TransactionSerializer(transactions, many=True)

        return Response(serializer.data)
