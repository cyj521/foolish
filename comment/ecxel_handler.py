import os

import openpyxl


class ExcelHandler:
    def __init__(self,excel_name):
        self.path=excel_name
        self.workbook=None

    def open_excel(self):
        # 打开excel
        self.workbook=openpyxl.load_workbook(self.path)
        return self.workbook

    def get_sheet(self,sheet_name):
        # 获取sheet表单
        workbook=self.open_excel()
        return workbook[sheet_name]

    def read_sheet(self,sheet_name):
        # 读取sheet页用例
        sheet=self.get_sheet(sheet_name)
        title=[]
        lis=[]
        rows=list(sheet.rows)
        for title_1 in rows[0]:
            title.append(title_1.value)

        for row in rows[1:]:
            dic={}
            for inx,data in enumerate(row):
                dic[title[inx]]=data.value
            lis.append(dic)
        return lis

    def write_sheet(self,sheet_name,row,colucm,information):
        # 写入数据到sheet页
        sheet=self.get_sheet(sheet_name)
        cell=sheet.cell(row,colucm).value=information
        self.save_excel()
        self.close_excel()
        return cell

    def save_excel(self):
        # 保存excel
        self.workbook.save(self.path)

    def close_excel(self):
        # 关闭excel
        self.workbook.close()


if __name__ == "__main__":
    pass
    # cases_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print(cases_path)
    # a=os.path.join(cases_path,"tests_case")
    # b=os.path.join(a,"cases.xlsx")
    # excel = ExcelHandler(b)
    # excel.get_sheet("register")
    # excel.write_sheet("register",25,10,10)


