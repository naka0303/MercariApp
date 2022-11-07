import log_outputter
import csv

class CsvConditioning:

    # 商品情報から一番最初の商品を取得
    def get_first(self, all_name_price_removed):
        first = all_name_price_removed[0]
        name = first[0]
        price = first[1]

        print(name, price)
    
    # 配列情報をcsvに出力
    def write_data(self, csv_path, csv_file , all_name_price_removed):
        with open(csv_path + '/' + csv_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(all_name_price_removed)

    # メルカリ画面から取得した商品名と価格の配列から不要情報を除去
    def remove_unneeded(self, args, all_name_price):
        all_name_price_removed = []
        idx = 0
        for name_price in all_name_price:
            name = name_price[0]

            # 検索ワードが商品名にあるかチェック
            none_cnt = 0
            for arg in args:
                if (arg in name):
                    none_cnt += 1
                    break
            
            # 検索ワード全てが商品名に無ければ配列から削除
            if (none_cnt != 0):
                all_name_price_removed.append(name_price)

            idx += 1
        
        return all_name_price_removed
