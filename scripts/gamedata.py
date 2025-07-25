
import pygame

import scripts.core as c


hidden_icon = pygame.transform.scale(pygame.image.load('asset\\success\\hidden.png'), (56, 56))


class Success():
    def __init__(self, id, title, description, hidden=False):
        self.id = id
        self.title = title
        self.description = description
        self.icon_unlocked = pygame.image.load('asset\\success\\' + id + '.png')
        self.icon_locked = pygame.transform.grayscale(self.icon_unlocked)
        self.icon = hidden_icon if hidden else self.icon_locked
        self.hidden = hidden
        self.unlocked = False
    
    def unlock(self):
        self.unlocked = True
        self.icon = self.icon_unlocked


class SuccessManager():
    def __init__(self, game):
        self.game = game
        data = c.read_file('asset\\success.json')
        self.success_data, self.success_order = data['success'], data['order']
        self.success = {}
        self.unlocked = []
        
    def setup(self, unlocked):
        for s in self.success_data.keys():
            success = Success(s, *self.success_data[s])
            self.success[s] = success
            if s in unlocked:
                success.unlock()
                self.unlocked.append(s)
    
    def unlock(self, id):
        if not id in self.unlocked:
            self.unlocked.append(id)
            self.success[id].unlock()
            self.game.set_popup(self.success[id].title)


class GameDataManager():
    def __init__(self, game):
        self.game = game
        self.data_file = 'data\\data.json'
        self.success_mgr = SuccessManager(game)
        self.load_data()
        self.load_shop_data()
    
    def load_data(self):
        data = c.read_file(self.data_file)
        self.high_score   = data['score']
        self.credits      = int(data['currency'])
        self.magnet_power = int(data['magnet'])
        self.games_nb     = int(data['games_nb'])
        self.powers       = data['powers']
        self.repulsions   = data['repulsions']
        self.freezes      = data['freezes']
        self.success_mgr.setup(data['unlocked_success'])
    
    def get_data(self):
        return {
            'score': self.high_score,
            'currency': self.game.credits,
            'magnet': self.game.magnet_power,
            'games_nb': self.games_nb,
            'unlocked_success': self.success_mgr.unlocked,
            'powers': self.powers,
            'freezes': self.freezes,
            'repulsions': self.repulsions
            }
    
    def save_data(self):
        c.write_file(self.data_file, self.get_data())
    
    def load_shop_data(self):
        data = c.read_file('asset/spaceship.json')
        self.magnet_prices = data['magnet_prices']
        self.unlock_freeze = data['unlock_freeze']
        self.unlock_repulsion = data['unlock_repulsion']
        self.freeze_prices = data['freeze']
        self.repulsion_prices = data['repulsion']
    
    def incr_game_nb(self):
        self.games_nb += 1
        for nb in [50, 100, 200, 500, 1000]:
            if self.games_nb == nb:
                self.success_mgr.unlock(f'runs.{nb}')
                return
        if self.games_nb == 69:
            self.success_mgr.unlock('humor.1')
        elif self.games_nb == 420:
            self.success_mgr.unlock('humor.2')
    
    def check_high_score(self, score):
        if score > self.high_score:
            self.high_score = score
            return True
        else:
            return False
    
    def check_time_success(self, time):
        for t in [1, 2, 3]:
            if time == t:
                self.success_mgr.unlock(f'time.{t}')
                break
    
    def get_success(self, id):
        return self.success_mgr.success[id]
