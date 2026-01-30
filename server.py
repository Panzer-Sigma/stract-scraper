import requests
import csv
from flask import Flask
import io
import json

EXTERNAL_API_URL = 'https://sidebar.stract.to/api'
headers = {
    'Authorization': f'Bearer SelecaoStract2026',
    'Content-Type': 'application/json'
}

# -------- funções de consumo e parsing --------
#verificação simples para campos do GET /geral
def is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)

#scraping de plataformas
def get_platforms(plataforma):
    response = requests.get(f"{EXTERNAL_API_URL}/platforms", headers=headers)
    available_plats = response.json()
    found = False
    platfound = None
    for plat in available_plats["platforms"]:
        if plat["value"] == plataforma:
            found = True
            platfound = plat
            break
    return found, available_plats["platforms"]

#scraping de campos por plataforma
def get_fields(plataforma):
    current_page = 1
    values = ["platform", "account_name"]
    texts = ["Platform","Account Name"]

    while True:
        response_field = requests.get(f"{EXTERNAL_API_URL}/fields?platform="+ str(plataforma) + "&page="+str(current_page), headers=headers)
        available_fields = response_field.json()
        for field in available_fields["fields"]:
            values.append(field["value"])
            texts.append(field["text"])
        try:
            if current_page >= int(available_fields["pagination"]["total"]):
                break
        except:
            break
        current_page += 1

    fieldheaders = ",".join(texts)
    fields = ",".join(values)
    return fieldheaders, fields

#scraping de contas por plataforma
def get_accounts(plataforma):
    current_page = 1
    accounts = []

    while True:
        response_account = requests.get(f"{EXTERNAL_API_URL}/accounts?platform="+ str(plataforma) + "&page="+str(current_page), headers=headers)
        available_accounts = response_account.json()
        
        for account in available_accounts["accounts"]:
            accounts.append(account)
        try:
            if current_page >= int(available_accounts["pagination"]["total"]):
                break
        except:
            break
        current_page += 1
    return accounts

def get_insights(plataforma, account_list, fields):
    insight_list = []
    for account in account_list:
        account_id = account["id"]
        account_token = account["token"]
        current_page = 1
        while True:
            response_insight = requests.get(f"{EXTERNAL_API_URL}/insights?platform="
                                            + str(plataforma) 
                                            + "&account=" 
                                            + str(account_id) 
                                            + "&token=" 
                                            + str(account_token) 
                                            + "&fields=" 
                                            + str(fields)
                                            + "&page="+str(current_page), headers=headers)
            insights = response_insight.json()


            for i in insights["insights"]:
                try: 
                    if "cpc" != i.keys():
                        i["cpc"] = i["spend"] / i["clicks"]
                #Não encontrei Spend com valor pra dividir com clicks, então:
                except:
                    i["cpc"] = 0
                    pass

                account_name = account["name"]
                i["account_name"] = account_name
                insight_list.append(i)

            try:
                if current_page >= int(insights["pagination"]["total"]):
                    break
            except:
                break
            current_page += 1
    return insight_list

def get_insights_resumo(plataforma, account_list, fields):
    insight_list = []
    for account in account_list:
        account_id = account["id"]
        account_token = account["token"]
        current_page = 1
        insight = {}

        while True: 
            response_insight = requests.get(f"{EXTERNAL_API_URL}/insights?platform="
                                            + str(plataforma) 
                                            + "&account=" 
                                            + str(account_id) 
                                            + "&token=" 
                                            + str(account_token) 
                                            + "&fields=" 
                                            + str(fields)
                                            + "&page="+str(current_page), headers=headers)
            insights = response_insight.json()
            for i in insights["insights"]:
                try: 
                    if "cpc" != i.keys():
                        i["cpc"] = i["spend"] / i["clicks"]
                
                except:
                    #Não estava disponível o valor de "spend" pra dividir com clicks e tirar o CPC para ga4 e pra o tiktok, então:
                    i["cpc"] = 0
                    pass

                for key, value in i.items():
                    if not is_number(value):
                        continue
                    if key not in insight:
                        insight[key] = value
                    else:
                        insight[key] += value               
            try:
                if current_page >= int(insights["pagination"]["total"]):
                    break
            except:
                break
            current_page += 1

        if insight != {}:
            account_name = account["name"]
            insight["account_name"] = account_name
            insight_list.append(insight)
    return insight_list

