def send_notification(user, message):
    if user["notification"] == "email":
        print(f"📧 Email enviado a {user['name']}: {message}")
    elif user["notification"] == "sms":
        print(f"📱 SMS enviado a {user['name']}: {message}")