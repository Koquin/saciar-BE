from datetime import datetime 

class Cliente :
    def __init__ (
    self ,
    id :int |None ,
    nome :str ,
    telefone :str ,
    pontos :int ,
    qtd_gasta :float ,
    troco :float =0.0 ,
    created_at :datetime =None ,
    updated_at :datetime =None 
    ):
        self .id :int |None =id 
        self .nome =nome 
        self .telefone =telefone 
        self .pontos =pontos 
        self .qtd_gasta =qtd_gasta 
        self .troco =troco 
        self .created_at :datetime =created_at 
        self .updated_at :datetime =updated_at 
