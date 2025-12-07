"""
Transfer API view
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.wallets.services.transfer import TransferService
from apps.wallets.serializers.transfer import TransferSerializer

from src.settings.utils.logging import logger


class TransferAPIView(APIView):
    """
    Wallet-to-wallet transfer API with race condition protection.

    Features:
        - Atomic transactions with `select_for_update` and F-expressions
        - 10% commission for transfers >1000 units, credited to admin wallet (ID=1)
        - Asynchronous Celery notification with 3 automatic retries
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
        Execute a wallet-to-wallet transfer.

        Race Condition Protection:
            - Pessimistic locking (`select_for_update`)
            - Atomic transactions
            - Safe balance updates with F-expressions

        Commission:
            - 10% commission for transfers > 1000 units
            - Commission credited to admin wallet (ID=1)

        Asynchronous Notification:
            - Notification sent via Celery after successful transfer
            - Automatic retry on failure (3 attempts, 3 seconds apart)
        """,
        request_body=TransferSerializer,
        responses={
            201: openapi.Response(
                description="Transfer completed successfully",
                examples={
                    "application/json": {
                        "success": True,
                        "transaction_id": 123,
                        "transaction_group": "550e8400-e29b-41d4-a716-446655440000",
                        "amount": "500.00",
                        "commission": "0.00",
                        "total_debited": "500.00"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation error or insufficient funds",
                examples={
                    "application/json": {
                        "error": "Insufficient funds. Available: 1000.00, Required: 2000.00"
                    }
                }
            ),
            401: "Unauthorized",
            500: "Internal server error"
        },
        tags=['Transfers'],
        security=[{'Token': []}]
    )
    def post(self, request):
        """
        Create a wallet-to-wallet transfer.

        :param request: DRF request object containing transfer data
        :type request: rest_framework.request.Request
        :return: JSON response with transfer result or error message
        :rtype: rest_framework.response.Response
        """
        serializer = TransferSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            result = TransferService.execute_transfer(
                sender_id=serializer.validated_data['sender_id'],
                recipient_id=serializer.validated_data['recipient_id'],
                amount=serializer.validated_data['amount'],
                description=serializer.validated_data.get('description', '')
            )

            return Response(result, status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.warning(f"Transfer validation error: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Transfer error: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
