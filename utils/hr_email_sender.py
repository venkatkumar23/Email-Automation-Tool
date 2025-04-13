import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import time
from tqdm import tqdm
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_sender.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def read_contacts(file_path):
    """Read contact information from Excel or CSV file"""
    if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Please use .xlsx, .xls, or .csv")

def create_email_body(name, title, company):
    """Create a personalized email body"""
    email_body = f"""
Dear {name},

I hope this email finds you well. My name is Venkat Kumar Meda, a Computer Vision Engineer with expertise in AI-driven surveillance solutions and Kubernetes-based deployments.

I noticed that {company} is at the forefront of innovation, and I'm particularly interested in bringing my technical skills to your organization. I believe you might be the right person to connect with regarding potential opportunities at {company}.

My experience includes:
• Developing versatile Kubernetes platforms across multiple environments
• Building production-grade face recognition systems
• Implementing computer vision AI solutions that reduced security incidents by 30%

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

def main():
    """Main function to execute the email sending process"""
    print("===== HR Email Automation Tool =====")
    print("This tool will help you send personalized emails to HR contacts")
    
    # Get input from user
    print("\nPlease provide the following information:")
    contact_file = input("Enter the path to your contacts file (.xlsx, .xls, or .csv): ")
    resume_path = input("Enter the path to your resume file (PDF recommended): ")
    sender_email = input("Enter your email (Gmail recommended): ")
    sender_password = input("Enter your app password (not your regular password): ")
    email_subject = input("Enter email subject (default: 'Job Application - Computer Vision Engineer'): ") or "Job Application - Computer Vision Engineer"
    
    # Optional parameters
    print("\nAdvanced settings (press Enter for defaults):")
    batch_size = int(input("Enter batch size (default: 50): ") or "50")
    delay_between_emails = int(input("Enter delay between emails in seconds (default: 3): ") or "3")
    delay_between_batches = int(input("Enter delay between batches in minutes (default: 15): ") or "15")
    
    # Read contacts
    logging.info(f"Reading contacts from {contact_file}")
    try:
        contacts_df = read_contacts(contact_file)
    except Exception as e:
        logging.error(f"Error reading contacts file: {str(e)}")
        print(f"Error reading contacts file: {str(e)}")
        return
    
    # Confirm with user
    total_contacts = len(contacts_df)
    print(f"\nYou are about to send {total_contacts} emails with the following settings:")
    print(f"- From: {sender_email}")
    print(f"- Subject: {email_subject}")
    print(f"- Resume: {resume_path}")
    print(f"- Batch size: {batch_size}")
    print(f"- Delay between emails: {delay_between_emails} seconds")
    print(f"- Delay between batches: {delay_between_batches} minutes")
    
    confirm = input("\nDo you want to proceed? (yes/no): ").lower()
    if confirm != 'yes':
        print("Operation cancelled.")
        return
    
    # Process in batches
    successful = 0
    failed = 0
    
    for i in range(0, total_contacts, batch_size):
        batch = contacts_df.iloc[i:i+batch_size]
        
        logging.info(f"Processing batch {i//batch_size + 1}/{(total_contacts + batch_size - 1)//batch_size}")
        
        # Process each contact in the batch
        for _, row in tqdm(batch.iterrows(), total=len(batch), desc="Sending emails"):
            try:
                name = row['Name']
                email = row['Email']
                title = row['Title']
                company = row['Company']
                
                # Create personalized email
                body = create_email_body(name, title, company)
                
                # Send email
                if send_email(sender_email, sender_password, email, email_subject, body, resume_path, delay_between_emails):
                    successful += 1
                    logging.info(f"Email sent successfully to {name} ({email})")
                else:
                    failed += 1
            
            except Exception as e:
                failed += 1
                logging.error(f"Error processing contact: {str(e)}")
        
        # Delay between batches (except for the last batch)
        if i + batch_size < total_contacts:
            logging.info(f"Batch completed. Waiting for {delay_between_batches} minutes before the next batch...")
            time.sleep(delay_between_batches * 60)
    
    # Final report
    logging.info(f"Email sending completed. Success: {successful}, Failed: {failed}")
    print(f"\nEmail sending completed. Success: {successful}, Failed: {failed}")
    print(f"Check 'email_sender.log' for detailed information.")

if __name__ == "__main__":
    main()