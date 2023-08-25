from .item import Item


class Article(Item):
    def __init__(self, title='?', author='?'):
        print('\tArticle.__init__(self)')
        super().__init__(title)   # <-- title goes to "item.name"
        # self.title = title
        self.author = author

    # def __init__(self):
    #     print('==> Article.__init__(self) called')
    #     super().__init__(self, 'name?')
    #     # , name='?', author='?'
    #     self.author = '?'

    def __str__(self):
        return (
            # super().__str__() + f'\n  Article =====> (title="{self.title}", author="{self.author}")'
            f'Article: title="{self.title}", author="{self.author}", --|> '
            + super().__str__()
        )
        # f'Article =======> (name="{self.name}", title="{self.title}", author="{self.author}")'

    @property
    def title(self):    # alias for name
        """Get the current title."""
        return self.name
