class Drug(object):
    def __init__(self,antibiotic,pmc,ean1,ean2,restriction,product_name,apresentation,classe,type_product,tarja,register,pharm,can_sell):
        self.ean1=ean1
        self.ean2=ean2
        self.restriction=restriction
        self.product_name=product_name
        self.apresentation=apresentation
        self.classe=classe
        self.type_product=type_product
        self.tarja=tarja
        self.register=register
        self.pharm=pharm
        self.can_sell=can_sell
        self.pmc=pmc
        self.is_antibiotic=antibiotic
    