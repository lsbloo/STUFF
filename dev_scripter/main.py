from xlstool.xlsreader import get_instance
from models.drug import Drug
from models.product import Product
import time
import requests
from settings_global import URL_ENDPOINT_SENDER
from collections import Counter
import hashlib

dont_settr = 'DONT SETTER'

if URL_ENDPOINT_SENDER == dont_settr:
    print('URL ENDPOINT POST DONT SETTER')
    exit


t1 = time.time()


reader = get_instance()
woorkbooks = reader.create_woorkbooks()

_list_tables_anvisa = reader.gerenate_data_anvisa(woorkbooks)
_list_tables_antibiotics = reader.generate_data_anvisa_ant(woorkbooks)

global md5
global repetidos


md5 = hashlib.md5()

def parseCellString(K, index):
    return str(K[index]).split(":")[1].replace("'","")


def construct_drug(K,antibiotico):
    if antibiotico:
        ean1 = parseCellString(K,3)
        ean2 = parseCellString(K,4)
        restriction = parseCellString(K,9)
        product_name = parseCellString(K,5)
        apresentation = parseCellString(K,6)
        classe = parseCellString(K,7)
        type_product = parseCellString(K,8)
        tarja = parseCellString(K,10)
        register = parseCellString(K,2)
        substance_pharm = parseCellString(K,11)
        can_sell = False
        pmc_20 = str(K[12]).split(":")[0]
        if pmc_20 == "number":
            pmc_20 = str(K[12]).split(":")[1]
        else:
            pmc_20 = 0.0
        
        return Drug(antibiotico,pmc_20,ean1,ean2,restriction,product_name,apresentation,classe,type_product,tarja,register,substance_pharm,can_sell)
    else:
        ean1 = parseCellString(K,3)
        ean2 = parseCellString(K,4)
        restriction = parseCellString(K,9)
        product_name = parseCellString(K,5)
        apresentation = parseCellString(K,6)
        classe = parseCellString(K,7)
        type_product =parseCellString(K,8)
        tarja = parseCellString(K,10)
        if tarja == 'Venda Livre':
            can_sell = True
        else:
            can_sell = False
        register = parseCellString(K,2)
        substance_pharm = parseCellString(K,11)
        pmc_20 = str(K[12]).split(":")[0]
        if pmc_20 == "number":
            pmc_20 = str(K[12]).split(":")[1]
        else:
            pmc_20 = 0.0
        
        return Drug(antibiotico,pmc_20,ean1,ean2,restriction,product_name,apresentation,classe,type_product,tarja,register,substance_pharm,can_sell)
def construct_product(K):
    laboratorio = parseCellString(K,1)
    product_name = parseCellString(K,5)
    pmc_20 = str(K[12]).split(":")[0]
    if pmc_20 == "number":
        pmc_20 = str(K[12]).split(":")[1]
    else:
        pmc_20 = 0.0

    principio_ativo = str(K[0]).split(":")[1].replace("'","")
    is_drug = True

    apresentation = parseCellString(K,6)
    register = parseCellString(K,2)
    description = "Apresentação: "
    description += apresentation
    description += " ;Registro MS: "
    description += register


    return Product(laboratorio,product_name,description,principio_ativo,is_drug)


def search_linear_and_remove(A,_list_tables_antibiotics):
    for i in _list_tables_antibiotics[1:]:
        cell_str = str(i)
        s = cell_str.split(":")
        string_c = s[1].replace("'","")
        for k in A[1:]:
            cell_str_0 = str(k[0])
            spliter_cel_0 = cell_str_0.split(":")
            string_cel_0 = spliter_cel_0[1].replace("'","")

            cell_str_1 = str(k[5])
            spliter_cel_1 = cell_str_1.split(":")
            string_cel_1 = spliter_cel_1[1].replace("'","")

            if string_cel_0.find(string_c) !=-1 or string_cel_1.find(string_c) != -1:
                A.remove(k)
    return A
                

