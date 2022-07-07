import pytextrank, spacy
import scattertext as st

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank", last=True)

convention_df = st.SampleCorpora.ConventionData2012.get_data().assign(
        parse=lambda df: df.text.apply(nlp),
        party=lambda df: df.party.apply(
            {'democrat': 'Democratic', 'republican': 'Republican'}.get)
        )
corpus = ( st.CorpusFromParsedDocuments(
                  convention_df,
                  category_col='party',
                  parsed_col='parse',
                  feats_from_spacy_doc=st.PyTextRankPhrases()
                )
              .build()
              .compact(
                    st.AssociationCompactor(2000, use_non_text_features=True)
                    )
        )
