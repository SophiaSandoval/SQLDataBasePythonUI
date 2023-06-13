import flet as ft
import mysql.connector
from flet import *

mydb = mysql.connector.connect(
    host="localhost", database="project2", user="root", password="Oranges1331"
)
cursor = mydb.cursor()


def PublisherTable(page: ft.Page):
    pubtxt = TextField(label="pubID")
    pnametxt = TextField(label="pname")
    email = TextField(label="email")
    phone = TextField(label="phone")

    edit_pubtxt = TextField(label="pubID")
    edit_pnametxt = TextField(label="pname")
    edit_email = TextField(label="email")
    edit_phone = TextField(label="phone")

    mydt = DataTable(
        columns=[
            DataColumn(Text("pubID")),
            DataColumn(Text("pname")),
            DataColumn(Text("email")),
            DataColumn(Text("phone")),
            DataColumn(Text("Actions")),
        ],
        rows=[],
    )

    def deletebtn(e):
        print("you selected pubID is =", e.control.data["pubID"])
        try:
            sql = "DELETE FROM publishers WHERE pubID = %s"
            val = (e.control.data["pubID"],)
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
            sql = "UPDATE publishers SET pname = %s, email = %s, phone = %s Where pubID = %s;"
            val = (
                edit_pnametxt.value,
                edit_email.value,
                edit_phone.value,
                edit_pubtxt.value,
            )
            cursor.execute(sql, val)
            mydb.commit()
            print("you successfully edited database")
            dialog.open = False
            page.update()

            edit_pubtxt.value = " "
            edit_pnametxt.value = " "
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
        content=Column([edit_pubtxt, edit_pnametxt, edit_email, edit_phone]),
        actions=[TextButton("Save", on_click=savedata)],
    )

    def editbtn(e):
        edit_pubtxt.value = e.control.data["pubID"]
        edit_pnametxt.value = e.control.data["pname"]
        edit_email.value = e.control.data["email"]
        edit_phone.value = e.control.data["phone"]
        page.dialog = dialog
        dialog.open = True
        page.update()

    def load_data():
        cursor.execute("SELECT * FROM publishers;")
        result = cursor.fetchall()

        colums = [column[0] for column in cursor.description]
        rows = [dict(zip(colums, row)) for row in result]

        for row in rows:
            mydt.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(row["pubID"])),
                        DataCell(Text(row["pname"])),
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
            sql = """INSERT INTO publishers(pubID, pname, email, phone) VALUES(%s, %s, %s, %s)"""
            val = (pubtxt.value, pnametxt.value, email.value, phone.value)
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

            pubtxt.value = " "
            pnametxt.value = " "
            email.value = " "
            phone.value = " "
            page.update()

    page.add(
        Column(
            [
                ft.Row(
                    [ft.Text("Publishers Table", size=30)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                pubtxt,
                pnametxt,
                email,
                phone,
                ElevatedButton("add to db", on_click=addtodb),
                mydt,
            ]
        )
    )

    return PublisherTable


# ft.app(target=SubjectTable)
