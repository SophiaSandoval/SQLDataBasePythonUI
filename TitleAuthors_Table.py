import flet as ft
import mysql.connector
from flet import *

mydb = mysql.connector.connect(
    host="localhost", database="project2", user="root", password="Oranges1331"
)
cursor = mydb.cursor()


def TitleAuthorsTable(page: ft.Page):
    titleIDtxt = TextField(label="titleID")
    auIDtxt = TextField(label="auID")
    importancetxt = TextField(label="importance")

    edit_titleIDtxt = TextField(label="titleID")
    edit_auIDtxt = TextField(label="auID")
    edit_importancetxt = TextField(label="importance")

    mydt = DataTable(
        columns=[
            DataColumn(Text("titleID")),
            DataColumn(Text("auID")),
            DataColumn(Text("importance")),
            DataColumn(Text("Actions")),
        ],
        rows=[],
    )

    def deletebtn(e):
        print("you selected titleID is =", e.control.data["titleID"])
        try:
            sql = "DELETE FROM TitleAuthors WHERE titleID = %s"
            val = (e.control.data["titleID"],)
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
                "UPDATE TitleAuthors SET auID = %s, importance = %s Where titleID = %s"
            )
            val = (edit_auIDtxt.value, edit_importancetxt.value, edit_titleIDtxt.value)
            cursor.execute(sql, val)
            mydb.commit()
            print("you successfully edited database")
            dialog.open = False
            page.update()

            edit_titleIDtxt.value = " "
            edit_auIDtxt.value = " "
            edit_importancetxt.value = " "

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
        content=Column([edit_titleIDtxt, edit_auIDtxt, edit_importancetxt]),
        actions=[TextButton("Save", on_click=savedata)],
    )

    def editbtn(e):
        edit_titleIDtxt.value = e.control.data["titleID"]
        edit_auIDtxt.value = e.control.data["auID"]
        edit_importancetxt.value = e.control.data["importance"]
        page.dialog = dialog
        dialog.open = True
        page.update()

    def load_data():
        cursor.execute("SELECT * FROM TitleAuthors")
        result = cursor.fetchall()

        colums = [column[0] for column in cursor.description]
        rows = [dict(zip(colums, row)) for row in result]

        for row in rows:
            mydt.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(row["titleID"])),
                        DataCell(Text(row["auID"])),
                        DataCell(Text(row["importance"])),
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
            sql = """INSERT INTO TitleAuthors(titleID, auID, importance) VALUES(%s, %s, %s)"""
            val = (titleIDtxt.value, auIDtxt.value, importancetxt.value)
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

            titleIDtxt.value = ""
            auIDtxt.value = ""
            importancetxt.value = ""
            page.update()

    page.add(
        Column(
            [
                ft.Row(
                    [ft.Text("TitleAuthors Table", size=30)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                titleIDtxt,
                auIDtxt,
                importancetxt,
                ElevatedButton("add to db", on_click=addtodb),
                mydt,
            ]
        )
    )

    return TitleAuthorsTable


# ft.app(target=SubjectTable)
