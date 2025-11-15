from exceptions .UserNotFoundException import UserNotFoundException 
from exceptions .InvalidCredentialsException import InvalidCredentialsException 
import bcrypt 

class AuthService :
    def __init__ (self ,authRepository ):
        print (f'Initiating AuthService, variables: \nauthRepository: {authRepository }')
        self .authRepository =authRepository 

    def login (self ,authDto ):
        print (f'In AuthService, method: login, variables: \nauthDto: {authDto }')
        user =self .authRepository .get_user_by_username (authDto .username )
        if not user :
            raise UserNotFoundException ()
        password_matches =bcrypt .checkpw (authDto .password .encode ('utf-8'),user ['password_hash'].encode ('utf-8'))
        if user and not password_matches :
            raise InvalidCredentialsException ()
        return True 
