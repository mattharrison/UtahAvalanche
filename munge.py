import re

import pandas as pd

def get_df(fname):
    df = pd.read_csv(fname)
    # remove colons
    df2 = df.rename(columns={x:x.replace(':', '')
                             for x in df.columns})
    df2['depth_inches'] = df2.Depth.apply(to_inches)
    df2['depth_inches'] = df2.depth_inches.fillna(df2['depth_inches'].median())

    df2['date'] = pd.to_datetime(df2['Occurrence Date'])

    df2['year'] = df2['date'].apply(lambda x: x.year)
    df2['dow'] = df2['Occurrence Date'].apply(lambda x: x.split(',')[0])

    df2['slope'] = df2['Slope Angle'].fillna(df2['Slope Angle'].median())

    df2['vert'] = df2.Vertical.str.replace('Unknown', 'NaN').astype(float)
    df2['vert'] = df2.vert.fillna(df2.vert.median())

    df2['injured'] = df2.Injured.fillna(0)

    df2['lat'] = df2.coordinates.apply(lambda x: float(x.split(',')[0]) if str(x) != 'nan' else float('nan'))
    df2['lon'] = df2.coordinates.apply(lambda x: float(x.split(',')[1]) if str(x) != 'nan' else float('nan'))

    df2['elevation'] = df2.Elevation.str.replace('Unknown', 'NaN').astype(float)
    df2['elevation'] = df2.elevation.fillna(df2.elevation.median())
    return df2

def to_inches(orig):
    """
    >>> to_inches("3'")
    36
    """
    r = r'''(((\d*\.)?\d*)')?(((\d*\.)?\d*)")?'''
    regex = re.compile(r)
    txt = str(orig)
    if txt == 'nan':
        return orig
    # if str(float(txt)) == 'nan':
    #     return txt
    match = regex.search(txt)
    groups = match.groups()
    feet = groups[1] or 0
    inches = groups[4] or 0
    return float(feet) * 12 + float(inches)



if __name__ == '__main__':
    df = get_df('/tmp/ava.csv')
