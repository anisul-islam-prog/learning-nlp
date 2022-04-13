from mysql_manager import MySQLManager
from scibert import SciBERT
import numpy as np
import pandas as pd
from scipy import spatial
import pickle
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns
import io
import base64

image_path = "static\\img"


def main(query):
    isMatched = match_job(query)
    if isMatched:
        return isMatched
    mysql = MySQLManager()
    data_2018 = mysql.select("2018")
    data_2019 = mysql.select("2019")
    data_2020 = mysql.select("2020")
    data_2021 = mysql.select("2021")
    # print(data_2021, flush=True)
    for item_2018 in data_2018:
        item_2018["vector"] = pickle.loads(item_2018["vector"])

    for item_2019 in data_2019:
        item_2019["vector"] = pickle.loads(item_2019["vector"])

    for item_2020 in data_2020:
        item_2020["vector"] = pickle.loads(item_2020["vector"])

    for item_2021 in data_2021:
        item_2021["vector"] = pickle.loads(item_2021["vector"])

    # print(data_2021)

    scibert = SciBERT()
    print("Enter 'q' to quit.", flush=True)
    while True:
        query = input("Enter your query: ")
        if query == "q":
            break
        vector = scibert.vectorize(query)
        res_2018 = pd.DataFrame(find(data_2018, vector))
        res_2019 = pd.DataFrame(find(data_2019, vector))
        res_2020 = pd.DataFrame(find(data_2020, vector))
        res_2021 = pd.DataFrame(find(data_2021, vector))

        res_2018.rename(columns={"mean": "mean_2018", "var": "var_2018"}, inplace=True)
        res_2018.drop(['std'], axis=1, inplace=True)
        print(res_2018.head())

        res_2019.rename(columns={"author": "author_2019", "mean": "mean_2019", "var": "var_2019"}, inplace=True)
        res_2019.drop(['std'], axis=1, inplace=True)
        print(res_2019.head())

        df_combined_v1 = res_2018.merge(res_2019, left_on='author', right_on='author_2019', how='inner')

        res_2020.rename(columns={"author": "author_2020", "mean": "mean_2020", "var": "var_2020"}, inplace=True)
        res_2020.drop(['std'], axis=1, inplace=True)
        print(res_2020.head())

        df_combined_v2 = df_combined_v1.merge(res_2020, left_on='author', right_on='author_2020', how='inner')

        res_2021.rename(columns={"author": "author_2021", "mean": "mean_2021", "var": "var_2021"}, inplace=True)
        res_2021.drop(['std'], axis=1, inplace=True)
        print(res_2021.head())

        df_combined = df_combined_v2.merge(res_2021, left_on='author', right_on='author_2021', how='inner')
        df_combined.drop(['author_2019', 'author_2020', 'author_2021'], axis=1, inplace=True)
        print(df_combined.head())

        model_mean = df_combined.groupby('author', sort=False).mean()[
            ['mean_2018', 'mean_2019', 'mean_2020', 'mean_2021']]
        print(model_mean.head())

        model_var = df_combined.groupby('author', sort=False).mean()[['var_2018', 'var_2019', 'var_2020', 'var_2021']]
        print(model_var.head())
        dy_line_plot("random plot", [0, 0, 0, 0], '0')
        c = input("plotting results? (y, n): ")
        if c == 'y':
            for index in range(0, 66):
                dy_line_plot(model_mean.index[index] + " Average Similarity", model_mean.iloc[index].values,
                             str(index) + "(1)")
                dy_line_plot(model_var.index[index] + " Varience", model_var.iloc[index].values, str(index) + "(2)")

        result = save_result(df_combined.iloc[:66, :].copy())
        print(result.head(1))
        # result.to_sql(con = my_conn, name = 'candidate', if_exists = 'append', index = False)
        mysql.delete_candidate()
        for i in range(66):
            record = {}
            record["author"] = result["Candidate"][i]
            record["mean"] = str(result["Average_Similarity"][i])
            record["meanimage"] = result["Image(Avg)"][i]
            record["var"] = str(result["Variance"][i])
            record["varimage"] = result["Image(Var)"][i]
            mysql.insert_candidate(record)
    print("Program ends", flush=True)


