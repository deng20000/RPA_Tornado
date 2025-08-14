from google_data import create_sheet_dict

def test_create_sheet_dict():
    excel_file = "c:\\Users\\gl-02251756\\Desktop\\rpa\\google_watch\\2025-06-11 Google Ads数据查看.xlsx"
    sheet_dict = create_sheet_dict(excel_file)
    
    print("表名字典:")
    for key, value in sheet_dict.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    test_create_sheet_dict()