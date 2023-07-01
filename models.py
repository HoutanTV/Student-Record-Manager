import re
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound, IntegrityError


class Person:
    def __init__(self, first_name, last_name, national_id, email, phone_number):
        self._name_validator(first_name)
        self._first_name = first_name
        self._name_validator(last_name)
        self._last_name = last_name
        self._national_id_validator(national_id)
        self._national_id = national_id
        self._email_validator(email)
        self._email = email
        self._phone_number_validator(phone_number)
        self._phone_number = phone_number

    class NameError(Exception):
        pass

    class IDError(Exception):
        pass

    class EmailError(Exception):
        pass

    class PhoneNumberError(Exception):
        pass

    def show_information(self):
        return f"First name: {self._first_name}\nLast name: {self._last_name}\nNational ID: {self._national_id}" \
               f"\nEmail : {self._email}\nPhone number : {self._phone_number}"

    @staticmethod
    def _name_validator(name: str):
        # Mohammad Amin
        name_list = name.split(" ")
        for name in name_list:
            if not name.isalpha():
                raise Person.NameError
        return True

    @staticmethod
    def _national_id_validator(national_id: str):
        for char in national_id:
            if not char.isdigit():
                raise Person.IDError
        if len(national_id) != 10:
            raise Person.IDError
        return True

    @staticmethod
    def _email_validator(email: str):
        pattern = r"\w+@\w+.\w+"
        result = re.match(pattern, email)
        if not result:
            raise Person.EmailError
        return True

    @staticmethod
    def _phone_number_validator(phone_number: str):
        pattern = r"09\d{9}"
        result = re.match(pattern, phone_number)
        if not result:
            raise Person.PhoneNumberError
        return True


class Student(Person):

    def __init__(self, first_name, last_name, national_id, email, phone_number, birthday, grades=None):
        super().__init__(first_name, last_name, national_id, email, phone_number)
        self._grades = grades
        self._birthday_validator(birthday)
        self._birthday = birthday

    class BirthDayError(Exception):
        pass

    class GradeError(Exception):
        pass

    # Methods for updating information about students

    def show_information(self):
        print(f"First name: {self._first_name}\nLast name: {self._last_name}\nNational ID: {self._national_id}"
              f"\nEmail : {self._email}\nPhone number : {self._phone_number}\nBirthday: {self._birthday}")

    def show_grades(self):
        result = f"Student name : {self._first_name} {self._last_name}"
        for grade in self._grades:
            grade_text = f"\n{grade} : {self._grades[grade]}"
            result += grade_text
        return result

    def set_first_name(self, new_first_name: str):
        self._name_validator(new_first_name)
        self._first_name = new_first_name
        return new_first_name

    def set_last_name(self, new_last_name: str):
        self._name_validator(new_last_name)
        self._last_name = new_last_name
        return new_last_name

    def set_national_id(self, new_national_id: str):
        self._national_id_validator(new_national_id)
        self._national_id = new_national_id
        return new_national_id

    def set_email(self, new_email: str):
        self._email_validator(new_email)
        self._email = new_email
        return new_email

    def set_phone_number(self, new_phone_number: str):
        self._phone_number_validator(new_phone_number)
        self._phone_number = new_phone_number
        return new_phone_number

    def set_birthday(self,new_birthday: str):
        self._birthday_validator(new_birthday)
        self._birthday = new_birthday
        return new_birthday

    def set_grades(self, grades: dict):
        self._grades_validator(grades)
        self._grades = grades
        return grades

    @staticmethod
    def _grades_validator(grades: dict):
        for grade in grades:
            if type(grade) == str and type(grades[grade]) == float:
                if 0 <= grades[grade] <= 20:
                    pass
                else:
                    raise Student.GradeError
            else:
                raise Student.GradeError

    @staticmethod
    def _birthday_validator(birthday: str):
        pattern = r"\d{4}(-|/)\d{2}(-|/)\d{2}"
        result = re.match(pattern, birthday)
        if not result:
            raise Student.BirthDayError
        return True


engine = create_engine('sqlite:///school.db')

Base = declarative_base()


class Students(Base):
    __tablename__ = 'students'
    id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    birthday = Column(String)


class Admins(Base):
    __tablename__ = 'admins'
    id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    password = Column(String)


