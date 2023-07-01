from models import *
import os

while True:
    os.system('cls')

    print("""
1. Enter as an admin
2. Create an admin 
3. Exit
""")

    menu_input = input(">>")
    if menu_input == "1":
        try:
            admin_id = input("please enter your national id: ")
            our_admin = session.query(Admins).filter(Admins.id == admin_id).one()
            admin_password = input("please enter your password: ")
            if our_admin.password == admin_password:
                admin = Admin(our_admin.first_name, our_admin.last_name, our_admin.id, our_admin.email,
                              our_admin.phone_number, our_admin.password)
                while True:
                    os.system('cls')
                    print("""
1. register a student
2. change students information
3. change/show students grades 
4. delete a student
5. show all students
6. go back

                    """)

                    menu_input2 = input(">>")
                    if menu_input2 == "1":
                        os.system("cls")
                        try:
                            first_name = input("please enter first name: ")
                            last_name = input("please enter last name: ")
                            national_id = input("please enter national id: ")
                            email = input("please enter email: ")
                            phone_number = input("please enter phone number: ")
                            birthday = input("please enter birthday(####-##-## or ####/##/## format): ")
                            admin.register_student(first_name, last_name, national_id, email, phone_number, birthday)
                            input("student registered successfully press enter to continue.")
                        except Admin.NameError:
                            input("please enter a valid first name or last name.")
                        except Admin.IDError:
                            input("please enter a valid national id.")
                        except Admin.EmailError:
                            input("please enter a valid email address.")
                        except Admin.PhoneNumberError:
                            input("please enter a valid phone number.")
                        except Student.BirthDayError:
                            input("please enter a valid birthday date in the given format.")
                        except IntegrityError:
                            input("national id is already in use.")

                    if menu_input2 == "2":
                        os.system('cls')
                        student_id = input("please enter student id: ")
                        try:
                            student_obj = admin.find_student_object(student_id)
                            student_obj.show_information()
                            print("""
1. first name
2. last name
3. national id
4. email
5. phone number
6. birth day
7. go back
                            
                            """)
                            menu_input22 = input(">>")
                            if menu_input22 == "1":
                                try:
                                    first_name = input("enter the new first name: ")
                                    admin.change_student_first_name(student_id, first_name, )
                                    input("first name changed successfully.")
                                except Admin.NameError:
                                    input("please enter a valid first name or last name.")
                            if menu_input22 == "2":
                                try:
                                    last_name = input("enter the new last name: ")
                                    admin.change_student_last_name(student_id, last_name)
                                    input("last name changed successfully.")
                                except Admin.NameError:
                                    input("please enter a valid first name or last name.")
                            if menu_input22 == "3":
                                try:
                                    id = input("enter the new national id: ")
                                    admin.change_student_last_name(student_id, id)
                                    input("national id changed successfully.")
                                except Admin.IDError:
                                    input("please enter a valid national id.")
                            if menu_input22 == "4":
                                try:
                                    email = input("enter the new email: ")
                                    admin.change_student_email(student_id, email)
                                    input("email changed successfully.")
                                except Admin.EmailError:
                                    input("please enter a valid email address.")
                            if menu_input22 == "5":
                                try:
                                    phone_number = input("enter the phone number: ")
                                    admin.change_student_phone_number(student_id, phone_number)
                                    input("phone number changed successfully.")
                                except Admin.PhoneNumberError:
                                    input("please enter a valid phone number.")
                            if menu_input22 == "6":
                                try:
                                    birthday = input("enter the new birthday: ")
                                    admin.change_student_birthday(student_id, birthday)
                                    input("birthdays changed successfully.")
                                except Student.BirthDayError:
                                    input("please enter a valid birthday date in"
                                          " the given format(####-##-## or ####/##/##).")
                            if menu_input22 == "7":
                                pass

                        except Admin.StudentNotFound:
                            input("student with this id doesn't exist.")

                    if menu_input2 == "3":
                        os.system('cls')
                        print("""
1. change existing grades or add new ones
2. see grades of a student
3. exit
                        """)

                        menu_input23 = input(">>")
                        if menu_input23 == "1":
                            student_id23 = input("please enter student id: ")
                            try:
                                our_student = admin.find_student(student_id23)
                                lesson = input("enter the lesson name: ")
                                grade = float(input("enter the grade: "))
                                admin.set_grade(student_id23, lesson, grade)
                                input("grade added successfully.")
                            except Admin.StudentNotFound:
                                input("student with this id doesn't exist.")
                        if menu_input23 == "2":
                            student_id24 = input("please enter student id: ")
                            try:
                                our_student = admin.find_student(student_id24)
                                admin.show_grades(student_id24)
                                input("press enter to continue.")
                            except Admin.StudentNotFound:
                                input("student with this id doesn't exist.")
                        if menu_input23 == "3":
                            break
                    if menu_input2 == "4":
                        os.system('cls')
                        student_id45 = input("please enter student id: ")
                        try:
                            our_student = admin.find_student(student_id45)
                            admin.delete_student(student_id45)
                            input("student deleted successfully.")
                        except Admin.StudentNotFound:
                            input("student with this id doesn't exist.")

                    if menu_input2 == "5":
                        os.system('cls')
                        all_students = session.query(Students).all()
                        for student in all_students:
                            student_obj = admin.find_student_object(student.id)
                            student_obj.show_information()
                            print("-----------------")
                        input("press enter to continue.")

                    if menu_input2 == "6":
                        break

            else:
                input("incorrect password.")



        except NoResultFound:
            temp = input("admin not found. try again.")

    if menu_input == "2":
        os.system('cls')
        try:
            first_name = input("please enter your first name: ")
            last_name = input("please enter your last name: ")
            national_id = input("please enter your national id: ")
            email = input("please enter your email: ")
            phone_number = input("please enter phone number: ")
            password = input("please enter your password: ")
            create_admin(first_name, last_name, national_id, email, phone_number, password)
            input("admin created successfully press enter to continue.")
        except Admin.NameError:
            input("please enter a valid first name or last name.")
        except Admin.IDError:
            input("please enter a valid national id.")
        except Admin.EmailError:
            input("please enter a valid email address.")
        except Admin.PhoneNumberError:
            input("please enter a valid phone number.")
        except Admin.PasswordValidationError:
            input("please enter a valid password with minimum of 8 characters.")
        except IntegrityError:
            input("national id is already in use.")

    if menu_input == "3":
        break
session.close