# -------- servidor local e tratamento de retornos requisitados --------

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Guilherme Nunes, thepanzersigma@gmail.com, www.linkedin.com/in/gui-nunes-lopes/', 200

@app.route('/<plataforma>', methods=['GET'])
def get_plataforma(plataforma):
    # #checagem de plataforma
    found, platforms = get_platforms(plataforma)
    if not found:
        return "", 404

    fieldheaders, fields = get_fields(plataforma)
    account_list = get_accounts(plataforma)
    insightsList = get_insights(plataforma, account_list, fields)

    csv_buffer = io.StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=fields.split(","),extrasaction='ignore') 

    header_map = dict(zip(fields.split(","),fieldheaders.split(","))) 
    csv_writer.writerow(header_map)

    for row in insightsList:
        row["platform"] = plataforma
        csv_writer.writerow(row)
    return csv_buffer.getvalue(), 200   


@app.route('/<plataforma>/resumo', methods=['GET'])
def get_plataforma_resumo(plataforma):
    # #checagem de plataforma
    found, platforms = get_platforms(plataforma)
    if not found:
        return "", 404

    fieldheaders, fields = get_fields(plataforma)
    account_list = get_accounts(plataforma)
    insightsList = get_insights_resumo(plataforma, account_list, fields)


    csv_buffer = io.StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=fields.split(","),extrasaction='ignore') 

    header_map = dict(zip(fields.split(","),fieldheaders.split(","))) 
    csv_writer.writerow(header_map)

    for row in insightsList:
        row["platform"] = plataforma
        csv_writer.writerow(row)
    return csv_buffer.getvalue(), 200   


@app.route('/geral', methods=['GET'])
def get_geral():
    insights_total = []
    totalfields_headers = []
    totalfields = []
    found, plats = get_platforms("")
    for platform in plats:
        plat = platform["value"]
        fieldheaders, fields = get_fields(plat)
        account_list = get_accounts(plat)
        insights_plat = get_insights(plat, account_list, fields)

        #faz merge da lista de cada plataforma
        for row in insights_plat:
            row["platform"] = plat

        insights_total += insights_plat 
       
        #faz merge dos fields (sem duplicados)
        list1 = totalfields
        list2 = fields.split(',')
        totalfields = list1 + [item for item in list2 if item not in list1]
        
        #faz merge dos fields (sem duplicados)
        list1 = totalfields_headers
        list2 = fieldheaders.split(',')
        totalfields_headers = list1 + [item for item in list2 if item not in list1]

    csv_buffer = io.StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=totalfields,extrasaction='ignore') 
    header_map = dict(zip(totalfields,totalfields_headers)) 
    csv_writer.writerow(header_map)

    for row in insights_total:
        csv_writer.writerow(row)

    return csv_buffer.getvalue(), 200   

#---
@app.route('/geral/resumo', methods=['GET'])
def get_geral_resumo():
    insights_total = []
    totalfields_headers = []
    totalfields = []
    found, plats = get_platforms("")
    for platform in plats:
        plat = platform["value"]
        fieldheaders, fields = get_fields(plat)
        account_list = get_accounts(plat)
        
        geral_i_plat = {}
        insights_plat = get_insights_resumo(plat, account_list, fields)

        for i_plat in insights_plat:
            for key, value in i_plat.items():
                if not is_number(value):
                    continue
                if key not in geral_i_plat:
                    geral_i_plat[key] = value
                else:
                    geral_i_plat[key] += value

        geral_i_plat["platform"] = plat

        insights_total.append(geral_i_plat)
      
        #faz merge dos fields (sem duplicatas)
        list1 = totalfields
        list2 = fields.split(',')
        totalfields = list1 + [item for item in list2 if item not in list1]
    
        list1 = totalfields_headers
        list2 = fieldheaders.split(',')
        totalfields_headers = list1 + [item for item in list2 if item not in list1]

    csv_buffer = io.StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=totalfields,extrasaction='ignore') 
    header_map = dict(zip(totalfields,totalfields_headers)) 
    csv_writer.writerow(header_map)

    for row in insights_total:
        csv_writer.writerow(row)

    return csv_buffer.getvalue(), 200   

if __name__ == '__main__':
    app.run(debug=True, port=5000)