def eligbles(_list_tables_anvisa,_list_tables_antibiotics):
    list_eligibles_antibiotics = []
    list_eligibles_drugs = []

    for i in _list_tables_antibiotics[1:]:
        cell_str = str(i)
        s = cell_str.split(":")
        string_c = s[1].replace("'","")
        for k in _list_tables_anvisa[1:]:
            cell_str_0 = str(k[0])
            spliter_cel_0 = cell_str_0.split(":")
            string_cel_0 = spliter_cel_0[1].replace("'","")

            cell_str_1 = str(k[5])
            spliter_cel_1 = cell_str_1.split(":")
            string_cel_1 = spliter_cel_1[1].replace("'","")

            if string_cel_0.find(string_c) !=-1 or string_cel_1.find(string_c) != -1:
                medicamento = construct_drug(k,True)
                produto = construct_product(k)
                md5.update(medicamento.ean1.encode("UTF-8"))
                list_eligibles_antibiotics.append([md5.hexdigest(),medicamento,produto])
            
    time.sleep(1)

    list_meds = search_linear_and_remove(_list_tables_anvisa, _list_tables_antibiotics)
    for k in list_meds:
        medicamento = construct_drug(k,False)
        produto = construct_product(k)
        md5.update(medicamento.ean1.encode("UTF-8"))
        list_eligibles_drugs.append( [md5.hexdigest(),medicamento,produto] )
            
        

    print("Quantidade de Antibioticos Encontrados: {list}".format(list=len(list_eligibles_antibiotics)))
    print("Quantidade de Medicamentos Encontrados: {list}".format(list=len(list_eligibles_drugs)))

    return {
        "antibioticos": list_eligibles_antibiotics,
        "medicamentos": list_eligibles_drugs
    }


dict_eligbles = eligbles(_list_tables_anvisa,_list_tables_antibiotics)
temp = time.time() - t1
print("Calculando Elegiveis -> Duração: {time}  Segundos ".format(time=temp))

global aux_p
aux_p = []
def search_ant(item,key,repetidos):
    for i in repetidos:
        if i not in aux_p and i == item:
            aux_p.append(i)
            return key
            break

global aux_d
aux_d = []
def search_drug(item,key,repetidos):
    for i in repetidos:
        if i not in aux_d and i == item:
            aux_d.append(i)
            return key
            break

def new_resolv(seta,drug):
    if drug:
        aux=[]
        for g in seta:
            for k in g.keys():
                values = g.get(k)
                aux.append(values)
        
        contador = Counter(aux)
        repetidos = [
        item for item, quantidade in contador.items() 
            if quantidade > 1
        ]
        q=[]
        for n in seta:
            for k in n.keys():
                key_resultante = search_drug(n.get(k),k,repetidos)
                q.append(key_resultante)

        result_keys=[]
        for i in q:
            if i != None:
                result_keys.append(i)

        return remove(result_keys)
    else:
        aux=[]
        for g in seta:
            for k in g.keys():
                values = g.get(k)
                aux.append(values)
        
        contador = Counter(aux)
        repetidos = [
        item for item, quantidade in contador.items() 
            if quantidade > 1
        ]
        q=[]
        for n in seta:
            for k in n.keys():
                key_resultante = search_ant(n.get(k),k,repetidos)
                q.append(key_resultante)

        result_keys=[]
        for i in q:
            if i != None:
                result_keys.append(i)

        return remove(result_keys)
def remove(lista):
    aux = []
    for i in lista:
        if i not in aux:
            aux.append(i)
    
    aux.sort()
    return aux

def distinct_antibiotcs(eligbles):
    p = eligbles.get("antibioticos")
    list_ant = []
    d = {}
    for i in p:
        list_ant.append({i[0]: i[1].ean1})
        d.update({i[0]: i[1].ean1})
    

    keys_distinct = new_resolv(list_ant,False)

    for k in keys_distinct:
        for n in p:
            if k == n[0]:
                p.remove(n)
                
    return p


def distinct_drugs(eligbles):
    p = eligbles.get("medicamentos")
    list_ant = []
    d = {}
    for i in p:
        list_ant.append({i[0]: i[1].ean1})
        d.update({i[0]: i[1].ean1})
    

    keys_distinct = new_resolv(list_ant,True)

    for k in keys_distinct:
        for n in p:
            if k == n[0]:
                p.remove(n)
                
    return p

def sender_eligibles_endpoint(medicamentos,antibioticos):
    # sender elegiveis para endpoint ;
    pass



antibioticos = distinct_antibiotcs(dict_eligbles)
medicamentos = distinct_drugs(dict_eligbles)


sender_eligibles_endpoint(medicamentos,antibioticos)
