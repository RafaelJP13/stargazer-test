class CustomerService:

    def __init__(self, db):
        self.db = db

    def create(self, payload):

        status = "Aguardando Análise"

        return 'cliente criado com sucesso'