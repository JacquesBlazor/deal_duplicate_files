import os
import re
import pandas as pd

target = 'E:/.developing_env/duplicated_files/groupby_method/'
df = pd.read_csv('df_index.csv')

while not df.empty:
    eval_group_id = df['組別'].iloc[0]
    path_list = df[df['組別'] == eval_group_id]['路徑'].unique()
    path_groups = df[df['路徑'].isin(path_list) == True].groupby('路徑')
    for folder in folder_lists:
        if isinstance(df_index_drive_root.loc[folder], pd.core.frame.DataFrame):
            loc_folders[folder] = df_index_drive_root.loc[folder].groupby('檔案資料夾')
    reshape_frame = pd.DataFrame()
    for folder in loc_folders:
        for group_name, group_frame in loc_folders[folder]:
            reshape_frame = pd.concat([reshape_frame, group_frame])
    groups_dump = reshape_frame['組別'].unique()
    folder_name = ''.join(re.findall('[\u4e00-\u9fff]+|^[<>:/\|?*"]+', df[df['組別'] == eval_group_id]['磁碟機根目錄'].min()))
    file_path_name = os.path.join(target, f'{folder_name}{groups_dump[0]}{groups_dump[-1]}.csv')
    try:
        reshape_frame = df[df['組別'].isin(groups_dump) == True].sort_values(['組別', '路徑'])
        reshape_frame.set_index('磁碟機根目錄', inplace=True)
        reshape_frame.to_csv(file_path_name, encoding='utf-8-sig')
    except Exception as e:
        print(f'嘗試儲存 {file_path_name} 時發生錯誤: {e}')
        continue
    else:
        del df_index_drive_root
        del reshape_frame
        del loc_folders
        del folder_names
        df.drop(df[df['組別'].isin(groups_dump) == True].index, inplace=True)
        print(f'{groups_dump[0]}~{groups_dump[-1]}已刪除。還有 {len(df)}筆。')