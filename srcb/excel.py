__author__ = 'user'
import win32com.client


class Excel:
    def __init__(self, path, sheet):
        """@path,@sheet must decode to ASCII first"""
        self.app = win32com.client.DispatchEx('Excel.Application')
        self.app.Visible = False
        self.app.ScreenUpdating = False
        self.app.DisplayAlerts = False
        self.workbook = self.app.Workbooks.Open(path)
        self.sheet = self.workbook.Sheets(sheet)

    def set_value(self, row, col, value):
        self.sheet.Cells(row, col).Value = value

    def get_set_value_function(self):
        return self.set_value

    def set_range_value(self, left_top, right_bottom, value):
        self.sheet.Range(self.sheet.Cells(left_top[0], left_top[1]),
                         self.sheet.Cells(right_bottom[0], right_bottom[1])).Value = value

    def used_range(self):
        return self.sheet.UsedRange.Rows.Count

    def get_row_data(self, row_no):
        return self.sheet.UsedRange.Rows[row_no-1].Value[0]  # here row no starts at 0

    def get_cell_value(self, row, col):
        return self.sheet.Cells(row, col).Value

    def get_cell_color(self, row, col):
        return self.sheet.Cells(row, col).Interior.ColorIndex

    def set_row_color(self, row_no, color_index):
        self.sheet.UsedRange.Rows[row_no].Interior.ColorIndex = color_index

    def get_row_color(self, row_no):
        return self.sheet.UsedRange.Rows[row_no].Interior.ColorIndex

    def set_range_border(self,rng):
        for border_in in range(7, 13):
            rng.Borders(border_in).LineStyle = 1
            rng.Borders(border_in).weight = 2

    def get_range(self, left_top, right_bottom):
        return self.sheet.Range(self.sheet.Cells(left_top[0], left_top[1]),
                                self.sheet.Cells(right_bottom[0], right_bottom[1]))

    def save_as(self, file_name):
        """file_name can contain directory if you do not want
        your file to be saved in current directory"""
        self.workbook.SaveAs(unicode(file_name, "utf-8"))

    def quit(self):
        self.app.Save()
        self.app.Quit()

    def quit_without_save(self):
        """just close the file and do not save any changes"""
        self.app.Quit()