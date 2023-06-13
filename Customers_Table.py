import flet as ft
import mysql.connector
from flet import *

mydb = mysql.connector.connect(
    host="localhost", database="project2", user="root", password="Oranges1331"
)
cursor = mydb.cursor()


def CustomersTable(page: ft.Page):
    custIDtxt = TextField(label="custID")
    custnametxt = TextField(label="custName")
    ziptxt = TextField(label="zip")
    citytxt = TextField(label="city")
    statetxt = TextField(label="state")

    edit_custIDtxt = TextField(label="custID")
    edit_custnametxt = TextField(label="custName")
    edit_ziptxt = TextField(label="zip")
    edit_citytxt = TextField(label="city")
    edit_statetxt = TextField(label="state")

    mydt = DataTable(
        columns=[
            DataColumn(Text("custId")),
            DataColumn(Text("custName")),
            DataColumn(Text("zip")),
            DataColumn(Text("city")),
            DataColumn(Text("state")),
            DataColumn(Text("Actions")),
        ],
        rows=[],
    )

    def deletebtn(e):
        print("you selected custID is =", e.control.data["custID"])
        try:
            sql = "DELETE FROM customers WHERE custID = %s"
            val = (e.control.data["custID"],)
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
            sql = "UPDATE customers SET custName = %s, zip = %s, city = %s, state = %s Where custID = %s"
            val = (
                edit_custnametxt.value,
                edit_ziptxt.value,
                edit_citytxt.value,
                edit_statetxt.value,
                edit_custIDtxt.value,
            )
            cursor.execute(sql, val)
            mydb.commit()
            print("you successfully edited database")
            dialog.open = False
            page.update()

            edit_custIDtxt.value = " "
            edit_custnametxt.value = " "
            edit_ziptxt.value = " "
            edit_citytxt.value = " "
            edit_statetxt.value = " "

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
            [edit_custIDtxt, edit_custnametxt, edit_ziptxt, edit_citytxt, edit_statetxt]
        ),
        actions=[TextButton("Save", on_click=savedata)],
    )

    def editbtn(e):
        edit_custIDtxt.value = e.control.data["custID"]
        edit_custnametxt.value = e.control.data["custName"]
        edit_ziptxt.value = e.control.data["zip"]
        edit_citytxt.value = e.control.data["city"]
        edit_statetxt.value = e.control.data["state"]
        page.dialog = dialog
        dialog.open = True
        page.update()

    def load_data():
        cursor.execute("SELECT * FROM customers")
        result = cursor.fetchall()

        colums = [column[0] for column in cursor.description]
        rows = [dict(zip(colums, row)) for row in result]

        for row in rows:
            mydt.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(row["custID"])),
                        DataCell(Text(row["custName"])),
                        DataCell(Text(row["zip"])),
                        DataCell(Text(row["city"])),
                        DataCell(Text(row["state"])),
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
            sql = """INSERT INTO customers(custID, custName, zip, city, state) VALUES(%s, %s, %s, %s, %s)"""
            val = (
                custIDtxt.value,
                custnametxt.value,
                ziptxt.value,
                citytxt.value,
                statetxt.value,
            )
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

            custIDtxt.value = ""
            custnametxt.value = ""
            ziptxt.value = ""
            citytxt.value = ""
            statetxt.value = ""
            page.update()

    page.add(
        Column(
            [
                ft.Row(
                    [ft.Text("Customers Table", size=30)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                custIDtxt,
                custnametxt,
                ziptxt,
                citytxt,
                statetxt,
                ElevatedButton("add to db", on_click=addtodb),
                mydt,
            ]
        )
    )

    return CustomersTable


# ft.app(target=SubjectTable)
