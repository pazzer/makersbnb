class Space:
    def __init__(self, space_id, name, description, price_per_night, user_id):
        self.space_id = space_id
        self.name = name
        self.description = description
        self.price_per_night = price_per_night
        self.user_id = user_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f'Space({self.space_id}, {self.name}, {self.description}, {self.price_per_night}, {self.user_id})'

    @staticmethod
    def image_for_id(id_):
        if id_ == 1: # Crazy Cabin
            return '🛖'
        elif id_ == 2: # Urban Loft
            return '🪜'
        elif id_ == 3: # Beach Bungalow
            return '⛱️'
        elif id_ == 4: # Mountain Retreat
            return '⛰️'
        elif id_ == 5: # Modern Studio
            return '🍸'
        elif id == 6: # Cool Castle
            return '🏰'
        else:
            return ''
