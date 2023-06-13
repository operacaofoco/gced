#%%
import pandas as pd
import numpy as np
import plotly.express as px
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
df.drop_duplicates('id', inplace=True)

df['pegou'] = pd.to_datetime(df['pegou'], dayfirst=True)
df['subiu'] = pd.to_datetime(df['subiu'], dayfirst=True)
df = df[['subiu','posto','camera','user','rotina','pegou','ref','cse','id']]
df['adido']= df['user'].str.len()<8
df.set_index('id', inplace= True)
df.replace({'posto':postos}, inplace=True)
df
#%%
df['dia pegou'] = df['pegou'].dt.date
df['hora pegou'] = df['pegou'].dt.hour
df['mes pegou'] = (df['pegou'].dt.year.astype(str)+'-'+df['pegou'].dt.month.astype(str)).astype(str)
df['dia subiu'] = df['subiu'].dt.date
df['hora subiu'] = df['subiu'].dt.hour
df.shape
# %%
df['tempo para subir'] =  (df['subiu'] - df['pegou']).apply(lambda td: td / np.timedelta64(1, 'h') )
df
# %%
df[['posto','adido']].value_counts()
# %%
df['tempo para subir'].hist(by=df['posto'], sharex=True, sharey=False)
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
df4b = df4.pivot(index='dia pegou', columns='posto', values='tempo para subir')

df4b.plot.bar(stacked=True, figsize=(15,10))
# %%
for posto in df['posto'].unique():
    for adido in ['todos','militar','civil']:
        df5x = df
        if adido != 'todos':
            df5x = df[df['adido'] == (adido == 'militar')]
        print(posto, adido, df5x.shape)
        df5x = df5x[df5x['posto'] == posto]
        if df5x.shape[0]:
            df5 = pd.DataFrame(df5x[['dia pegou','hora pegou','posto']].groupby(['hora pegou','dia pegou']).count()['posto']).reset_index()
            df5 = df5[df5['dia pegou'].astype(str) >= '2023-04-25']
            df5b = df5.pivot(index='dia pegou', columns='hora pegou', values='posto')/2
            fig = px.imshow(df5b, text_auto=True, title=posto+' '+adido)
            fig.write_image(f'img/{posto}_{adido}.png')
            fig.show()
# %%
df6 = pd.DataFrame(df[['dia pegou','hora pegou','posto']].groupby(['hora pegou','dia pegou']).count()['posto']).reset_index()
df6 = df6[df6['dia pegou'].astype(str) >= '2023-05-01']
#df6 = df6[df6['dia pegou'].astype(str) < '2023-06-01']
df6b = df6.pivot(index='dia pegou', columns='hora pegou', values='posto')/2
fig = px.imshow(df6b, text_auto=True, title='Todos os postos')
fig.write_image(f'img/todos_postos.png')
fig.show()
# %%
df
# %%
for posto in df['posto'].unique():
    df7x = df[df['posto'] == posto]
    df7 = pd.DataFrame(df7x[['dia subiu','hora subiu','posto']].groupby(['hora subiu','dia subiu']).count()['posto']).reset_index()
    df7 = df7[df7['dia subiu'].astype(str) >= '2023-05-07']
    df7b = df7.pivot(index='dia subiu', columns='hora subiu', values='posto')
    fig = px.imshow(df7b, text_auto=True, title=posto)
    fig.show()
# %%
df8 = df[df['dia pegou'].astype(str) >= '2023-05-15']
df8 = pd.DataFrame(df8[['dia pegou','user','posto']].groupby(['user','dia pegou']).count()['posto']).reset_index()
df8b = df8.pivot(index='user', columns='dia pegou', values='posto')
fig = px.imshow(df8b, text_auto=True, title='Todos os postos')
fig.show()
# %%
df8.sort_values('posto')
# %%
df8b.to_excel('data/usuarios.xlsx')
# %%
df7 = pd.DataFrame(df[['dia subiu','hora subiu','posto']].groupby(['hora subiu','dia subiu']).count()['posto']).reset_index()
df7 = df7[df7['dia subiu'].astype(str) >= '2023-05-07']
df7b = df7.pivot(index='dia subiu', columns='hora subiu', values='posto')
fig = px.imshow(df7b, text_auto=True, title=posto)
fig.write_image('img/upload.png')
fig.show()

