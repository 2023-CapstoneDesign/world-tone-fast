import os

def delete_files_in_folder(folder_path):
    try:
        # 해당 폴더의 모든 파일 리스트 가져오기
        file_list = os.listdir(folder_path)

        # 각 파일에 대해 순회하며 삭제
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            os.remove(file_path)
            print(f"{file_path} 삭제 완료")

        print(f"{folder_path} 폴더 내의 모든 파일 삭제 완료")

    except Exception as e:
        print(f"오류 발생: {e}")