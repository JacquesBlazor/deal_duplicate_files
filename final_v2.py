import re
import os
import pickle
import pandas as pd

target = 'E:/.developing_env/duplicated_files/group_by/'
df = pd.read_csv('df_index.csv')

while not df.empty:
    eval_group_id = df['組別'].iloc[0]
    path_list = df[df['組別'] == eval_group_id]['路徑'].unique()
    path_groups = df[df['路徑'].isin(path_list) == True].groupby('路徑')

    reshape_frame = pd.DataFrame()
    file_name = None
    for path_name, path_frame in path_groups:
        if not file_name:
            file_name = ''.join(re.findall('[\u4e00-\u9fff]+|\w+|^[<>:/\|?*"]+', path_name))
        reshape_frame = pd.concat([reshape_frame, path_frame])
    group_numbers = reshape_frame['組別'].unique()
    file_path_name = os.path.join(target, '%05d.%05d.%s.csv' % (group_numbers[0], group_numbers[-1], file_name))

    try:
        reshape_frame = df[df['組別'].isin(group_numbers) == True].sort_values(['組別', '路徑'])
        reshape_frame.set_index('磁碟機根目錄', inplace=True)
        reshape_frame.to_csv(file_path_name, encoding='utf-8-sig')
    except Exception as e:
        print(f'嘗試儲存 {file_path_name} 時發生錯誤: {e}')
        break
    drop_indexes = df[df['組別'].isin(group_numbers) == True].index
    df.drop(drop_indexes, inplace=True)
    print(f'\n從{group_numbers[0]}組別開始共{len(group_numbers)}組別已刪除。還有 {len(df)}筆。')




