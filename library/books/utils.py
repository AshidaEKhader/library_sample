import xlwt
import uuid


def generate_report(data, report_name):
    """
    Function to generate excel report
    :param data:Report data
    :param report_name:Name for report
    :return:
    """
    #: Create a work book
    wb = xlwt.Workbook()
    #: Add the sheet
    ws = wb.add_sheet('Test sheet')
    row_num=0
    col_num=0
    #: Add the headings
    columns = ('Title', 'Status', 'Rented days', 'Authors')
    for col_num, col_value in enumerate(columns):
        ws.write(row_num, col_num, col_value)
    row_num +=1
    #: Iterate through each data and write ti each row of excel
    for book_info in data:
        col_num = 0
        author_names = ''
        for author in book_info.authors.all():
            author_names += author.username + ' '
        columns = (book_info.title, book_info.status, book_info.rented_days, author_names)
        for col_num, col_value in enumerate(columns):
            ws.write(row_num, col_num, col_value)
        row_num += 1

    wb.save(report_name + '.xlsx')