#%%
import pandas as pd
import numpy as np

# %%

postos = {'SECCNHANGAPIDK1': 'Nhangapi', 
          'SECCMAROVERDE': 'Mato Verde',
          'SECCTIMBODK1': 'Timbó',
          'SECCLEVYGASPARIANDK1': 'Levy',
          'SECCANGRADOSREISDK1' : 'Angra',
          'SECCCICCDK1': 'Inteligência',
          'unpolice': 'Outros',
          'hikvision': 'Outros',
          'SECCOPERACAOFOCOMATOVERDE': 'Mato Verde'}

#%%
df = pd.read_excel('data/log_camera.xlsx', names = ['nada','subiu','posto','camera','user','rotina','pegou','ref','cse','id'],
                   parse_dates=['subiu','pegou'])
df.shape
# %%
df.drop_duplicates('id', inplace=True)
df = df[['subiu','posto','camera','user','rotina','pegou','ref','cse','id']]
df.set_index('id', inplace= True)
df.replace({'posto':postos}, inplace=True)
df['dia pegou'] = df['pegou'].dt.date
df.shape
# %%
df['tempo para subir'] =  (df['subiu'] - df['pegou']).apply(lambda td: td / np.timedelta64(1, 'h') )
df
# %%
df['posto'].value_counts()
# %%
df['tempo para subir'].hist(by=df['posto'], sharex=True, sharey=True)
# %%
# %%

# %%
df
# %%
df2 = pd.DataFrame(df[['posto','dia pegou','tempo para subir']].groupby(['posto','dia pegou']).mean()['tempo para subir']).reset_index()
df2 = df2[df2['dia pegou'].astype(str) > '2023-04-30']
df2.pivot(index='dia pegou', columns='posto', values='tempo para subir').plot()
# %%
df3 = pd.DataFrame(df[['posto','dia pegou','tempo para subir']].groupby(['posto','dia pegou']).max()['tempo para subir']).reset_index()
df3 = df3[df3['dia pegou'].astype(str) > '2023-04-30']
df3.pivot(index='dia pegou', columns='posto', values='tempo para subir').plot()
# %%
df4 = pd.DataFrame(df[['posto','dia pegou','tempo para subir']].groupby(['posto','dia pegou']).count()['tempo para subir']).reset_index()
df4 = df4[df4['dia pegou'].astype(str) > '2023-04-30']
df4.pivot(index='dia pegou', columns='posto', values='tempo para subir').plot()
# %%
