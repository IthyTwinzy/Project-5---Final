# This function works on the basis of accessing data from a local JSON.

jsonExample = {"Email": ["hello@hi.com","goodbye@bye.com"], "Sender": ["hello","bye"], "Date": ["04-01-2026","04-02-2026"]}

def returnFunc(type, jsonObj): # Specify what type of data you want to retrieve
    
    match type:
        # AZURE DATA
        case "Email":
            print(jsonExample["Email"])
        case "Sender":
            print(jsonExample["Sender"])
        case "Date":
            print(jsonExample["Date"])
        # API DATA
        


returnFunc("Email")