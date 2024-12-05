from pypdf import PdfReader as pdf
import requests as req

reader = pdf(r'C:\Users\Tarun Akash\Desktop\ML-Ops.pdf')
page = reader.pages[0]
texted = page.extract_text()
print(texted)

file_path = "newtext.txt"
with open(file_path, 'w') as file:
    file.write(texted)

def langtrans(text, source_lang, target_lang):
    url = 'https://libretranslate.com/translate'

    data = {
        'q': text,                
        'source': source_lang,    
        'target': target_lang,    
        'format': 'text'          
    }

    response = req.post(url, data=data)

    if response.status_code == 200:
        translated_text = response.json()['translatedText'] 
        return translated_text
    else:
        print("Error:", response.status_code) 
        return None

tt = langtrans(texted, 'en', 'de')
if tt:
    print(tt)
else:
    print("failed")
