class AuthController :
    def __init__ (self ,authService ):
        print (f'Initiating AuthController, variables: \nauthService: {authService }')
        self .authService =authService 

    def login (self ,authDto ):
        print (f'In AuthController, method: login, variables: \nauthDto: {authDto }')
        response =self .authService .login (authDto )
        return response 