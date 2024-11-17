from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
import os

app = Flask(__name__)

# Configuration for Flask-Mail and Gmail SMTP
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'omingovincent4@gmail.com'
app.config['MAIL_PASSWORD'] = 'shoc cqji yuay dtea'

mail = Mail(app)

@app.route('/')
def index():
    # Rendering the template for the user
    return render_template('index.html')

@app.route('/sending-surprise')
def sending_surprise():
    return render_template('sending.html')


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    # Parse the incoming JSON data from the frontend
    data = request.get_json()

    user_name = data.get('user_name')
    response = data.get('response')
    user_email = data.get('user_email')  # Get the user's email
    
    # Debugging: print the incoming data
    print(f"Received data: user_name={user_name}, response={response}, user_email={user_email}")

    # Define the list of variations of "Yes"
    positive_responses = [
        "yes", "yees", "yes please", "sure", "definitely", "absolutely", 
        "of course", "yep", "yep yep", "yessir", "yess", "yeah"
    ]

    try:
        # Send the email with the user's response to the bot's Valentine's proposal
        msg = Message(
            subject="Valentine's Day Proposal - Response 💖",
            sender='omingovincent4@gmail.com',
            recipients=['omingovincent319@gmail.com'],  # Change to your desired email
        )

        # Craft the email body with the user's response
        msg.body = f"User: {user_name}\nResponse: {response}\n\nAnswered the Valentine's proposal!"
        
        # Debugging: print the email body before sending
        print(f"Sending email to Vincent with body: {msg.body}")
        
        # Send the email to Vincent
        mail.send(msg)
        print("Email sent successfully to Vincent.")

        # Now send the surprise email to the user based on their response
        surprise_msg = Message(
            subject="A Valentine's Day Surprise for You 💌",
            sender='omingovincent4@gmail.com',
            recipients=[user_email],  # Send the email to the user's email
        )

        # Check if the response is a positive response (yes, sure, etc.)
        if any(positive_response in response.lower() for positive_response in positive_responses):
            surprise_msg.body = f"Dear {user_name},\n\nThank you for saying 'Yes'! 🎉 You have made this Valentine's Day extra special. Please enjoy your surprise gift! 💖\n\n- Vincent"
        else:
            surprise_msg.body = f"Dear {user_name},\n\nThank you for your time and for answering! 😊 Though it wasn't the answer I hoped for, I still wish you a wonderful Valentine's Day ahead. 💫\n\n- Vincent"

        # Debugging: print the surprise email body before sending
        print(f"Sending surprise email to {user_email} with body: {surprise_msg.body}")
        
        # Send the personalized surprise email
        mail.send(surprise_msg)
        print("Surprise email sent successfully to the user.")

        # Return success response to the frontend
        return jsonify({'status': 'success', 'message': 'Feedback and surprise email sent successfully!'}), 200

    except Exception as e:
        # Log the error and return an error response to the frontend
        print(f"Error sending email: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
