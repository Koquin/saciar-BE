from datetime import datetime 

class Cliente :
    def __init__ (
    self ,
    id :int |None ,
    nome :str ,
    cpf :str ,
    telefone :str ,
    pontos :int ,
    qtd_gasta :float ,
    created_at :datetime ,
    updated_at :datetime 
    ):
        self .id :int |None =id 
        self .nome =nome 
        self .cpf =cpf 
        self .telefone =telefone 
        self .pontos =pontos 
        self .qtd_gasta =qtd_gasta 
        self .created_at :datetime =created_at 
        self .updated_at :datetime =updated_at 
