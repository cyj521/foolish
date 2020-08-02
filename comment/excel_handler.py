# 创建一个excel读取操作的类
import openpyxl


class ExcelHandler:

    # 初始化一个工作簿
    def __init__(self,file_name):
        self.file=file_name
        self.workbook=None

    # 打开文件
    def open_excel(self):
        self.workbook=openpyxl.load_workbook(self.file)
        return self.workbook

    # 打开sheet表单
    def get_sheet(self,sheet_name):
        workbook=self.open_excel()
        return workbook[sheet_name]

    # 读取sheet表单的数据
    def read_sheet(self,sheet_name):
        sheet=self.get_sheet(sheet_name)
        title = []
        lis = []
        rows = list(sheet.rows)
        for title_1 in rows[0]:
            title.append(title_1.value)

        for row in rows[1:]:
            dic = {}
            for inx, data in enumerate(row):
                dic[title[inx]] = data.value
            lis.append(dic)
        return lis

    # 写入数据到excel
    def write_excel(self,sheet_name,row,colucm,information):
        sheet=self.get_sheet(sheet_name)
        cell=sheet.cell(row,colucm).value=information
        self.save_excel()
        self.close_excel()
        return cell

    # 保存excel
    def save_excel(self):
        self.workbook.save(self.file)

    # 关闭工作簿
    def close_excel(self):
        self.workbook.close()


if __name__ == '__main__':
    import os
    dir_case_pass=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(dir_case_pass)
    case_path=os.path.join(dir_case_pass,"test_data\cases_test.xlsx")
    print(case_path)
    excel=ExcelHandler(case_path)
    dir_data=excel.open_excel()
    data=excel.read_sheet("register")
    print(data)
    cell=excel.write_excel("register",2,10,"pass")
    pass





