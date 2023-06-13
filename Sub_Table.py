import flet as ft
import mysql.connector
from flet import *

mydb = mysql.connector.connect(
    host="localhost", database="project2", user="root", password="Oranges1331"
)
cursor = mydb.cursor()


def SubjectTable(page: ft.Page):
    page.title = "Subjects"
    subtxt = TextField(label="subID")
    snametxt = TextField(label="sName")

    edit_subtxt = TextField(label="subID")
    edit_snametxt = TextField(label="sName")

    mydt = DataTable(
        columns=[
            DataColumn(Text("subId")),
            DataColumn(Text("sName")),
            DataColumn(Text("Actions")),
        ],
        rows=[],
    )

    def deletebtn(e):
        print("you selected subID is =", e.control.data["subID"])
        try:
            sql = "DELETE FROM subjects WHERE subID = %s"
            val = (e.control.data["subID"],)
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
            sql = "UPDATE subjects SET sName = %s Where subID = %s"
            val = (edit_snametxt.value, edit_subtxt.value)
            cursor.execute(sql, val)
            mydb.commit()
            print("you successfully edited database")

            mydt.rows.clear()
            load_data()
            dialog.open = False
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
        content=Column([edit_subtxt, edit_snametxt]),
        actions=[TextButton("Save", on_click=savedata)],
    )

    def editbtn(e):
        edit_subtxt.value = e.control.data["subID"]
        edit_snametxt.value = e.control.data["sName"]
        page.dialog = dialog
        dialog.open = True
        page.update()

    def load_data():
        mydt.rows.clear()
        cursor.execute("SELECT * FROM subjects")
        result = cursor.fetchall()

        colums = [column[0] for column in cursor.description]
        rows = [dict(zip(colums, row)) for row in result]

        for row in rows:
            mydt.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(row["subID"])),
                        DataCell(Text(row["sName"])),
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
            sql = """INSERT INTO subjects(subID, sName) VALUES(%s, %s)"""
            val = (subtxt.value, snametxt.value)
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

            subtxt.value = ""
            snametxt.value = ""
            page.update()

    page.add(
        Column(
            [
                ft.Row(
                    [ft.Text("Subjects Table", size=30)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                subtxt,
                snametxt,
                ElevatedButton("add to db", on_click=addtodb),
                mydt,
            ]
        )
    )

    return SubjectTable


# ft.app(target=SubjectTable)