def match_job(query):
    # print("Here", flush=True);
    mysql = MySQLManager()
    data_2018 = mysql.select("2018")
    data_2019 = mysql.select("2019")
    data_2020 = mysql.select("2020")
    data_2021 = mysql.select("2021")
    for item_2018 in data_2018:
        item_2018["vector"] = pickle.loads(item_2018["vector"])
        # print(item_2018,  flush=True)
    for item_2019 in data_2019:
        item_2019["vector"] = pickle.loads(item_2019["vector"])

    for item_2020 in data_2020:
        item_2020["vector"] = pickle.loads(item_2020["vector"])

    for item_2021 in data_2021:
        item_2021["vector"] = pickle.loads(item_2021["vector"])

    scibert = SciBERT()
    vector = scibert.vectorize(query)
    res_2018 = pd.DataFrame(find(data_2018, vector))
    res_2019 = pd.DataFrame(find(data_2019, vector))
    res_2020 = pd.DataFrame(find(data_2020, vector))
    res_2021 = pd.DataFrame(find(data_2021, vector))

    res_2018.rename(columns={"mean": "mean_2018", "var": "var_2018",
                             "docs": "docs_2018"}, inplace=True)
    res_2018.drop(['std'], axis=1, inplace=True)

    res_2019.rename(columns={"author": "author_2019", "mean": "mean_2019", "var": "var_2019",
                             "university": "university_2019", "docs": "docs_2019"}, inplace=True)
    res_2019.drop(['std'], axis=1, inplace=True)

    df_combined_v1 = res_2018.merge(res_2019, left_on=['author', 'university'],
                                    right_on=['author_2019', 'university_2019'],
                                    how='inner')
    # print(df_combined_v1, flush=True)
    # exit(0)
    res_2020.rename(columns={"author": "author_2020", "mean": "mean_2020", "var": "var_2020",
                             "university": "university_2020", "docs": "docs_2020"}, inplace=True)
    res_2020.drop(['std'], axis=1, inplace=True)

    df_combined_v2 = df_combined_v1.merge(res_2020, left_on=['author', 'university'],
                                          right_on=['author_2020', 'university_2020'], how='inner')

    res_2021.rename(columns={"author": "author_2021", "mean": "mean_2021", "var": "var_2021",
                             "university": "university_2021", "docs": "docs_2021"}, inplace=True)
    res_2021.drop(['std'], axis=1, inplace=True)

    df_combined = df_combined_v2.merge(res_2021, left_on=['author', 'university'],
                                       right_on=['author_2021', 'university_2021'], how='inner')
    df_combined.drop(['author_2019', 'author_2020', 'author_2021', 'university_2019', 'university_2020',
                      'university_2021'], axis=1, inplace=True)
    # print(df_combined, flush=True)
    # exit(0)
    model_mean = df_combined.groupby('author', sort=False).mean()[['mean_2018', 'mean_2019', 'mean_2020', 'mean_2021']]
    model_var = df_combined.groupby('author', sort=False).mean()[['var_2018', 'var_2019', 'var_2020', 'var_2021']]

    dy_line_plot("random plot", [0, 0, 0, 0], '0')
    for index in range(0, 66):
        dy_line_plot(model_mean.index[index] + " Average Similarity", model_mean.iloc[index].values, str(index) + "(1)")
        dy_line_plot(model_var.index[index] + " Varience", model_var.iloc[index].values, str(index) + "(2)")

    result = save_result(df_combined.iloc[:66, :].copy())
    mysql.delete_candidate()
    for i in range(66):
        record = {}
        record["author"] = result["Candidate"][i]
        record["university"] = result["university"][i]
        record["doc_count"] = str(result["Docs"][i])
        record["avg_sim"] = str(result["AVG_SIM"][i])
        record["mean"] = str(result["Average_Similarity"][i])
        record["meanimage"] = result["Image(Avg)"][i]
        record["var"] = str(result["Variance"][i])
        record["varimage"] = result["Image(Var)"][i]
        mysql.insert_candidate(record)
    print("Candidate data inserted", flush=True)
    return True


def dy_line_plot(author, heights, index):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax = sns.set_style(style="whitegrid")
    plt.rcParams.update({'figure.max_open_warning': 0})
    labels = ['2018', '2019', '2020', '2021']  # this is the years
    sns.lineplot(x=labels, y=heights)
    plt.title(author.title())
    # canvas = FigureCanvas(fig)    
    # img = io.BytesIO()
    # fig.savefig(img)
    # img.seek(0)
    # plt.plot(labels,heights)
    plt.savefig(image_path + '\\img-' + index + '.png')
    # plt.close()


def save_result(df):
    mean_list = []
    var_list = []
    mean_image_list = []
    var_image_list = []
    docs_list = []
    avg_mean_list=[]
    for i in range(0, 66):
        mean_tuple = (df["mean_2018"][i], df["mean_2019"][i], df["mean_2020"][i], df["mean_2021"][i])
        avg_mean = sum(mean_tuple) / len(mean_tuple)
        avg_mean_list.append(avg_mean)
        mean_list.append(mean_tuple)
        var_list.append((df["var_2018"][i], df["var_2019"][i], df["var_2020"][i], df["var_2021"][i]))
        mean_image_list.append('/static/img/img-' + str(i) + '(1).png')
        var_image_list.append('/static/img/img-' + str(i) + '(2).png')
        # print(sum((df["docs_2018"][i], df["docs_2019"][i], df["docs_2020"][i], df["docs_2021"][i])), flush=True)
        # exit(0)
        docs_list.append(sum((df["docs_2018"][i], df["docs_2019"][i], df["docs_2020"][i], df["docs_2021"][i])))
    df.drop(["mean_2018", "mean_2019", "mean_2020", "mean_2021"], axis=1, inplace=True)
    df.drop(["var_2018", "var_2019", "var_2020", "var_2021"], axis=1, inplace=True)
    df.drop(["docs_2018", "docs_2019", "docs_2020", "docs_2021"], axis=1, inplace=True)
    df.rename(columns={'author': 'Candidate'}, inplace=True)
    df["Average_Similarity"] = mean_list
    df["Image(Avg)"] = mean_image_list
    df["Variance"] = var_list
    df["Image(Var)"] = var_image_list
    # new column code added here
    df["Docs"] = docs_list
    df["AVG_SIM"] = avg_mean_list
    # print(df, flush=True)
    # # print(mean_list, flush=True)
    # exit(0)
    return df


def find(data, vector):
    df_lst = []
    for item in data:
        sim = similarity(vector, item["vector"])
        df_lst.append((item["author"], item["university"], sim))
    df = pd.DataFrame(df_lst, columns=["author", "university", "similarity"])
    df['docs'] = df.groupby('author')['author'].transform('count')
    df_agg = df.groupby(by=["author", "university", "docs"]).similarity.agg(["mean", "std", "var"])
    df_agg.reset_index(inplace=True)
    df_agg.fillna(0, inplace=True)
    df_sorted = df_agg.sort_values(by=["mean", "std"], ascending=[False, True])
    return df_sorted.to_dict("records")


def similarity(a, b):
    return 1 - spatial.distance.cosine(a, b)


if __name__ == "__main__":
    query = "Machine Learning"
    main(query)
