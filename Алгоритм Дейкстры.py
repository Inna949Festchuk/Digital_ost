def find_lowest_cost_node(costs):
    lowest_cost=float('inf')
    lowest_cost_node=None
    for node in costs:
        cost=costs[node]
        if cost<lowest_cost and node not in processed:
            lowest_cost=cost
            lowest_cost_node=node
    return lowest_cost_node

besconech=float('inf')
#Известные веса ребер
costs={'A':5,'B':2,'C':besconech,'D':besconech,'fin':besconech}
#Сам граф с описанием соседних узлов и их веса из каждой точки
graph={'start':{'A':5,'B':2},'A':{'C':4,'D':2},'B':{'A':8,'D':7},'C':{'fin':3,'D':6},'D':{'fin':1},'fin':{}}
#Таблица родительских таблиц наилучшего маршрута
parents={'A':'start','B':'start','C':None,'D':None,'fin':None}
processed=[]
node = find_lowest_cost_node(costs)  #берем первый узел
while node is not None:   
    cost=costs[node]     #снимаем вес ребра
    neighbors=graph[node]   #узнаем соседей узла
    for n in neighbors.keys():   #ищем можно ли добраться до данного узла дешевле
        new_cost=cost+neighbors[n]
        if costs[n]>new_cost:
            costs[n]=new_cost
            parents[n]=node
    processed.append(node)  #Обозначаем узел  как проверенный
    node=find_lowest_cost_node(costs)


