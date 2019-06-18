import requests
import itertools
import pandas as pd
from sync_api.demo_public import OneToken
# 图的节点结构
class Node:
    def __init__(self, exchange,name):
        self.exchange = exchange
        self.name = name      # 节点值

        self.come= {}      #入节点，边：dict:名称:节点，边 ,入度
        self.out = {}      #出节点，边：dict:名称:节点，边 ,入度
        self.come['count'] = 0
        self.out['count'] = 0

# 图的边结构
class Edge:
    def __init__(self,fro, to,rate = {}):
        self.fro = fro              # 边的from节点
        self.to = to                # 边的to节点

        self.rate = rate

def get_price(contract):
    print(contract)
    res = requests.get( 'https://1token.trade/api/v1/quote/single-tick/okex/{}'.format(contract) )
    #print(res.json())

    bid = res.json()['bids'][0]['price']
    ask = res.json()['asks'][0]['price']

    return bid,ask
    #
    # if not self.invert:
    #     self.price = res.json()['bids'][0]['price']
    # else:
    #     self.price = 1 / res.json()['asks'][0]['price']
    #
    # self.value = self.price * (1 - self.taker_commition)

# 图结构
class Graph:
    def __init__(self):
        self.nodes = {}     # 图的所有节点集合  字典形式：{节点编号：节点}
        self.edges = {}    # 图的边集合


# 生成图结构
# matrix = [
#   [1,2,3],        ==>   里面分别代表权重, from节点, to节点
#   [...]
# ]

'''
def createGraph(matrix):
    graph = Graph()
    for edge in matrix:
        weight = edge[0]
        fro = edge[1]
        to = edge[2]
        if fro not in graph.nodes:
            graph.nodes[fro] = Node(fro)
        if to not in graph.nodes:
            graph.nodes[to] = Node(to)
        fromNode = graph.nodes[fro]
        toNode = graph.nodes[to]
        newEdge = Edge(weight, fromNode, toNode)
        fromNode.nexts.append(toNode)
        fromNode.out += 1
        toNode.come += 1
        fromNode.edges.append(newEdge)
        graph.edges.append(newEdge)
    return graph
'''
def createGraph():
    pass

def demo():
    DEBUG = True
    onetoken = OneToken()

    exchange = onetoken.exchanges
    okex_contracts = onetoken.contracts['okex']['name']
    okex_tickets = onetoken.get_quote_tickets('okex')
    print(okex_tickets)
    okex_tickets['ask_price'] = list(map(lambda x: x[0]['price'], okex_tickets['asks']))
    okex_tickets['ask_volume'] = list(map(lambda x: x[0]['volume'], okex_tickets['asks']))
    okex_tickets['bid_price'] = list(map(lambda x: x[0]['price'], okex_tickets['bids']))
    okex_tickets['bid_volume'] = list(map(lambda x: x[0]['volume'], okex_tickets['bids']))
    del okex_tickets['asks']
    del okex_tickets['bids']
    print(okex_tickets)

    graph = Graph()

    for contract in okex_contracts:
        pair = contract.split( '.' )

        ask_price = okex_tickets['ask_price'][okex_tickets['contract'] == ('okex/'+contract )]
        bid_price = okex_tickets['bid_price'][okex_tickets['contract'] ==('okex/'+contract) ]

        if not pair[0] in graph.nodes.keys():
            graph.nodes[pair[0]] = Node('okex', pair[0] )
        if not pair[1] in graph.nodes.keys():
            graph.nodes[pair[1]] = Node('okex', pair[1])

        Node0 = graph.nodes[pair[0]]
        Node1 = graph.nodes[pair[1]]

        newEdge0 = Edge( Node0, Node1)
        newEdge1 = Edge(Node1, Node0)

        newEdge0.rate['ask_price'] = ask_price
        newEdge0.rate['bid_price'] = bid_price

        newEdge1.rate['ask_price'] = 1 / bid_price
        newEdge1.rate['bid_price'] = 1 / ask_price

        Node0.out[pair[1]] = {}
        Node0.out[pair[1]]['node'] = Node1
        Node0.out[pair[1]]['edge'] = newEdge0
        Node0.out['count'] +=1

        Node0.come[pair[1]] = {}
        Node0.come[pair[1]]['node'] = Node1
        Node0.come[pair[1]]['edge'] = newEdge1
        Node0.come['count'] += 1

        Node1.out[pair[0]] = {}
        Node1.out[pair[0]]['node'] = Node0
        Node1.out[pair[0]]['edge'] = newEdge0
        Node1.out['count'] +=1

        Node1.come[pair[0]] = {}
        Node1.come[pair[0]]['node'] = Node0
        Node1.come[pair[0]]['edge'] = newEdge0
        Node1.come['count'] +=1

        graph.edges[pair[0], pair[1]] = ( newEdge0 )
        graph.edges[pair[1], pair[0]] = (newEdge1)

    print( 'End' )


if __name__ == '__main__':
    demo()