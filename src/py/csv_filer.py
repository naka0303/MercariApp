import csv

class CsvFiler:

    # 商品情報から一番最初の商品を取得
    def get_first(self, all_name_price_removed):
        first_name_price = all_name_price_removed[0]
        first_name_price_list = []
        first_name_price_list.append(first_name_price)

        return first_name_price_list
    
    # 配列情報をcsvに出力
    def write_data(self, csv_path, csv_file , data, mode):
        with open(csv_path + '/' + csv_file, mode) as f:
            writer = csv.writer(f)

            if 'all_product' in csv_file:
                writer.writerows(data)
            else:
                writer.writerow(data)

    # メルカリ画面から取得した商品名と価格の配列から不要情報を除去
    def remove_unneeded(self, args, all_name_price_img):
        all_name_price_img_removed = []
        idx = 0
        for name_price_img in all_name_price_img:
            name = name_price_img[0]

            # 検索ワードが商品名にあるかチェック
            none_cnt = len([arg for arg in args if not arg in name])
            
            # 検索ワード全てが商品名にある場合のみ返す
            if none_cnt == 0:
                all_name_price_img_removed.append(name_price_img)

            idx += 1
        
        return all_name_price_img_removed
