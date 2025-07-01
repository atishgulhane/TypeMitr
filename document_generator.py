import os
from openai import OpenAI
import logging

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_document_content(document_type, language, tone, sender_name, recipient_name, 
                            purpose, reason=None, date_from=None, date_to=None):
    """
    Generate document content using OpenAI GPT-4o
    """
    try:
        # Build the prompt based on inputs
        language_names = {
            'english': 'English',
            'hindi': 'Hindi',
            'marathi': 'Marathi'
        }
        
        tone_descriptions = {
            'formal': 'very formal and professional',
            'semi_formal': 'semi-formal and respectful',
            'friendly': 'friendly but professional'
        }
        
        prompt = f"""
Generate a complete {document_type} in {language_names.get(language, 'English')} language.

Document Details:
- Type: {document_type}
- Language: {language_names.get(language, 'English')}
- Tone: {tone_descriptions.get(tone, 'formal')}
- Sender: {sender_name}
- Recipient: {recipient_name}
- Purpose: {purpose}
"""
        
        if reason:
            prompt += f"- Reason/Additional Details: {reason}\n"
        
        if date_from:
            prompt += f"- Start Date: {date_from}\n"
        
        if date_to:
            prompt += f"- End Date: {date_to}\n"
        
        prompt += f"""
Requirements:
1. Create a properly formatted {document_type} with appropriate headers, salutations, and closings
2. Use {tone_descriptions.get(tone, 'formal')} tone throughout
3. Include all necessary details based on the purpose provided
4. Follow standard format for this type of document
5. Make it professional and complete
6. Include proper date formatting and addressing
7. If writing in Hindi or Marathi, use proper script and formal language conventions
8. End with appropriate closing and signature line

Generate the complete document content now:
"""
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert document writer who creates professional letters, applications, and official documents in multiple languages. Always generate complete, properly formatted documents."
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        generated_content = response.choices[0].message.content.strip()
        
        logging.info(f"Successfully generated {document_type} for {sender_name}")
        return generated_content
        
    except Exception as e:
        logging.error(f"Error generating document content: {str(e)}")
        raise Exception(f"Failed to generate document: {str(e)}")
