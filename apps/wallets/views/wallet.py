"""
Wallet API view
"""

from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.wallets.models.wallet import Wallet
from apps.wallets.serializers.wallet import WalletSerializer


class WalletListCreateAPIView(APIView):
    """
    API view to list all wallets or create a new wallet.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the list of all wallets",
        responses={200: WalletSerializer(many=True)}
    )
    def get(self, request):
        """
        Retrieve all wallets.

        :param request: HTTP request
        :return: Response with a list of wallet objects (200 OK)
        """
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new wallet for a user",
        request_body=WalletSerializer,
        responses={201: WalletSerializer(), 400: "Bad Request"}
    )
    def post(self, request):
        """
        Create a new wallet.

        :param request: HTTP request with wallet data
        :return: Response with created wallet data (201) or errors (400)
        """
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletDetailAPIView(APIView):
    """
    API view to retrieve, update, or delete a wallet by ID.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, wallet_id):
        """
        Retrieve a wallet object by ID.

        :param wallet_id: ID of the wallet to retrieve
        :return: Wallet instance if found, None otherwise
        """
        try:
            return Wallet.objects.get(id=wallet_id)
        except Wallet.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve a wallet by its ID",
        responses={200: WalletSerializer(), 404: "Wallet not found"},
    )
    def get(self, request, wallet_id):
        """
        Get wallet details by ID.

        :param request: HTTP request
        :param wallet_id: Wallet ID
        :return: Response with wallet data (200) or error (404)
        """
        wallet = self.get_object(wallet_id)
        if not wallet:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update a wallet completely",
        request_body=WalletSerializer,
        responses={200: WalletSerializer(), 404: "Wallet not found"}
    )
    def put(self, request, wallet_id):
        """
        Fully update a wallet by ID.

        :param request: HTTP request with wallet data
        :param wallet_id: Wallet ID
        :return: Response with updated wallet (200) or error (404/400)
        """
        wallet = self.get_object(wallet_id)
        if not wallet:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WalletSerializer(wallet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Partially update a wallet",
        request_body=WalletSerializer,
        responses={200: WalletSerializer(), 404: "Wallet not found"}
    )
    def patch(self, request, wallet_id):
        """
        Partially update wallet fields.

        :param request: HTTP request with wallet data
        :param wallet_id: Wallet ID
        :return: Response with updated wallet (200) or error (404/400)
        """
        wallet = self.get_object(wallet_id)
        if not wallet:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = WalletSerializer(wallet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a wallet",
        responses={204: "No Content", 404: "Wallet not found"}
    )
    def delete(self, request, wallet_id):
        """
        Delete a wallet by ID.

        :param request: HTTP request
        :param wallet_id: Wallet ID
        :return: Response with 204 if deleted or 404 if wallet not found
        """
        wallet = self.get_object(wallet_id)
        if not wallet:
            return Response({"error": "Wallet not found"}, status=status.HTTP_404_NOT_FOUND)
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
