#pip install -U spacy
#python -m spacy download en_core_web_sm
import spacy



"""
========
Read me:
=========
Dependicies to install:

pip install -U spacy
python -m spacy download en_core_web_sm

================

METHOD
~~~~~~~~~~~~~~~~~
process_text(userInput)
~~~~~~~~~~~~~~~~~

-Pass string datatype

- Returns the organisation, time_frame, converted days

- E.g 
>>>>>>>process_text('Show me this weeks Apple Inc stock price")

>>>>>>> Apple , week , 5

####Important####

- The purpose of this method is to extract company and time frames.

- Each time frame is represented in days. So 5 weeks is 5 x 5 days = 25 days

- 1 week is 5 days as Sat/Sun do not have stock history

#####Very important#####

To extract information from this function, create a tuple of variables with names
of your choice

E.g:

>>>> myOrganisation , myTimeFrame, myDays = process_text('Show Apple Inc stocks for this week')




"""






nlp = spacy.load("en_core_web_sm")


def get_entity_from_text(userInput):
    date_entity = 5
    organisation_entitiy = "GOOGL"
    doc = nlp(userInput)

    for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)
            if ent.label_ == 'ORG':
                organisation_entitiy = ent.text
            
            if ent.label_ =='DATE':
                date_entity = ent.text
            
            if date_entity == None:
                date_entity = "5 days"
                
            if ent.label_ != 'ORG':
                organisation_entitiy = "orgMissing"


    return  organisation_entitiy, date_entity






def process_date_entity(date):
   
    time_frame = None
    if "days" in date or "day" in date or "today" in date or "todays" in date:
        if date.isdigit() is True:
            converted_days = int(date.split())

        else:
            converted_days = 1

        
        time_frame = "day"

    elif "week" in date or "weeks" in date or "weekly" in date:
        if date.isdigit() is True:
            converted_days = int(date.split()) * 5
        else:
            converted_days = 5

        time_frame = "week"

    elif "month" in date or "months" in date:

        if date.isdigit() is True:
            converted_days = int(date.split()) * 30

        else:
            converted_days = 30

        time_frame = "month"

    elif "year" in date or "years" in date or "yearly" in date:
        if date.isdigit() is True:
            converted_days = int(date.split()) * 365

        else:
            converted_days = 365

        
        time_frame = "year"


    return time_frame,converted_days







#===============================================================
def process_text(userInput):
    organisation, date_entity = get_entity_from_text(userInput)

    time_frame, converted_days = process_date_entity(date_entity)


    return organisation, time_frame , converted_days

#===============================================================  


