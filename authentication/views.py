from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import csv
import os
from .models import CustomUser
from whatsapp_notifications.main import send_whatsapp_messages  # Import the function

def export_users_to_csv(request):
    # Create the HttpResponse object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['ID', 'Username', 'Email', 'First Name', 'Last Name', 'WhatsApp Number', 'Date Joined'])

    # Query all users and write their data
    for user in CustomUser.objects.all():
        writer.writerow([user.id, user.username, user.email, user.first_name, user.last_name, user.whatsapp_number, user.date_joined])

    return response

def validate_cameroon_number(number):
    """
    Validates and formats a Cameroon phone number.
    :param number: The phone number to validate.
    :return: A properly formatted phone number with +237 or None if invalid.
    """
    if number.startswith("6") and len(number) == 9:  # Local format (e.g., 677123456)
        return f"+237{number}"
    elif number.startswith("+237") and len(number) == 13:  # Already in international format
        return number
    else:
        return None

def send_whatsapp_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        selected_users = request.POST.getlist('users')
        media = request.FILES.get('media')  # Handle uploaded media file

        # Debug logs
        print(f"Message: {message}")
        print(f"Selected Users: {selected_users}")

        if not message:
            messages.error(request, "Message cannot be empty.")
            return redirect('send_whatsapp_message')

        if not selected_users:
            messages.error(request, "No users selected.")
            return redirect('send_whatsapp_message')

        # Save the media file temporarily if it exists
        media_path = None
        if media:
            media_path = os.path.join('temp', media.name)
            with open(media_path, 'wb') as f:
                for chunk in media.chunks():
                    f.write(chunk)

        # Query selected users and validate their phone numbers
        users = CustomUser.objects.filter(id__in=selected_users)
        numbers = []
        for user in users:
            formatted_number = validate_cameroon_number(user.whatsapp_number)
            if formatted_number:
                numbers.append(formatted_number)

        # Debug logs
        print(f"Validated Numbers to send messages to: {numbers}")

        if not numbers:
            messages.error(request, "No valid Cameroon WhatsApp numbers found for the selected users.")
            return redirect('send_whatsapp_message')

        # Call the send_whatsapp_messages function
        try:
            from whatsapp_notifications.main import send_whatsapp_messages  # Ensure the function is imported
            print("Calling send_whatsapp_messages function...")  # Debug log
            send_whatsapp_messages(message, numbers, media_path)
            messages.success(request, "Messages sent successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send messages: {e}")
            print(f"Error: {e}")

        # Clean up the temporary media file
        if media_path and os.path.exists(media_path):
            os.remove(media_path)

        return redirect('send_whatsapp_message')

    users = CustomUser.objects.all()
    return render(request, 'authentication/send_whatsapp_message.html', {'users': users})
