import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import pyecharts.options as opts
from pyecharts.charts import Line,Pie
from pyecharts.faker import Faker

file1,file2=csv.reader(open('total_pop.csv','r')),csv.reader(open("aging_structure.csv", 'r'))
file3=csv.reader(open('NPGR.csv','r'))

# 处理人口性别比例、城乡比例数据
content=[line[1:] for line in file1][3:-2]
pop_data=[]
for line in content:
    line.reverse()
    pop_data.append(list(map(float,line)))

# 处理人口年龄比例数据
content=[line[1:] for line in file2][3:-3]
age_data=[]
for line in content:
    line.reverse()
    age_data.append(list(map(int,line)))

# 处理人口自然增长率数据
content=[line[1:] for line in file3][3:-2]
npgr_data=[]
for line in content:
    line.reverse()
    npgr_data.append(list(map(float,line)))

years=[str(year) for year in range(2009,2019)]

c1=(
    Line()
    .add_xaxis(years)
    .add_yaxis("男性人口",pop_data[1],is_smooth=True)
    .add_yaxis("女性人口",pop_data[2],is_smooth=True)
    .add_yaxis("总人口",pop_data[0],is_smooth=True)
    .set_global_opts(title_opts=opts.TitleOpts(title='2009-2018年间中国人口增长趋势图'))
    .render("Male_Female.html")
)

c2=(
    Line()
    .add_xaxis(years)
    .add_yaxis("城镇人口",pop_data[3],is_smooth=True)
    .add_yaxis("农村人口",pop_data[4],is_smooth=True)
    .set_global_opts(title_opts=opts.TitleOpts(title='2009-2018年间中国城乡人口变化趋势图'))
    .render("rural_urban.html")
)

c3=(
    Line()
    .add_xaxis(years)
    .add_yaxis("出生率",npgr_data[0],is_smooth=True,areastyle_opts=opts.AreaStyleOpts(opacity=0.2))
    .add_yaxis("死亡率",npgr_data[1],is_smooth=True,areastyle_opts=opts.AreaStyleOpts(opacity=0.2))
    .add_yaxis("自然增长率",npgr_data[2],is_smooth=True,areastyle_opts=opts.AreaStyleOpts(opacity=0.2))
    .set_global_opts(title_opts=opts.TitleOpts(title='2009-2018年间\n中国人口自然增长率变化趋势'))
    .set_colors(['#5bc49f','#ff7c7c','black'])
    .render("NPGR.html")
)

inner_x_data=['0-14岁人口(万人)','15-64岁人口(万人)','64岁以上(万人)']
inner_y_data=[data for data in (line[0] for line in age_data[1:4])]
inner_data_pair=[list(z) for z in zip(inner_x_data,inner_y_data)]

outer_x_data=inner_x_data
outer_y_data=[data for data in (line[-1] for line in age_data[1:4])]
outer_data_pair=[list(z) for z in zip(outer_x_data,outer_y_data)]

(
    Pie(init_opts=opts.InitOpts(width='1000px',height='800px'))
    .add(
        series_name='2009年年龄结构',
        data_pair=inner_data_pair,
        radius=[0,'40%'],
        label_opts=opts.LabelOpts(position='inner'),
    )
    .add(
        series_name='2018年年龄结构',
        radius=['50%','65%'],
        data_pair=outer_data_pair,
        label_opts=opts.LabelOpts(
            position='outside',
            formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%} ",
            background_color='#eee',
            border_color='#aaa',
            border_width=1,
            border_radius=4,
            rich={
                "a":{"color": "#999", "lineHeight": 22, "align": "center"},
                "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                     },
                "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                "b":{"fontSize": 16, "lineHeight": 33},
                "per":{
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
            },
        ),
    )
    .set_global_opts(legend_opts=opts.LegendOpts(pos_left='left',orient='vertical'))
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger='item',formatter="{a} <br/>{b}: {c} ({d}%)"
        )
    )
    .set_colors(['#60acfc','#32d3eb','#5bc49f'])
    .render('age_ratio.html')
)
