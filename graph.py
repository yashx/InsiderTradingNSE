import os
import copy
from matplotlib import pyplot as plt
from numpy.core.fromnumeric import sort

plt.style.use('dark_background')

def plotCompanyConsolidated(df, graph_title, saveImage=False):
    groups = df.groupby("symbol")
    _handleGroups(groups, graph_title, saveImage)

def plotTargetCompanyByDate(df,sym, graph_title, saveImage=False):
    df = df[df["symbol"]==sym]
    groups = df.groupby("acqtoDt")
    _handleGroups(groups, graph_title, saveImage)    

def _handleGroups(grps, graph_title, saveImage=False):
    dataToPlot = {}

    print("\n\n")
    
    for g_name, g_df in grps:
        try:
            print(g_name.strftime("%d %b %Y"))
        except:
            print(g_name)
        print("")
        sub_groups = g_df.groupby("tdpTransactionType")
        dataToPlot[g_name] = (sub_groups.secAcq.sum().to_dict())

        print("Shares")
        for sg_name, sg_df in sub_groups:
            n, s = sg_name, sg_df.secAcq.sum() 
            ns = "Bought" if n=="Buy" else ("Sold" if(n == "Sell") else n)

            print(f"{ns}:{s} Worth: {sg_df.secVal.sum()}")

        print("\n")
        print("Method used")
        for k,v in (g_df["acqMode"].value_counts().to_dict().items()):
            print(f"{k}: {v}")

        print("")
        print("Transacions Done By Entity Category")
        for k,v in (g_df["personCategory"].value_counts().to_dict().items()):
            print(f"{k}: {v}")

        print("")
        print("Transacions Done By Entity Name")
        for k,v in (g_df["acqName"].value_counts().to_dict().items()):
            print(f"{k}: {v}")
        
        print("")
        sub_groups = g_df.groupby("acqName")

        print("Transactions By")
        print("")
        for sg_name, sg_df in sub_groups:
            print(f"{sg_name}: ") 
            sub_df = (sg_df[['tdpTransactionType', 'secAcq','secVal', 'acqfromDt', 'acqtoDt', 'intimDt', 'acqMode']])
            sub_df = sub_df.rename(columns={'tdpTransactionType':'Type', 'secAcq':'Qty', 'acqfromDt':'From', 'acqtoDt':'To', 'intimDt':'Declared', 'acqMode':'Mode', 'secVal':'Value'})
            print(sub_df.to_string(index=False, justify="center"))
            print("")

        print("\n\n")
    fig, ax = plt.subplots(2)
    _plotBuySellGraph(dataToPlot, ax[0])
    _plotPledgeRevokeInvokeGraph(dataToPlot, ax[1])
    fig.suptitle(graph_title)
    fig.tight_layout()
    if saveImage:
        print("Saving Image of Graph")
        path = f"img/{graph_title}.png"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        fig.savefig(path, bbox_inches='tight', dpi=1000)
    plt.show()


def _plotBuySellGraph(d, ax):
    """Plots Buy Sell Graph

    Args:
        d (Dictionary): Should be a dictionary with objects of following structure '63MOONS': {'Buy': 60543, 'Sell': 60543}
    """
    width = 0.45
    data = copy.copy(d)
    for k,v in d.items():
        if not("Buy" in v or "Sell" in v):
            del data[k]

    labels = list(data.keys())
    try:
        labels = list(map(lambda d:d.strftime("%d %b %Y"),labels))
    except:
        pass
    ticks = range(len(labels))
    bought = []
    sold = []
    for d in data.values():
        bought.append(d.get("Buy",0))
        sold.append(d.get("Sell",0))
    ax.tick_params(axis="x", labelsize='small')
    ax.bar([x-(width/2)  for x in ticks], bought, width, label='Bought', log=True, color=['green'])
    ax.bar([x+(width/2)  for x in ticks], sold, width, label='Sold', log=True, color=['red'])

    ax.set_ylabel('Shares')
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, rotation=90)
    ax.legend()

def _plotPledgeRevokeInvokeGraph(d, ax):
    """Plots Pledge Revoke Invoke Graph

    Args:
        d (Dictionary): Should be a dictionary with objects of following structure '63MOONS': {'Buy': 60543, 'Sell': 60543}
    """
    width = 0.45
    data = copy.copy(d)
    for k,v in d.items():
        if not("Pledge Revoke" in v or "Pledge" in v):
            del data[k]

    labels = list(data.keys())
    try:
        labels = list(map(lambda d:d.strftime("%d %b %Y"),labels))
    except:
        pass
    ticks = range(len(labels))

    ticks = range(len(labels))
    revoke = []
    invoke = []
    for d in data.values():
        revoke.append(d.get("Pledge Revoke",0))
        invoke.append(d.get("Pledge",0))
    ax.tick_params(axis="x", labelsize='small')
    ax.bar([x-(width/2)  for x in ticks], revoke, width, label='Pledge Revoke', log=True, color=['green'])
    ax.bar([x+(width/2)  for x in ticks], invoke, width, label='Pledge Invoke', log=True, color=['red'])

    ax.set_ylabel('Shares')
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels, rotation=90)
    ax.legend()