class Grades(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    lesson = Column(String)
    grade = Column(Float)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class Admin(Person):

    def __init__(self, first_name, last_name, national_id, email, phone_number, password):
        super().__init__(first_name, last_name, national_id, email, phone_number)
        self._password_validator(password)
        self._password = password

    class PasswordValidationError(Exception):
        pass

    class PasswordError(Exception):
        pass

    class StudentNotFound(Exception):
        pass

    @staticmethod
    def register_student(firstname, lastname, national_id, email, phone_number, birthday):
        our_student = Students(id=national_id, first_name=firstname, last_name=lastname, email=email,
                               phone_number=phone_number
                               , birthday=birthday)
        student_object = Student(firstname, lastname, national_id, email, phone_number
                                 , birthday)
        session.add(our_student)
        session.commit()

    def change_student_first_name(self, student_id, first_name):
        student_obj = self.find_student_object(student_id)
        student_obj.set_first_name(first_name)
        our_student = self.find_student(student_id)
        our_student.first_name = first_name
        session.commit()
        return first_name

    def change_student_last_name(self, student_id, last_name):
        student_obj = self.find_student_object(student_id)
        student_obj.set_last_name(last_name)
        our_student = self.find_student(student_id)
        our_student.first_name = last_name
        session.commit()
        return last_name

    def change_student_id(self, student_id, national_id):
        student_obj = self.find_student_object(student_id)
        student_obj.set_national_id(national_id)
        our_student = self.find_student(student_id)
        our_student.id = national_id
        session.commit()
        return national_id

    def change_student_email(self, student_id, email):
        student_obj = self.find_student_object(student_id)
        student_obj.set_email(email)
        our_student = self.find_student(student_id)
        our_student.email = email
        session.commit()
        return email

    def change_student_phone_number(self, student_id, phone_number):
        student_obj = self.find_student_object(student_id)
        student_obj.set_phone_number(phone_number)
        our_student = self.find_student(student_id)
        our_student.phone_number = phone_number
        session.commit()
        return phone_number

    def change_student_birthday(self, student_id, birthday):
        student_obj = self.find_student_object(student_id)
        student_obj.set_birthday(birthday)
        our_student = self.find_student(student_id)
        our_student.birthday = birthday
        session.commit()
        return birthday


    def delete_student(self, student_id):
        our_student = self.find_student(student_id)
        session.delete(our_student)
        session.commit()

    def set_grade(self, student_id, lesson, grade):
        try:
            student_obj = self.find_student_object(student_id)
            student_obj.set_grades({lesson: grade})
            our_grade = session.query(Grades).filter(Grades.student_id == student_id, Grades.lesson == lesson).one()
            our_grade.grade = grade
            session.commit()
        except NoResultFound:
            our_grade = Grades(student_id=student_id, lesson=lesson, grade=grade)
            session.add(our_grade)
            session.commit()

    def show_grades(self,student_id):
        student_grades = session.query(Grades).filter(Grades.student_id == student_id).all()
        for grade in student_grades:
            print(grade.lesson, ":", grade.grade)

    @staticmethod
    def _password_validator(password):
        if len(password) < 8:
            raise Admin.PasswordValidationError
        return True

    @staticmethod
    def find_student(student_id: str):
        try:
            our_student = session.query(Students).filter(Students.id == student_id).one()
            return our_student
        except NoResultFound:
            raise Admin.StudentNotFound

    # Actual object of student
    @staticmethod
    def find_student_object(student_id: str):
        try:
            our_student = session.query(Students).filter(Students.id == student_id).one()
            student_obj = Student(our_student.first_name, our_student.last_name, our_student.id,
                                  our_student.email, our_student.phone_number, our_student.birthday)
            return student_obj
        except NoResultFound:
            raise Admin.StudentNotFound


def create_admin(first_name, last_name, national_id, email, phone_number, password):
    our_admin_obj = Admin(first_name, last_name, national_id, email, phone_number, password)
    our_admin = Admins(id=national_id, first_name=first_name, last_name=last_name, email=email,
                       phone_number=phone_number,password=password)
    session.add(our_admin)
    session.commit()

    return True


# new_user = Students(id="0441200524",first_name='John',last_name="ahmadi",email="akbar@gmail.com",phone_number="09025694650",birthday= "2004-03-16")
# session.add(new_user)
# session.commit()

# our_user = session.query(Students).filter(Students.id == "0441200524").one()
# our_user.first_name = "Ahmad"
# session.commit()
# our_grade1 = Grades(student_id="0441200524",lesson="Arabic",grade=18.5)
# our_grade2 = Grades(student_id="0441200888",lesson="Arabic",grade=18.5)
# session.add(our_grade1)
# session.add(our_grade2)
# our_grade = session.query(Grades).filter(Grades.student_id == "0441200524", Grades.lesson == "English").one()
# print(our_grade.grade)
# session.commit()

