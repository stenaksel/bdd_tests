class Item:
    def __init__(self, name: str):
        print('\tItem.__init__(self, name)')
        self.name = name

    def __str__(self):
        return f'Item: (name="{self.name}")'
