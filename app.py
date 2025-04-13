from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sys
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import time
import threading
import logging
from werkzeug.utils import secure_filename
from utils import email_template, hr_email_sender


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_sender.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Global variables for tracking progress
sending_status = {
    'is_sending': False,
    'total': 0,
    'sent': 0,
    'failed': 0,
    'current_recipient': '',
    'progress': 0
}

# Email template
def create_email_body(name, title, company):
    """Create a personalized email body"""
    email_body = f"""
Dear {name},

I hope this email finds you well. My name is Venkat Kumar Meda, a Computer Vision Engineer with expertise in AI-driven surveillance solutions and Kubernetes-based deployments.

I noticed that {company} is at the forefront of innovation, and I'm particularly interested in bringing my technical skills to your organization. I believe you might be the right person to connect with regarding potential opportunities at {company}.

My experience includes:
- Developing versatile Kubernetes platforms across multiple environments
- Building production-grade face recognition systems
- Implementing computer vision AI solutions that reduced security incidents by 30%

I have attached my resume for your review. I would appreciate the opportunity to discuss how my skills and experience could contribute to {company}'s success.

Thank you for considering my application. I look forward to the possibility of working with your team.

Best regards,
Venkat Kumar Meda
+91 9618367367
venkatkumarmeda23@gmail.com
https://www.linkedin.com/in/venkat-kumar-meda-8710b5266/
    """
    return email_body

def send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path=None, delay=2):
    """Send an email with optional attachment"""
    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Attach email body
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach resume if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as file:
                part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)
        
        # Create SMTP session
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        # Add delay to avoid triggering spam filters
        time.sleep(delay)
        return True
    
    except Exception as e:
        logging.error(f"Failed to send email to {recipient_email}: {str(e)}")
        return False

def send_emails_task(contacts_file, resume_file, email_settings):
    """Background task to send emails"""
    global sending_status
    
    try:
        # Read contacts file
        if contacts_file.endswith('.csv'):
            contacts_df = pd.read_csv(contacts_file)
        else:  # Excel file
            contacts_df = pd.read_excel(contacts_file)
            
        # Set up sending status
        total_contacts = len(contacts_df)
        sending_status['is_sending'] = True
        sending_status['total'] = total_contacts
        sending_status['sent'] = 0
        sending_status['failed'] = 0
        sending_status['progress'] = 0
        
        # Process in batches
        batch_size = int(email_settings.get('batch_size', 50))
        delay_between_emails = int(email_settings.get('delay_between_emails', 3))
        delay_between_batches = int(email_settings.get('delay_between_batches', 15)) * 60  # Convert to seconds
        
        for i in range(0, total_contacts, batch_size):
            batch = contacts_df.iloc[i:min(i+batch_size, total_contacts)]
            
            # Process each contact in the batch
            for _, row in batch.iterrows():
                try:
                    name = row['Name']
                    email = row['Email']
                    title = row.get('Title', '')  # Use empty string if Title column doesn't exist
                    company = row['Company']
                    
                    sending_status['current_recipient'] = f"{name} ({email})"
                    
                    # Create personalized email
                    body = create_email_body(name, title, company)
                    
                    # Send email
                    if send_email(
                        email_settings.get('sender_email'),
                        email_settings.get('app_password'),
                        email,
                        email_settings.get('email_subject', 'Job Application - Computer Vision Engineer'),
                        body,
                        resume_file,
                        delay_between_emails
                    ):
                        sending_status['sent'] += 1
                        logging.info(f"Email sent successfully to {name} ({email})")
                    else:
                        sending_status['failed'] += 1
                        logging.error(f"Failed to send email to {name} ({email})")
                
                except Exception as e:
                    sending_status['failed'] += 1
                    logging.error(f"Error processing contact: {str(e)}")
                
                # Update progress
                sent_plus_failed = sending_status['sent'] + sending_status['failed']
                sending_status['progress'] = int((sent_plus_failed / total_contacts) * 100)
            
            # Delay between batches (except for the last batch)
            if i + batch_size < total_contacts:
                logging.info(f"Batch completed. Waiting for {delay_between_batches/60} minutes before the next batch...")
                time.sleep(delay_between_batches)
        
        # All emails have been processed
        sending_status['is_sending'] = False
        logging.info(f"Email sending completed. Success: {sending_status['sent']}, Failed: {sending_status['failed']}")
    
    except Exception as e:
        logging.error(f"Error in send_emails_task: {str(e)}")
        sending_status['is_sending'] = False

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'contacts_file' not in request.files or 'resume_file' not in request.files:
        return jsonify({'error': 'Missing files'}), 400
    
    contacts_file = request.files['contacts_file']
    resume_file = request.files['resume_file']
    
    if contacts_file.filename == '' or resume_file.filename == '':
        return jsonify({'error': 'No selected files'}), 400
    
    # Save contacts file
    contacts_filename = secure_filename(contacts_file.filename)
    contacts_path = os.path.join(app.config['UPLOAD_FOLDER'], contacts_filename)
    contacts_file.save(contacts_path)
    
    # Save resume file
    resume_filename = secure_filename(resume_file.filename)
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
    resume_file.save(resume_path)
    
    return jsonify({
        'contacts_file': contacts_path,
        'resume_file': resume_path
    })

@app.route('/analyze', methods=['POST'])
def analyze_file():
    """Analyze the contacts file and return summary info"""
    try:
        contacts_path = request.json.get('contacts_file')
        
        # Read the file based on extension
        if contacts_path.endswith('.csv'):
            df = pd.read_csv(contacts_path)
        else:  # Excel file
            df = pd.read_excel(contacts_path)
        
        # Ensure required columns exist
        required_columns = ['Name', 'Email', 'Company']
        missing_columns = []
        for col in required_columns:
            if col not in df.columns:
                missing_columns.append(col)
        
        # Fill NA values to prevent JSON serialization issues
        df = df.fillna('')
        
        # Get file info
        total_contacts = len(df)
        columns = list(df.columns)
        
        # Get sample data (first 5 rows)
        sample_data = df.head(5).to_dict('records')
        
        # Count unique companies
        unique_companies = df['Company'].nunique() if 'Company' in columns else 0
        
        return jsonify({
            'total_contacts': total_contacts,
            'columns': columns,
            'missing_columns': missing_columns,
            'sample_data': sample_data,
            'unique_companies': unique_companies
        })
    
    except Exception as e:
        print(f"Error analyzing file: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/send', methods=['POST'])
def send_emails():
    global sending_status
    
    # Check if already sending
    if sending_status['is_sending']:
        return jsonify({'error': 'Already sending emails'}), 400
    
    # Get data from request
    data = request.json
    contacts_file = data.get('contacts_file')
    resume_file = data.get('resume_file')
    email_settings = data.get('email_settings')
    
    # Validate required data
    if not contacts_file or not resume_file or not email_settings:
        return jsonify({'error': 'Missing required data'}), 400
    
    if not os.path.exists(contacts_file) or not os.path.exists(resume_file):
        return jsonify({'error': 'Files not found'}), 400
    
    required_settings = ['sender_email', 'app_password', 'email_subject', 'batch_size', 
                        'delay_between_emails', 'delay_between_batches']
    for setting in required_settings:
        if setting not in email_settings:
            return jsonify({'error': f'Missing required setting: {setting}'}), 400
    
    # Start email sending in a background thread
    thread = threading.Thread(
        target=send_emails_task, 
        args=(contacts_file, resume_file, email_settings)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'started', 'message': 'Email sending has started'})

@app.route('/status', methods=['GET'])
def get_status():
    """Get the current status of email sending"""
    return jsonify(sending_status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)