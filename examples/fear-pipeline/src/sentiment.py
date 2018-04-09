"""
Copyright 2018 Banco Bilbao Vizcaya Argentaria, S.A.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import re
import pandas as pd

from spacy import load as spacy_load


def load_sentiment_model(sentiment_file_path):
    try:
        senti_raw = pd.read_csv(
            sentiment_file_path,
            sep="\t",
            names=["POS", "ID", "PosScore", "NegScore", "SynsetTerms", "Gloss"],
            skiprows=27,
            skipfooter=1,
            engine='python'
        )
        senti_raw = senti_raw[(senti_raw['PosScore'] + senti_raw['NegScore']) != 0]

        exploded = senti_raw['SynsetTerms'].apply(
            lambda x: re.split("\s+", x)
        ).apply(pd.Series)
        senti_exploded = pd.concat(
            [senti_raw[["PosScore", "NegScore"]], exploded],
            axis=1
        )
        senti_norm = pd.melt(
            senti_exploded,
            id_vars=["PosScore", "NegScore"],
            value_vars=range(0, 25)
        )
        senti_norm = senti_norm[senti_norm['value'].notnull()]
        senti_norm['value'] = senti_norm['value'].apply(
            lambda x: re.sub("#\d+", "", x)
        )
        df_senti = senti_norm.groupby("value").mean()
        df_senti['NegScore'] = df_senti['NegScore'] * -1
        return df_senti['NegScore'].to_dict(), df_senti['PosScore'].to_dict()
    except:
        return None
