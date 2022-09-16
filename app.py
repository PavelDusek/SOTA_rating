from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

users = ["user1", "user2", "user3"]

@app.route("/")
def info():
    return "Vyber uzivatele."

@app.route("/<user>/")
def info2(user):
    if not user in users:
        return "Spatny uzivatel"
    return "Vyber studii."

@app.route("/<user>/results")
def results(user):
    if not user in users:
        return "Spatny uzivatel"
    df = pd.read_csv(f"/app/{user}.csv")

    #better structure for jinja2 template:
    df_list = []
    for i, row in df.iterrows():
        df_list.append(
                {
                    'id': i,
                    'title': row['title'],
                    'journal': row['journals'],
                    'pubmed_id': row['pubmed_id'],
                    'doi': row['doi'],
                    'impact': row['impact'],
                    'originality': row['originality'],
                    }
                )
    return render_template("results.html", user = user, df = df_list)

@app.route("/<user>/<int:id>", methods= ['GET'])
def index(user, id):
    if not user in users:
        return "Spatny uzivatel"

    impact, orig = request.args.get("i"), request.args.get("o")
    if impact:
        impact = int(impact)
        df = pd.read_csv(f"/app/{user}.csv")
        df.loc[id, "impact"] = impact
        df.to_csv(f"/app/{user}.csv", index = False)
        print(impact)

    if orig:
        orig = int(orig)
        df = pd.read_csv(f"/app/{user}.csv")
        df.loc[id, "originality"] = orig
        df.to_csv(f"/app/{user}.csv", index = False)
        print(orig)

    df = pd.read_csv(f"/app/{user}.csv")
    row = df.loc[id]
    prev_article, next_article, abstract = -1, len(df), ""
    if id >= 1: prev_article = id - 1
    if id < len(df): next_article = id + 1
    journal, title, pubmedid, doi, impact, orig = row['journals'], row['title'], row['pubmed_id'], row['doi'], row['impact'], row['originality']

    with open(f"/app/abstracts/{id}.txt", encoding="utf-8") as f:
            abstract = f.read()

    return render_template("pubmed.html",
            user = user,
            journal = journal,
            title = title,
            pubmedid = pubmedid,
            doi = doi,
            prev_article = prev_article,
            next_article = next_article,
            id = id,
            n = len(df)-1,
            abstract = abstract,
            impact = impact,
            orig = orig,
            )

if __name__ == "__main__":
    app.run(debug = True)
