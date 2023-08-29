import pandas as pd

def auto_preprocess(df1, target_col, missing_threshold=0.5):
    # Drop columns with high percentage of missing values
    # missing_percentage = df.isna().sum() / len(df)
    # drop_cols = list(missing_percentage[missing_percentage > missing_threshold].index)
    # df = df.drop(drop_cols, axis=1)
    #
    # # Drop columns with high cardinality or unique values
    # cat_cols = list(df.select_dtypes(include=['object', 'category']).columns)
    # card_threshold = int(len(df) * 0.8)
    # drop_cols = []
    # for col in cat_cols:
    #     nunique = df[col].nunique()
    #     if nunique >= card_threshold:
    #         drop_cols.append(col)
    # df = df.drop(drop_cols, axis=1)
    #
    # # Drop ID and target columns
    # drop_cols = [col for col in df.columns if col.endswith('ID') or col == target_col]
    # df = df.drop(drop_cols, axis=1)
    #
    # convert all columns to numeric type, any non-numeric values will be replaced with NaN
    df = df1.select_dtypes(exclude=['datetime64']).copy()
    df = df.apply(pd.to_numeric, errors='coerce')

    # select only numeric columns
    # drop non-numeric columns and NaN values
    df = df.select_dtypes(include='number').dropna(axis=1, how='any')

    print(df)
    return df

def raw_data():
    import pymongo

    return "success"

def GetClientUpdateByComapnyCode():
    from pymongo import MongoClient,DESCENDING
    clientUpdate = MongoClient("mongodb://10.10.54.57:15115")
    mydb = clientUpdate["KTBXPXCGZB"]
    mycol = mydb["productionData"]
    df=pd.DataFrame(mycol.find({},{"_id":0}).sort("dateTime", DESCENDING).limit(10))
    p_df=auto_preprocess(df,"predictionResult",0.5)
    return clientUpdate

GetClientUpdateByComapnyCode();