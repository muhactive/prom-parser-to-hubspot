from parser import find_product_info
import json
import pandas as pd

if __name__ == "__main__":
    
    all_info_products = list(find_product_info())

    with open("product.json", "w", encoding="utf-8") as f:
        json.dump(all_info_products, f, ensure_ascii=False, indent=4)
        
    data_save = pd.DataFrame(all_info_products)
    data_save.to_csv("products.csv", index=False)
    data_save.to_excel("products.xlsx", index=False)

    print(f"Собрано всего {len(all_info_products)} товаров")


main()