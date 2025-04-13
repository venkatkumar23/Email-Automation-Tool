document.addEventListener('DOMContentLoaded', function() {
    // Variables to store file paths and settings
    let contactsFilePath = '';
    let resumeFilePath = '';
    let fileData = {
        contactsCount: 0,
        contactsName: '',
        resumeName: ''
    };
    
    // Step navigation elements
    const step1Element = document.getElementById('step1');
    const step2Element = document.getElementById('step2');
    const step3Element = document.getElementById('step3');
    const step1Tab = document.getElementById('step1-tab');
    const step2Tab = document.getElementById('step2-tab');
    const step3Tab = document.getElementById('step3-tab');
    
    // Form elements
    const uploadForm = document.getElementById('upload-form');
    const settingsForm = document.getElementById('settings-form');
    const backToUploadBtn = document.getElementById('back-to-upload-btn');
    const backToSettingsBtn = document.getElementById('back-to-settings-btn');
    const sendEmailsBtn = document.getElementById('send-emails-btn');
    
    // Progress elements
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar');
    const sentCount = document.getElementById('sent-count');
    const failedCount = document.getElementById('failed-count');
    const totalCount = document.getElementById('total-count');
    const sendingMessage = document.getElementById('sending-message');
    const completeMessage = document.getElementById('complete-message');

    // Step 1: Upload Form
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const contactsFileInput = document.getElementById('contacts-file');
        const resumeFileInput = document.getElementById('resume-file');
        
        if (!contactsFileInput.files[0] || !resumeFileInput.files[0]) {
            alert('Please select both contacts file and resume file.');
            return;
        }
        
        // Display loading state
        document.getElementById('upload-btn').disabled = true;
        document.getElementById('upload-btn').innerHTML = 'Uploading files...';
        
        // Create form data
        const formData = new FormData();
        formData.append('contacts_file', contactsFileInput.files[0]);
        formData.append('resume_file', resumeFileInput.files[0]);
        
        try {
            // Upload files
            const uploadResponse = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            if (!uploadResponse.ok) {
                throw new Error('Failed to upload files');
            }
            
            const uploadData = await uploadResponse.json();
            contactsFilePath = uploadData.contacts_file;
            resumeFilePath = uploadData.resume_file;
            
            // Analyze the contacts file
            const analyzeResponse = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    contacts_file: contactsFilePath
                })
            });
            
            if (!analyzeResponse.ok) {
                throw new Error('Failed to analyze contacts file');
            }
            
            const analyzeData = await analyzeResponse.json();
            
            // Check if required columns exist
            if (analyzeData.missing_columns.length > 0) {
                throw new Error(`Missing required columns: ${analyzeData.missing_columns.join(', ')}`);
            }
            
            // Store file data
            fileData.contactsCount = analyzeData.total_contacts;
            fileData.contactsName = contactsFileInput.files[0].name;
            fileData.resumeName = resumeFileInput.files[0].name;
            
            // Navigate to step 2
            goToStep(2);
        } catch (error) {
            alert('Error: ' + error.message);
            console.error(error);
        } finally {
            // Reset loading state
            document.getElementById('upload-btn').disabled = false;
            document.getElementById('upload-btn').innerHTML = 'Continue to Email Settings';
        }
    });
    
    // Step 2: Settings Form
    settingsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get all settings
        const senderEmail = document.getElementById('sender-email').value;
        const appPassword = document.getElementById('app-password').value;
        const emailSubject = document.getElementById('email-subject').value;
        const batchSize = document.getElementById('batch-size').value;
        const delayBetweenEmails = document.getElementById('delay-between-emails').value;
        const delayBetweenBatches = document.getElementById('delay-between-batches').value;
        
        // Validate settings
        if (!senderEmail || !appPassword) {
            alert('Please enter your email and app password.');
            return;
        }
        
        // Update review screen
        document.getElementById('review-contacts-file').textContent = fileData.contactsName;
        document.getElementById('review-contacts-count').textContent = `${fileData.contactsCount} contacts`;
        document.getElementById('review-resume-file').textContent = fileData.resumeName;
        document.getElementById('review-sender-email').textContent = senderEmail;
        document.getElementById('review-email-subject').textContent = emailSubject;
        document.getElementById('review-batch-size').textContent = batchSize;
        document.getElementById('review-delay-between-emails').textContent = delayBetweenEmails + ' seconds';
        document.getElementById('review-delay-between-batches').textContent = delayBetweenBatches + ' minutes';
        
        // Navigate to step 3
        goToStep(3);
    });
    
    // Navigation buttons
    backToUploadBtn.addEventListener('click', function() {
        goToStep(1);
    });
    
    backToSettingsBtn.addEventListener('click', function() {
        goToStep(2);
    });
    
    // Send emails
    sendEmailsBtn.addEventListener('click', async function() {
        const senderEmail = document.getElementById('sender-email').value;
        const appPassword = document.getElementById('app-password').value;
        const emailSubject = document.getElementById('email-subject').value;
        const batchSize = document.getElementById('batch-size').value;
        const delayBetweenEmails = document.getElementById('delay-between-emails').value;
        const delayBetweenBatches = document.getElementById('delay-between-batches').value;
        
        // Confirm sending
        if (!confirm(`You are about to send emails to ${fileData.contactsCount} contacts. Continue?`)) {
            return;
        }
        
        // Disable send button
        sendEmailsBtn.disabled = true;
        backToSettingsBtn.disabled = true;
        
        // Show progress
        progressContainer.classList.remove('d-none');
        
        try {
            // Start sending emails
            const response = await fetch('/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    contacts_file: contactsFilePath,
                    resume_file: resumeFilePath,
                    email_settings: {
                        sender_email: senderEmail,
                        app_password: appPassword,
                        email_subject: emailSubject,
                        batch_size: batchSize,
                        delay_between_emails: delayBetweenEmails,
                        delay_between_batches: delayBetweenBatches
                    }
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to start sending emails');
            }
            
            // Set up status polling
            const statusInterval = setInterval(async function() {
                try {
                    const statusResponse = await fetch('/status');
                    const status = await statusResponse.json();
                    
                    // Update progress
                    progressBar.style.width = status.progress + '%';
                    progressBar.textContent = status.progress + '%';
                    progressBar.setAttribute('aria-valuenow', status.progress);
                    
                    sentCount.textContent = status.sent;
                    failedCount.textContent = status.failed;
                    totalCount.textContent = status.total;
                    
                    // Check if sending is complete
                    if (!status.is_sending) {
                        clearInterval(statusInterval);
                        sendingMessage.classList.add('d-none');
                        completeMessage.classList.remove('d-none');
                        
                        // Enable back button
                        backToSettingsBtn.disabled = false;
                    }
                } catch (error) {
                    console.error('Error polling status:', error);
                }
            }, 1000);
            
        } catch (error) {
            alert('Error: ' + error.message);
            console.error(error);
            sendEmailsBtn.disabled = false;
            backToSettingsBtn.disabled = false;
        }
    });
    
    // Helper function to navigate between steps
    function goToStep(step) {
        // Hide all steps
        step1Element.classList.add('d-none');
        step2Element.classList.add('d-none');
        step3Element.classList.add('d-none');
        
        // Reset active state
        step1Tab.classList.remove('active');
        step2Tab.classList.remove('active');
        step3Tab.classList.remove('active');
        step1Tab.querySelector('.nav-link').classList.remove('active');
        step2Tab.querySelector('.nav-link').classList.remove('active');
        step3Tab.querySelector('.nav-link').classList.remove('active');
        
        // Show selected step
        if (step === 1) {
            step1Element.classList.remove('d-none');
            step1Tab.classList.add('active');
            step1Tab.querySelector('.nav-link').classList.add('active');
            step2Tab.classList.remove('completed');
            step3Tab.classList.remove('completed');
        } else if (step === 2) {
            step2Element.classList.remove('d-none');
            step2Tab.classList.add('active');
            step2Tab.querySelector('.nav-link').classList.add('active');
            step1Tab.classList.add('completed');
            step3Tab.classList.remove('completed');
        } else if (step === 3) {
            step3Element.classList.remove('d-none');
            step3Tab.classList.add('active');
            step3Tab.querySelector('.nav-link').classList.add('active');
            step1Tab.classList.add('completed');
            step2Tab.classList.add('completed');
        }
    }
});