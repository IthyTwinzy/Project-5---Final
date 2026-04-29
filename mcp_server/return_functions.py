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

''' Notes
We're saving the data from AZURE; threat level, email details
REST API data: Various aspects which are flagged

User can ask:
- List of data (emails, sender, date etc...)
- Specific data (EX. user prompts with email, gets sender & date)
- Prompts server? (Does the user send the data thru the MCP server to Azure?)
'''