from pypdf import PdfReader as pdf
import requests as req

reader = pdf(r'C:\Users\Tarun Akash\Desktop\ML-Ops1.pdf')
page = reader.pages[0]
texted = page.extract_text()

file_path = "newtext.txt"
with open(file_path, 'w') as file:
    file.write(texted)

def langtrans(text, source_lang, target_lang):
    url = "https://api.mymemory.translated.net/get"
    
    params = {
        "q": text,
        "langpair": f"{source_lang}|{target_lang}"
    }
    
    response = req.get(url, params=params)
    
    if response.status_code == 200:
        translated_text = response.json()['responseData']['translatedText']
        return translated_text
    else:
        print(f"Error: {response.status_code}")
        return None

text = texted
translated = langtrans(text, "en", "de")
if translated:
    print(f"Translated text: {translated}")
else:
    print("Failed to translate.")


file_path = "newtranslatedtext.txt"
with open(file_path, 'w') as file:
    file.write(translated)
