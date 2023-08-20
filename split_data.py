import argparse
import pandas as pd 

def split_data(diff_types='changes'):
    df = pd.read_parquet(f'data/cmg-data-processed.parquet', engine='fastparquet')
    df = df.sort_values(by=['extract_level'])
    result = list()
    for _, row in df.iterrows():
        diff = list()
        for l in row['diff'].splitlines():
            if diff_types=='changes':
                if l.startswith('-') or l.startswith('+'):
                    diff.append(l)
            elif diff_types=='alldiffs':
                diff.append(l)
        doc = row['label'].split()
        if row['old_path_file'] == row['new_path_file']:
            file = row['new_path_file']
        else:
            if row['old_path_file'] is not None and row['new_path_file'] is not None:
                file = row['old_path_file'] + ' SEP ' + row['new_path_file']
            else:
                file = row['old_path_file'] if row['old_path_file'] is not None else row['new_path_file']
            print(file)
        file = file+ ' SEP'
        index = row['index'].replace('_file_fc_patch.csv','')
        code = file + '\n'.join(diff)
        code = code.split()
        result.append({'code_tokens':code,'docstring_tokens':doc,'index':index})
    train, val,test = result[:17848],result[17848:20398],result[20398:]
    import json
    def dump_to_file(obj, file):
        with open(file,'w+') as f:
            for el in obj:
                f.write(json.dumps(el)+'\n')
    dump_to_file(train,'data/train.jsonl')
    dump_to_file(test,'data/test.jsonl')
    dump_to_file(val,'data/valid.jsonl')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--diff_type", default='changes', type=str,
                        help="Diff type: get all diffs or only changes")
    
    args = parser.parse_args()
    
    split_data(args.diff_type)

if __name__ == "__main__":
    main()