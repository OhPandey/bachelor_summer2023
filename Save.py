from fpdf import FPDF

from Student import Student


class Save:

    def __init__(self, students):
        if students is None:
            self.students = list()
        if not isinstance(students, list):
            self.students = list()
        self.students = students

    def saveAsPdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)

        for i, x in enumerate(self.students):
            if not isinstance(x, Student):
                text="<Error retrieving this Student>"
            else:
                text = f"{x.getName()}, {x.getBirth()}, {x.getId()}, SEAT: {x.getSeat()}"
            pdf.cell(200, 5, txt=text, ln=1)

        # Placeholder. User should be able to decide the directory
        pdf.output("Students.pdf")
