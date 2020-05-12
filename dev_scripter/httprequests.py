import requests
import os
import json

class PayLoad(object):
    SLEEP_TIME=0.5
    def __init__(self,token,endpoint):
        try:
            if token == "" or endpoint == "":
                print('Parametros Não carregados na construção do payload.')
            else:
                self.token=token
                self.endpoint = endpoint
        except Exception as e:
            print("Fail Create Constructor Payload  " ,  e)
    

    @staticmethod
    def change_sleep(sleep_time):
        SLEEP_TIME=sleep_time
    
    @staticmethod
    def check_sleep():
        print(SLEEP_TIME)
    
    @classmethod
    def check_path():
        result = os.environ.get('URL_ENDPOINT_POST','DONT SETTER')
        if result != 'DONT SETTER':
            return True
        return False
    
    """
     -> Cria um payload para o envio dos dados elegiveis. 
     -> O carregamento da url endpoint e o token de acesso é fornecido na construção do payLoad
    """
    def create_payload(self):
        token_acc =  "Token  "
        token_acc += self.token

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": token_acc
        }

        return self.headers

    def sender_payload_antibiotic(self,antibioticos,headers):
        url  = self.endpoint
        header = headers
        cont = 0
        for i in antibioticos:
            med = i[1]
            prod = i[2]
            payload = {
                "ean1": med.ean1,
                "icon": "",
                "is_antibiotic": med.is_antibiotic,
                "category": 'Genéricos',
                "name":med.product_name,
                "brand":prod.brand,
                "description":prod.description,
                "is_drug":med.is_drug,
                "active_principle":prod.active_principle,
                "federal_code": med.register,
                "display":med.apresentation,
                "atc":med.classe,
                "status_type":med.type_product,
                "band_color": med.tarja,
                "can_sell":med.can_sell,
                "pmc_20":med.pmc,
                "barcode2":med.ean2
            }
            r = requests.post(url,data=json.dumps(payload), headers=header)
            time.sleep(SLEEP_TIME)
            cont+=1

        print("Enviando  {cont}  de  {q}".format(cont=cont,q=len(antibioticos)))

        if cont == len(antibioticos):
            print('Antibioticos Enviados. ')
            return True
        








