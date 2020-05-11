import xlrd
from .settings.settings import PATH_ARCHIVE_ANVISA_MED,PATH_ARCHIVE_ANVISA_ANT
dont_settr = 'DONT SETTER'


class ReaderXLS(object):

    def __init__(self):
        if PATH_ARCHIVE_ANVISA_MED == dont_settr or PATH_ARCHIVE_ANVISA_ANT == dont_settr:
            print('PATH NOT FOUND FOR TABLES ANVISA')
        else:
            self.path_anvisa_med=PATH_ARCHIVE_ANVISA_MED
            self.path_anvisa_ant=PATH_ARCHIVE_ANVISA_ANT
    
    def create_woorkbooks(self):
        return {
                "anvisa_med": xlrd.open_workbook(self.path_anvisa_med),
                "anvisa_ant": xlrd.open_workbook(self.path_anvisa_ant)
        }
    def get_name_woorkbook(woorkbook):
        pass

    def gerenate_data_anvisa(self,woorkbook):
        anv_list = []
        cont_anv=0
        anvisa_med = woorkbook.get('anvisa_med')
        principio_ativo = anvisa_med.sheet_by_index(0).col(0)
        laboratorio = anvisa_med.sheet_by_index(0).col(1)
        registro = anvisa_med.sheet_by_index(0).col(2)
        ean1 = anvisa_med.sheet_by_index(0).col(3)
        ean2 = anvisa_med.sheet_by_index(0).col(4)
        produto = anvisa_med.sheet_by_index(0).col(5)
        apresentacao = anvisa_med.sheet_by_index(0).col(6)
        classe = anvisa_med.sheet_by_index(0).col(7)
        tipo = anvisa_med.sheet_by_index(0).col(8)
        registricao=anvisa_med.sheet_by_index(0).col(9)
        tarja = anvisa_med.sheet_by_index(0).col(10)
        substancia = anvisa_med.sheet_by_index(0).col(11)
        pmc_20 = anvisa_med.sheet_by_index(0).col(12)

        for i in range(len(principio_ativo)):
            anv_list.append([
                principio_ativo[i],
                laboratorio[i],
                registro[i],
                ean1[i],
                ean2[i],
                produto[i],
                apresentacao[i],
                classe[i],
                tipo[i],
                registricao[i],
                tarja[i],
                substancia[i],
                pmc_20[i]
            ])
            cont_anv+=1
            
        print("Generating Data Collect: {counter} Registers Table Anvisa".format(counter=cont_anv))
        return anv_list
    def generate_data_anvisa_ant(self,woorkbook):
        anv_list = []
        cont_anv=0
        anvisa_ant = woorkbook.get('anvisa_ant')
        antibiotico = anvisa_ant.sheet_by_index(0).col(0)
        for i in range(len(antibiotico)):
            anv_list.append(antibiotico[i])
            cont_anv+=1
        print("Generating Data Collect: {counter} Registers Table Antibiotics".format(counter=cont_anv))
        return anv_list

def get_instance():
    return ReaderXLS()



    
