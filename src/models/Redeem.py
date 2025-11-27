from datetime import datetime 

class Redeem :
    def __init__ (
    self ,
    id :int |None ,
    cliente_id :str ,
    cliente_nome :str ,
    cliente_telefone :str ,
    premio :str ,
    pontos :int ,
    created_at :datetime ,
    updated_at :datetime 
    ):
        self .id :int |None =id 
        self .cliente_id =cliente_id 
        self .cliente_nome =cliente_nome 
        self .cliente_telefone =cliente_telefone 
        self .premio =premio 
        self .pontos =pontos 
        self .created_at :datetime =created_at 
        self .updated_at :datetime =updated_at 
