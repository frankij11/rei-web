import panel as pn
import pandas as pd
import hvplot.pandas
import numpy as np
from rei import sdat
from rei import search_homes as s

auc = pd.concat([s.auction_hw(), s.auction_ac()])
redfin = s.redfin()
redfin = redfin.assign(url = redfin["url_see_http://www.redfin.com/buy-a-home/comparative-market-analysis_for_info_on_pricing"] )
pn.config.sizing_mode = 'stretch_width'


def comps(address="1303 Alberta Dr"):
    meta = sdat.sdat_query(where=sdat.where_meta(address))
    comps = sdat.sdat_comps(df=meta)
    try:
        meta = sdat.add_features(meta)
        comps = sdat.add_features(comps)
    except:
        pass
    app = pn.Card(
            pn.Column(
                pn.Card(meta[['address','price', 'sqft', 'acre']], title="Meta Data"),
                pn.Card(comps[['address','price','sqft','acre']], title="Comparable Data"),
                pn.Card(comps.hvplot(x='sqft', y='price', kind='scatter', color="basement"))
                )
        )
    return app

app = pn.template.BootstrapTemplate(title="KJ's REI APP", header_background='blue',header_color="red")

pg_comp_calc = pn.Column(pn.interact(comps, address="1303 Alberta Dr"))
pg_auc = pn.Column(
                pn.Card(pn.widgets.DataFrame(auc), title="Auction Properties")
            )
pg_redfin = pn.Column(
                pn.Card(pn.widgets.DataFrame(redfin[["address", "city","price", "square_feet", "url"]] ), title="Redfin Properties")
                )

app.main.append(
        pn.Tabs(
            ("Comp Calculaor", pg_comp_calc),
            ("Auction", pg_auc),
            ("Redfin" , pg_redfin)
            )
        )


app.servable("KJ's REI APP")

if __name__ == "__main__":
    app.show("KJ's REI APP")
    
