def create_standard_email(name, company):
    """
    Create a standard personalized email body
    
    Parameters:
    - name: Recipient's name
    - company: Recipient's company name
    
    Returns:
    - Formatted email body as a string
    """
    email_body = f"""
Dear {name},

I hope this email finds you well. My name is Venkat Kumar Meda, a Computer Vision Engineer with expertise in AI-driven surveillance solutions and Kubernetes-based deployments.

I noticed that {company} is at the forefront of innovation, and I'm particularly interested in bringing my technical skills to your organization. I believe you might be the right person to connect with regarding potential opportunities at {company}.

My experience includes:
• Developing versatile Kubernetes platforms across multiple environments
• Building production-grade face recognition systems with RETINAFACE and INSIGHTFACE
• Implementing computer vision AI solutions that reduced security incidents by 30%
• Optimizing face recognition latency from 8 seconds to 1 second in real-time environments

I have attached my resume for your review. I would appreciate the opportunity to discuss how my skills in computer vision, cloud technologies, and AI could contribute to {company}'s success.

Thank you for considering my application. I look forward to the possibility of working with your team.

Best regards,
Venkat Kumar Meda
+91 9618367367
venkatkumarmeda23@gmail.com
LinkedIn: https://www.linkedin.com/in/venkat-kumar-meda-8710b5266/
GitHub: https://github.com/venkatkumar23
    """
    return email_body


def create_technical_email(name, company):
    """
    A more technically-focused email template
    
    Parameters:
    - name: Recipient's name
    - company: Recipient's company name
    
    Returns:
    - Formatted email body as a string
    """
    email_body = f"""
Dear {name},

I hope this email finds you well. I'm Venkat Kumar Meda, a Computer Vision Engineer specializing in Kubernetes-based deployments and AI-driven surveillance solutions.

I've been following {company}'s innovative work, and I'm reaching out to explore potential opportunities to contribute my technical expertise to your team. I believe you might be interested in my experience with:

• Kubernetes orchestration across on-premises, cloud, and hybrid environments
• Computer vision systems using DeepSORT, YOLO, InsightFace, and RetinaFace
• Real-time video analytics and face recognition systems with 95% accuracy
• Cloud-native technologies (AWS, Docker) and ReactJS dashboards

Most recently, I've delivered a production-grade face recognition system integrating model conversion (ONNX/OpenVINO/TensorRT), Triton Inference Server, and Milvus vector database, reducing face recognition latency from 8 seconds to 1 second.

I've attached my resume with more details about my projects and skills. I would welcome the opportunity to discuss how my technical background could add value to {company}.

Thank you for your consideration.

Best regards,
Venkat Kumar Meda
+91 9618367367
venkatkumarmeda23@gmail.com
LinkedIn: https://www.linkedin.com/in/venkat-kumar-meda/
GitHub: https://github.com/venkatkumar23
    """
    return email_body


def create_followup_email(name, company, days_since_contact=7):
    """
    Create a follow-up email template
    
    Parameters:
    - name: Recipient's name
    - company: Recipient's company name
    - days_since_contact: Days since first contact
    
    Returns:
    - Formatted email body as a string
    """
    email_body = f"""
Dear {name},

I hope this email finds you well. I wanted to follow up on my previous email regarding potential opportunities at {company}.

I understand that you must be busy, but I'm still very interested in discussing how my expertise in computer vision and Kubernetes could benefit your team. If the timing wasn't right before, I'd be happy to reconnect at your convenience.

For your reference, I've attached my resume again. My experience includes deploying production-grade face recognition systems that reduced latency from 8 seconds to 1 second, and implementing computer vision solutions that improved monitoring efficiency by 20%.

Please let me know if you'd like to discuss further or if you need any additional information from me.

Thank you for your consideration.

Best regards,
Venkat Kumar Meda
+91 9618367367
venkatkumarmeda23@gmail.com
LinkedIn: https://www.linkedin.com/in/venkat-kumar-meda/
    """
    return email_body


# Import this file in hr_email_sender.py to use these templates
# Example usage:
# from email_templates import create_standard_email, create_technical_email, create_followup_email
#
# # Then in your code:
# body = create_standard_email(name, company)
#
# # Or for a more technical audience:
# body = create_technical_email(name, company)
#
# # For follow-ups:
# body = create_followup_email(name, company, days_since_contact=10)