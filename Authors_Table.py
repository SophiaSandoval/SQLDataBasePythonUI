import flet as ft
import mysql.connector
from flet import *

mydb = mysql.connector.connect(
    host="localhost", database="project2", user="root", password="Oranges1331"
)
cursor = mydb.cursor()


def AuthorsTable(page: ft.Page):
    autxt = TextField(label="auID")
    anametxt = TextField(label="aNAME")
    email = TextField(label="email")
    phone = TextField(label="phone")

    edit_autxt = TextField(label="auID")
    edit_anametxt = TextField(label="aNMAE")
    edit_email = TextField(label="email")
    edit_phone = TextField(label="phone")

    mydt = DataTable(
        columns=[
            DataColumn(Text("auID")),
            DataColumn(Text("aNAME")),
            DataColumn(Text("email")),
            DataColumn(Text("phone")),
            DataColumn(Text("Actions")),
        ],
        rows=[],
    )

    def deletebtn(e):
        print("you selected auID is =", e.control.data["auID"])
        try:
            sql = "DELETE FROM authors WHERE auID = %s"
            val = (e.control.data["auID"],)
            cursor.execute(sql, val)
            mydb.commit()
            print("you deleted")
            mydt.rows.clear()
            load_data()
            page.snack_bar = SnackBar(
                Text("Data success deleted", size=30), bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            print(e)
            print("error your CODE for delete!!!")

    def savedata(e):
        try:
            sql = (
                "UPDATE Authors SET aNAME = %s, email = %s, phone = %s Where auID = %s;"
            )
            val = (
                edit_anametxt.value,
                edit_email.value,
                edit_phone.value,
                edit_autxt.value,
            )
            cursor.execute(sql, val)
            mydb.commit()
            print("you successfully edited database")
            dialog.open = False
            page.update()

            edit_autxt.value = " "
            edit_anametxt.value = " "
            edit_email.value = " "
            edit_phone.value = " "
            page.update()

            mydt.rows.clear()
            load_data()
            page.snack_bar = SnackBar(
                Text("Data success EDIT", size=30), bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            print(e)
            print("Error Saving edit!!!")

    dialog = AlertDialog(
        title=Text("edit data"),
        content=Column([edit_autxt, edit_anametxt, edit_email, edit_phone]),
        actions=[TextButton("Save", on_click=savedata)],
    )

    def editbtn(e):
        edit_autxt.value = e.control.data["auID"]
        edit_anametxt.value = e.control.data["aNAME"]
        edit_email.value = e.control.data["email"]
        edit_phone.value = e.control.data["phone"]
        page.dialog = dialog
        dialog.open = True
        page.update()

    def load_data():
        cursor.execute("SELECT * FROM authors;")
        result = cursor.fetchall()

        colums = [column[0] for column in cursor.description]
        rows = [dict(zip(colums, row)) for row in result]

        for row in rows:
            mydt.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(row["auID"])),
                        DataCell(Text(row["aNAME"])),
                        DataCell(Text(row["email"])),
                        DataCell(Text(row["phone"])),
                        DataCell(
                            Row(
                                [
                                    IconButton(
                                        "delete",
                                        icon_color="red",
                                        data=row,
                                        on_click=deletebtn,
                                    ),
                                    IconButton(
                                        "create",
                                        icon_color="green",
                                        data=row,
                                        on_click=editbtn,
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            )
            page.update()

    load_data()

    def addtodb(e):
        try:
            sql = """INSERT INTO authors(auID, aNAME, email, phone) VALUES(%s, %s, %s, %s)"""
            val = (autxt.value, anametxt.value, email.value, phone.value)
            cursor.execute(sql, val)
            mydb.commit()
            print(cursor.rowcount, "you record insert")

            mydt.rows.clear()
            load_data()
            page.snack_bar = SnackBar(
                Text("Data success add", size=30), bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            print(e)
            print("Error you CODE !!!")

            autxt.value = " "
            anametxt.value = " "
            email.value = " "
            phone.value = " "
            page.update()

    page.add(
        Column(
            [
                ft.Row(
                    [ft.Text("Authors Table", size=30)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                autxt,
                anametxt,
                email,
                phone,
                ElevatedButton("add to db", on_click=addtodb),
                mydt,
            ]
        )
    )

    return AuthorsTable


# ft.app(target=SubjectTable)
