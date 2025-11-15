class PrizeController:
    def __init__(self, prizeService):
        print(f'Initiating PrizeController, variables: \nprizeService: {prizeService}')
        self.prizeService = prizeService

    def get_all_prizes(self):
        print('In PrizeController, method: get_all_prizes')
        return self.prizeService.get_all_prizes()

    def update_prizes(self, prizes_list: list):
        print(f'In PrizeController, method: update_prizes, variables: \nprizes_list: {prizes_list}')
        return self.prizeService.update_prizes(prizes_list)

    def use_points(self, cliente_id: str, points: int):
        print(f'In PrizeController, method: use_points, variables: \ncliente_id: {cliente_id}, points: {points}')
        return self.prizeService.use_points(cliente_id, points)
