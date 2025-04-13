# Email Automation Tool

An easy-to-use web application for sending personalized job application emails to HR contacts at scale.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## 🚀 Features

- **User-friendly web interface** - Simple three-step process
- **Batch processing** - Avoid triggering spam filters
- **Real-time progress tracking** - Monitor email sending status
- **CSV and Excel support** - Import your HR contacts
- **Customizable templates** - Personalize your outreach

## 📋 Requirements

- Python 3.6+
- Flask
- Gmail account with App Password enabled

## 🔧 Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/Email-Automation-Tool.git
   cd Email-Automation-Tool
   ```

2. Create and activate a virtual environment
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Usage

1. Start the application
   ```bash
   python app.py
   ```

2. Navigate to `http://localhost:5000` in your browser

3. Follow the three-step process:
   - **Upload Files**: Add your HR contacts list (CSV/Excel) and resume (PDF)
   - **Email Settings**: Configure Gmail credentials and batch settings
   - **Review & Send**: Check your settings and start sending

## 📁 Project Structure

```
email_tool/
├── app.py                 # Main Flask application
├── static/                # Static files
│   ├── css/
│   │   └── styles.css     # Custom CSS styles
│   └── js/
│       └── main.js        # Client-side functionality
├── templates/             # HTML templates
│   └── index.html         # Main page with all steps
├── uploads/               # Folder for uploaded files
├── utils/                 # Helper functions
│   ├── __init__.py        # Make utils a proper package
│   ├── email_template.py  # Email template functionality
│   └── hr_email_sender.py # Email sending functionality
```

## 📧 Gmail App Password Setup

To use Gmail for sending emails:

1. Go to your Google Account settings
2. Navigate to Security > 2-Step Verification
3. Scroll down to "App passwords"
4. Select "Mail" as the app and "Other" as the device
5. Generate the password and use it in the application

## 🛠️ Troubleshooting

- **Flask app won't start**: Make sure dependencies are installed and virtual environment is active
- **Email sending failures**: Check Gmail app password and Less Secure Apps settings
- **File upload issues**: Ensure uploads folder has write permissions
- **JSON parsing errors**: Verify CSV file formatting (Name, Email, and Company columns)

## 🔮 Future Enhancements

- Email template management
- Contact list organization
- Email tracking and analytics
- Scheduled sending
- Multi-service support



## 👨‍💻 Author

Venkat Kumar Meda - [GitHub](https://github.com/venkatkumar23)

## 🙏 Acknowledgments

- Flask for the web framework
- Bootstrap for UI components
- Open source community for inspiration

---

<p align="center">Made with ❤️ for job seekers in tech</p>
