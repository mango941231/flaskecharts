from random import randrange
from flask import Flask, render_template
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from get_data import *

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


@app.route("/barChart")
def get_bar_chart():
    c = bar_base()
    return c.dump_options_with_quotes()


@app.route("/lineChart")
def get_line_chart():
    c = line_base()
    return c.dump_options_with_quotes()


@app.route("/xq_avg_price")
def get_xq_avg_price_chart():
    c = xiaoqu_avg_price()
    return c.dump_options_with_quotes()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5678, debug=True, threading=True)
