from fastapi import FastAPI
from pydantic import BaseModel
from masking import mask_email
from model import classify_email_subject, extract_subject
import json

app = FastAPI()

class EmailInput(BaseModel):
    input_email_body: str

@app.post("/classify")
def classify(input: EmailInput):
    original_email = input.input_email_body
    subject = extract_subject(original_email)
    masked_email, entities = mask_email(original_email)
    category = classify_email_subject(subject)

    return {
        "input_email_body": original_email,
        "list_of_masked_entities": entities,
        "masked_email": masked_email,
        "category_of_the_email": category
    }
