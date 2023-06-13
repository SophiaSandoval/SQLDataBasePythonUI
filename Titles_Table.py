import flet as ft
import mysql.connector
from flet import *

mydb = mysql.connector.connect(
    host="localhost", database="project2", user="root", password="Oranges1331"
)
cursor = mydb.cursor()


def TitlesTable(page: ft.Page):
    titleIDtxt = TextField(label="titleID")
    titletxt = TextField(label="title")
    pubID = TextField(label="pubID")
    subID = TextField(label="subID")
    date = TextField(label="pubDate")
    cover = TextField(label="cover")
    price = TextField(label="price")

    edit_titleIDtxt = TextField(label="titleID")
    edit_titletxt = TextField(label="title")
    edit_pubID = TextField(label="pubID")
    edit_subID = TextField(label="subID")
    edit_date = TextField(label="pubDate")
    edit_cover = TextField(label="cover")
    edit_price = TextField(label="price")

    mydt = DataTable(
        columns=[
            DataColumn(Text("titleID")),
            DataColumn(Text("title")),
            DataColumn(Text("pubID")),
            DataColumn(Text("subID")),
            DataColumn(Text("pubDate")),
            DataColumn(Text("cover")),
            DataColumn(Text("price")),
            DataColumn(Text("Actions")),
        ],
        rows=[],
    )

    def deletebtn(e):
        print("you selected titleID is =", e.control.data["titleID"])
        try:
            sql = "DELETE FROM titles WHERE titleID = %s"
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
            sql = "UPDATE titles SET title = %s, pubID = %s, subID = %s, pubDate = %s, cover = %s, price = %s Where titleID = %s;"
            val = (
                edit_titletxt.value,
                edit_pubID.value,
                edit_subID.value,
                edit_date.value,
                edit_cover.value,
                edit_price.value,
                edit_titleIDtxt.value,
            )
            cursor.execute(sql, val)
            mydb.commit()
            print("you successfully edited database")
            dialog.open = False
            page.update()

            edit_titleIDtxt.value = ""
            edit_titletxt.value = ""
            edit_pubID.value = ""
            edit_subID.value = ""
            edit_date.value = ""
            edit_cover.value = ""
            edit_price.value = ""
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
        content=Column(
            [
                edit_titleIDtxt,
                edit_titletxt,
                edit_pubID,
                edit_subID,
                edit_date,
                edit_cover,
                edit_price,
            ]
        ),
        actions=[TextButton("Save", on_click=savedata)],
    )

    def editbtn(e):
        edit_titleIDtxt.value = e.control.data["titleID"]
        edit_titletxt.value = e.control.data["title"]
        edit_pubID.value = e.control.data["pubID"]
        edit_subID.value = e.control.data["subID"]
        edit_date.value = e.control.data["pubDate"]
        edit_cover.value = e.control.data["cover"]
        edit_price.value = e.control.data["price"]
        page.dialog = dialog
        dialog.open = True
        page.update()

    def load_data():
        cursor.execute("SELECT * FROM titles;")
        result = cursor.fetchall()

        colums = [column[0] for column in cursor.description]
        rows = [dict(zip(colums, row)) for row in result]

        for row in rows:
            mydt.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(row["titleID"])),
                        DataCell(Text(row["title"])),
                        DataCell(Text(row["pubID"])),
                        DataCell(Text(row["subID"])),
                        DataCell(Text(row["pubDate"])),
                        DataCell(Text(row["cover"])),
                        DataCell(Text(row["price"])),
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
            sql0 = "SET foreign_key_checks = 0; "
            sql = """ INSERT INTO titles(titleID, title, pubID, subID, pubDate, cover, price) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
            val = (
                titleIDtxt.value,
                titletxt.value,
                pubID.value,
                subID.value,
                date.value,
                cover.value,
                price.value,
            )
            cursor.execute(sql0, sql, val)
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
            titletxt.value = ""
            pubID.value = ""
            subID.value = ""
            date.value = ""
            cover.value = ""
            price.value = ""
            page.update()

    page.add(
        Column(
            [
                ft.Row(
                    [ft.Text("Titles Table", size=30)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                titleIDtxt,
                titletxt,
                pubID,
                subID,
                date,
                cover,
                price,
                ElevatedButton("add to db", on_click=addtodb),
                mydt,
            ]
        )
    )

    return TitlesTable


# ft.app(target=SubjectTable)
