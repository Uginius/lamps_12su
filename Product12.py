class Product12:
    def __init__(self, tr):
        self.td_cells = tr.find_all('td')
        self.id = None
        self.name = None
        self.url = None
        self.status = None
        self.price = None
        self.order = 0

    def parse(self):
        self.id = int(self.td_cells[0].find('span').string)
        self.name = self.td_cells[1].a.string
        self.url = 'https://1-2.su' + self.td_cells[1].a.get('href')
        self.status = str(self.td_cells[4].text)
        if 'Под заказ' in self.status:
            self.status = 'Под заказ, ' + self.status.split('Под заказ')[-1].strip()
        self.price = self.td_cells[5].div.string
        if self.price:
            self.price = float(self.price)

    def print_out(self):
        print('\n', '=' * 3, self.order, '=' * 100)
        print('id:', self.id)
        print('name:', self.name)
        print('url:', self.url)
        print('status:', self.status)
        print('price:', self.price)

    def data_out(self):
        return self.id, self.name, self.url, self.price
