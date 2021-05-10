from zeep import Client
from IPython.display import clear_output
import sys
import time
import pandas as pd



def validate_vat_id_csv(file, start, end):
    df = pd.read_csv(file)
    df.columns=['VATID']
    try:
        ids = list(df.VATID)
    except:
        print("list finished")
    print(f"{len(ids)} to validate")
    print("Beginning validation")
    time.sleep(2)
    VIES_URL = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
    client = Client(VIES_URL)
    my_dict = {}
    
    i=0
    for id in ids:
        country_suffix = id[:2]
        number = id[2:]
        try:
            res = client.service.checkVat(countryCode=country_suffix, vatNumber=number)
            my_dict[id] = [res.countryCode, res.vatNumber, res.requestDate, res.valid, res.name, res.address] 
        except:
            print("trying to reconnect")
            time.sleep(60)
            VIES_URL = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
            client = Client(VIES_URL)
            
            
            
        sys.stdout.write("\033[F") #back to previous line 
        sys.stdout.write("\033[K") #clear line
        clear_output(wait=True)
        i+=1
        print(f"{round((i*100)/len(ids),2)}% complete; {i} numbers validated")
      
    
    
    
    new_df = pd.DataFrame.from_dict(my_dict, orient='index')
    new_df = new_df.reset_index()
    new_df.columns = ['VATID', 'Country', 'Number','Date','Valid', 'Name', 'Address']
    
    sys.stdout.write("\033[F") #back to previous line 
    sys.stdout.write("\033[K") #clear line
    print(f"{len(ids)} IDs successfully validated")
    
    return new_df

# file = str(input("file name?"))
file = 'IDS.csv'
start = 0
end = 100000

df = validate_vat_id_csv(file, start, end)

df.to_csv(f"Validation Results.csv")


