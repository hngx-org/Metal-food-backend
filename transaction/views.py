from django.shortcuts import render

# Create your views here.
# Import necessary modules
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Define a view for creating withdrawal requests
class WithdrawalRequestCreateView(generics.CreateAPIView):
    # Get all Withdrawals objects
    queryset = Withdrawals.objects.all()
    
    # Use WithdrawalRequestSerializer for serialization
    serializer_class = WithdrawalRequestSerializer
    
    # Require authentication for this view
    permission_classes = [IsAuthenticated]

    # Handle HTTP POST requests for creating withdrawal requests
    def create(self, request, *args, **kwargs):
        # Serialize the incoming request data
        serializer = self.get_serializer(data=request.data)

        # Check if the serializer is valid, raise an exception if not
        if serializer.is_valid(raise_exception=True):
            # Create a new Withdrawals object with the validated data
            withdrawal_request = Withdrawals.objects.create(
                amount=serializer.validated_data["amount"],
                user_id=request.user
            )

            # Set the status of the withdrawal request to "success"
            withdrawal_request.status = "success"
            withdrawal_request.save()

            # Prepare a response with relevant data
            response_data = {
                "message": "Withdrawal request created successfully",
                "statusCode": status.HTTP_201_CREATED,
                "data": {
                    "id": withdrawal_request.id,
                    "user_id": withdrawal_request.user_id,
                    "status": withdrawal_request.status,
                    "amount": withdrawal_request.amount,
                    "created_at": withdrawal_request.created_at.isoformat()
                }
            }

            # Return the response with a 201 Created status
            return Response(response_data, status=status.HTTP_201_CREATED)
