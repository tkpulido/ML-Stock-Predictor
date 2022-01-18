from alpaca_trade_api.rest import REST, TimeFrame
import os
import datetime


sp500  =["MMM","AOS","ABT","ABBV","ABMD","ACN","ATVI","ADM","ADBE","AAP","AMD","AES","AFL","A","APD","AKAM","ALK","ALB","ARE","ALGN","ALLE","LNT","ALL","GOOGL","GOOG","MO","AMZN","AMCR","AEE","AAL","AEP","AXP","AIG","AMT","AWK","AMP","ABC","AME","AMGN","APH","ADI","ANSS","ANTM","AON","APA","AAPL","AMAT","APTV","ANET","AJG","AIZ","T","ATO","ADSK","ADP","AZO","AVB","AVY","BKR","BLL","BAC","BBWI","BAX","BDX","BRK.B","BBY","BIO","TECH","BIIB","BLK","BK","BA","BKNG","BWA","BXP","BSX","BMY","AVGO","BR","BRO","BF.B","CHRW","CDNS","CZR","CPB","COF","CAH","KMX","CCL","CARR","CTLT","CAT","CBOE","CBRE","CDW","CE","CNC","CNP","CDAY","CERN","CF","CRL","SCHW","CHTR","CVX","CMG","CB","CHD","CI","CINF","CTAS","CSCO","C","CFG","CTXS","CLX","CME","CMS","KO","CTSH","CL","CMCSA","CMA","CAG","COP","ED","STZ","CPRT","GLW","CTVA","COST","CTRA","CCI","CSX","CMI","CVS","DHI","DHR","DRI","DVA","DE","DAL","XRAY","DVN","DXCM","FANG","DLR","DFS","DISCA","DISCK","DISH","DG","DLTR","D","DPZ","DOV","DOW","DTE","DUK","DRE","DD","DXC","EMN","ETN","EBAY","ECL","EIX","EW","EA","LLY","EMR","ENPH","ETR","EOG","EFX","EQIX","EQR","ESS","EL","ETSY","RE","EVRG","ES","EXC","EXPE","EXPD","EXR","XOM","FFIV","FB","FAST","FRT","FDX","FIS","FITB","FRC","FE","FISV","FLT","FMC","F","FTNT","FTV","FBHS","FOXA","FOX","BEN","FCX","GPS","GRMN","IT","GNRC","GD","GE","GIS","GM","GPC","GILD","GPN","GL","GS","HAL","HBI","HAS","HCA","PEAK","HSIC","HES","HPE","HLT","HOLX","HD","HON","HRL","HST","HWM","HPQ","HUM","HBAN","HII","IBM","IEX","IDXX","INFO","ITW","ILMN","INCY","IR","INTC","ICE","IFF","IP","IPG","INTU","ISRG","IVZ","IPGP","IQV","IRM","JBHT","JKHY","J","SJM","JNJ","JCI","JPM","JNPR","KSU","K","KEY","KEYS","KMB","KIM","KMI","KLAC","KHC","KR","LHX","LH","LRCX","LW","LVS","LEG","LDOS","LEN","LNC","LIN","LYV","LKQ","LMT","L","LOW","LUMN","LYB","MTB","MRO","MPC","MKTX","MAR","MMC","MLM","MAS","MA","MTCH","MKC","MCD","MCK","MDT","MRK","MET","MTD","MGM","MCHP","MU","MSFT","MAA","MRNA","MHK","TAP","MDLZ","MPWR","MNST","MCO","MS","MSI","MSCI","NDAQ","NTAP","NFLX","NWL","NEM","NWSA","NWS","NEE","NLSN","NKE","NI","NSC","NTRS","NOC","NLOK","NCLH","NRG","NUE","NVDA","NVR","NXPI","ORLY","OXY","ODFL","OMC","OKE","ORCL","OGN","OTIS","PCAR","PKG","PH","PAYX","PAYC","PYPL","PENN","PNR","PBCT","PEP","PKI","PFE","PM","PSX","PNW","PXD","PNC","POOL","PPG","PPL","PFG","PG","PGR","PLD","PRU","PTC","PEG","PSA","PHM","PVH","QRVO","QCOM","PWR","DGX","RL","RJF","RTX","O","REG","REGN","RF","RSG","RMD","RHI","ROK","ROL","ROP","ROST","RCL","SPGI","CRM","SBAC","SLB","STX","SEE","SRE","NOW","SHW","SPG","SWKS","SNA","SO","LUV","SWK","SBUX","STT","STE","SYK","SIVB","SYF","SNPS","SYY","TMUS","TROW","TTWO","TPR","TGT","TEL","TDY","TFX","TER","TSLA","TXN","TXT","COO","HIG","HSY","MOS","TRV","DIS","TMO","TJX","TSCO","TT","TDG","TRMB","TFC","TWTR","TYL","TSN","USB","UDR","ULTA","UAA","UA","UNP","UAL","UPS","URI","UNH","UHS","VLO","VTR","VRSN","VRSK","VZ","VRTX","VFC","VIAC","VTRS","V","VNO","VMC","WRB","GWW","WAB","WBA","WMT","WM","WAT","WEC","WFC","WELL","WST","WDC","WU","WRK","WY","WHR","WMB","WLTW","WYNN","XEL","XLNX","XYL","YUM","ZBRA","ZBH","ZION","ZTS"]

def alpaca():
    return REST(
        base_url="https://paper-api.alpaca.markets",
        secret_key=os.environ.get("APCA_API_SECRET_KEY"),
        key_id=os.environ.get("APCA_API_KEY_ID"),
    )

def to_date(row):
    return (row.name.date().isoformat())

def process_symbol(symbol):
    daily = api.get_bars(symbol, TimeFrame.Day, start, end, adjustment='raw').df
    daily['date'] = daily.apply(lambda row: to_date(row), axis=1)
    daily = daily.set_index('date')
    for date in daily.index.tolist():
        fifteen = api.get_bars(symbol, TimeFrame.Fifteen, date, date, adjustment='raw').df
        # Remove pre-market
        fifteen = fifteen.loc[fifteen.index.time >= datetime.time(14,30)]
        # Remove post-market
        fifteen = fifteen.loc[fifteen.index.time <= datetime.time(20,45)]
        daily.loc[date, '15min_close'] = fifteen.iloc[0].close
        daily.loc[date, 'is_positive_start'] = bool(fifteen.iloc[0].close > fifteen.iloc[0].open)
        daily.loc[date, 'is_positive_end'] = bool(fifteen.iloc[0].close < daily.loc[date].close)
        daily.loc[date, '15min_volume'] = fifteen.iloc[0].volume
    with open("{}.csv".format(symbol), "w") as fp:
        daily.to_csv(fp)
        
end = datetime.date.today().isoformat()
start = (datetime.date.today() - datetime.timedelta(days=1000)).isoformat()
api = alpaca()

for symbol in sp500:
    process_symbol(symbol)