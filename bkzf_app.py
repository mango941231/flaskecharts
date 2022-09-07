from random import randrange
from flask import Flask, render_template
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from get_data import *
from datetime import datetime

app = Flask(__name__, static_folder="templates")


def bar_base() -> Bar:
    xaxis, yaxis = get_everyday_avg_price()
    c = (
        Bar()
        .add_xaxis(xaxis)
        .add_yaxis("二手房", [round(sum(i) / len(i), 2) for i in yaxis])
        .add_yaxis("房量", [len(i) for i in yaxis])
        .set_global_opts(title_opts=opts.TitleOpts(title="青岛房价走势柱状图", subtitle="十梅庵区域每日房价均值"))
    )
    return c


def line_base() -> Line:
    xaxis, yaxis = get_everyday_avg_price()
    c = (
        Line(init_opts=opts.InitOpts(width="1000px", height="600px"))
        .add_xaxis(xaxis_data=xaxis)
        .add_yaxis(
            series_name="二手房",
            y_axis=[round(sum(i) / len(i), 2) for i in yaxis],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="青岛房价走势折线图", subtitle="十梅庵区域每日房价均值"),
            # tooltip_opts=opts.TooltipOpts(trigger="axis"),
            # toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
        )
    )
    return c


def line_base_xqcjjl() -> Line:
    result = get_xq_cjjl()
    for k, v in result.items():
        b = {}
        for i in v:
            bk = ''.join(i[0].split('.')[:-1])
            if b.get(bk) == None:
                b[bk] = []
            b[bk].append(i[1])
        for c, j in b.items():
            b[c] = int(sum(j) / len(j))
        result[k] = b
    year = datetime.now().year
    month = datetime.now().month
    all_month = []
    for i in range(2013, year + 1):
        for j in range(1, 13):
            all_month.append(str(i) + str('0' + str(j) if len(str(j)) == 1 else j))
            if i == year and j == month:
                break
    for key, val in result.items():
        y = [None] * len(all_month)
        for k, v in dict(val).items():
            if k in all_month:
                index = all_month.index(k)
                y[index] = v
        result[key] = y
    c = (
        Line(init_opts=opts.InitOpts(width="1000px", height="600px"))
        .add_xaxis(xaxis_data=all_month)
        .add_yaxis(
            series_name="湖山美地一期",
            y_axis=result['湖山美地一期'],
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'), opts.MarkPointItem(type_='max')]),
            is_connect_nones=True,
        )
        .add_yaxis(
            series_name="湖山美地二期",
            y_axis=result['湖山美地二期'],
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'), opts.MarkPointItem(type_='max')]),
            is_connect_nones=True,
        )
        .add_yaxis(
            series_name="春和景明一期",
            y_axis=result['春和景明一期'],
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'), opts.MarkPointItem(type_='max')]),
            is_connect_nones=True,
        )
        .add_yaxis(
            series_name="春和景明二期",
            y_axis=result['春和景明二期'],
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='min'), opts.MarkPointItem(type_='max')]),
            is_connect_nones=True,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="青岛房价走势折线图", subtitle="青岛小区多年房价走势图"),
            # tooltip_opts=opts.TooltipOpts(trigger="axis"),
            # toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            datazoom_opts=[
                opts.DataZoomOpts(range_start=0, range_end=100),
                opts.DataZoomOpts(type_="inside", range_start=0, range_end=100),
            ]
        )
    )
    return c


def xiaoqu_avg_price() -> Bar:
    xaxis, yaxis = get_xiaoqu_avg_price()
    c = (
        Bar()
        .add_xaxis(xaxis)
        .add_yaxis("房价均值", yaxis)
        .set_global_opts(title_opts=opts.TitleOpts(title="青岛房价走势柱状图", subtitle="十梅庵各小区房价均值排序"))
    )
    return c


@app.route("/1")
def index_bar():
    return render_template("index.html")


@app.route("/2")
def index_line():
    return render_template("index_line.html")


@app.route("/3")
def index_xq_avg_price():
    return render_template("index_xq_avg_price.html")


@app.route("/4")
def index_xq_avg_price():
    return render_template("index_line_xqcjjl.html")


@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()


@app.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options_with_quotes()


@app.route("/lineChart_xqcjjl")
def get_line_chart_xqcjjl():
    c = line_base_xqcjjl()
    return c.dump_options_with_quotes()


@app.route("/xq_avg_price")
def get_xq_avg_price_chart():
    c = xiaoqu_avg_price()
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5678, debug=True)
