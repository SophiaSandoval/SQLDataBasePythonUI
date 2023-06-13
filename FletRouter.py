import flet as ft

from index_view import IndexView
from Sub_Table import SubjectTable
from Pub_Table import PublisherTable
from Customers_Table import CustomersTable
from Authors_Table import AuthorsTable
from TitleAuthors_Table import TitleAuthorsTable
from Titles_Table import TitlesTable


class Router:
    def __init__(self, page):
        self.page = page
        self.ft = ft
        self.routes = {
            "/": IndexView(page),
            "/subjecttable": SubjectTable(page),
            "/publishertable": PublisherTable(page),
            "/customerstable": CustomersTable(page),
            "/authorstable": AuthorsTable(page),
            "/titleauthorstable": TitleAuthorsTable(page),
            "/titles": TitlesTable(page),
        }

        self.body = ft.Container(content=self.routes["/"])

    def route_change(self, route):
        self.body.content = self.routes[route.route]
        self.body.update()
