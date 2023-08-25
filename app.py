import panel as pn
import pandas as pd
import hvplot.pandas
import holoviews as hv
import numpy as np
import ipyleaflet as leaflet

from rei import sdat
from rei import search_homes as s

pn.extension("perspective")

auc = pd.concat([s.auction_hw(), s.auction_ac()])
#auc_comps = sdat.Homes(auc.address)
redfin = s.redfin()
redfin = redfin.assign(url = lambda x: x.filter(regex="url_*"))
pn.config.sizing_mode = 'stretch_width'


def comps(address="1303 Alberta Dr"):
    meta = sdat.sdat_query(where=sdat.where_meta(address))
    comps = sdat.sdat_comps(df=meta, year=2023)
    try:
        meta = sdat.add_features(meta)
        comps = sdat.add_features(comps)
    except:
        pass

    cols = ['address','yearSold','price', 'sqft', 'acre','basement','style','type', 'url']

    app = pn.Card(
            pn.Column(
                pn.Card(meta[cols], title="Meta Data"),
                pn.Card(
                    comps.query("sqft >@meta.sqft.max()*.8 and sqft <@meta.sqft.max()*1.2").price.describe(), title="ARV"
                    ),
                pn.Card(comps.hvplot(x='sqft', y='price', kind='scatter', color="basement") *\
                       hv.VLine(meta.sqft.max(), color='blue')),
                pn.Card(pn.pane.Perspective(comps[cols]), title="Comparable Data")
                
                )
        )
    return app

app = pn.template.BootstrapTemplate(title="KJ's REI APP", header_background='blue',header_color="red")

pg_comp_calc = pn.Column(pn.interact(comps, address="1303 Alberta Dr"))


#map_auction = leaflet.Map().add_layer()
pg_auc = pn.Column(
                #pn.Card(pn.panel(map_auction)),
                pn.Card(pn.pane.Perspective(pn.widgets.DataFrame(auc)), title="Auction Properties")
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
    
