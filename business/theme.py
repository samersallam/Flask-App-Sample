from model import Theme
from service import theme_svc

class ThemeBusiness:
    @staticmethod
    def test_theme_table():
        payload = {'name': 'Hello'}
        new_theme = Theme(payload)
        theme_svc.create(new_theme)

        qs = theme_svc.read(Theme.id == new_theme.id)
        return qs.data.name