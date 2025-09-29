def validate_form(age, date_of_visit, gender, responses):
    if not age and not date_of_visit and not gender and not any(responses.values()):
        return "Please fill out the form before submitting."
    if not age or not age.isdigit():
        return "Please enter a valid numeric age."
    if not date_of_visit:
        return "Please select a date of visit."
    if not gender:
        return "Please select a gender."
    if not all(responses.values()):
        return "Please answer all survey questions."
    return None
