import json

from movies.utils import get_avg_rating_data, get_movie_release_each_year_data


class BaseChart:
    def __init__(self, **kwargs):
        self.filters = kwargs['filters']
        self.chart = {}
        self.set_base_chart()

    def set_base_chart(self):
        self.chart = {
            "legend": {
                "show": True,
                "type": "scroll",
                "orient": "horizontal",
                "selectedMode": True,
                "top": "bottom",
                "left": "center",
                "itemGap": 40,
                "itemWidth": 20,
                "textStyle": {
                    "fontSize": 11
                }
            },
            "xAxis": [
                {
                    "data": [],
                    "show": True,
                    "nameLocation": "middle",
                    "nameTextStyle": {
                        "color": "#696969"
                    },
                    "axisTick": {
                        "show": False,
                        "alignWithLabel": True
                    },
                    "axisLine": {
                        "show": True,
                        "lineStyle": {
                            "color": "#A3A3A3"
                        }
                    },
                    "splitArea": {
                        "show": False
                    },
                    "axisLabel": {
                        "color": "#808080",
                        "interval": "auto",
                        "rotate": 30
                    },
                    "splitLine": {
                        "show": False
                    },
                    "boundaryGap": True,
                    "nameGap": 30
                }
            ],
            "yAxis": [
                {
                    "show": True,
                    "nameGap": 55,
                    "nameLocation": "middle",
                    "nameTextStyle": {
                        "color": "#808080"
                    },
                    "axisTick": {
                        "show": False,
                        "alignWithLabel": False
                    },
                    "splitArea": {
                        "show": False
                    },
                    "axisLine": {
                        "show": True,
                        "lineStyle": {
                            "color": "#A3A3A3"
                        }
                    },
                    "axisLabel": {
                        "color": "#999999",
                        "interval": "auto"
                    },
                    "splitLine": {
                        "show": False
                    }
                }
            ],
            "title": {
                "show": True,
                "left": "center",
                "top": "top",
                "textStyle": {
                    "fontSize": 14,
                    "fontWeight": "bold",
                    "lineHeight": 15
                }
            },
            "tooltip": {
                "show": True,
                "confine": True,
                "trigger": "item",
                "axisPointer": {
                    "type": "shadow"
                },
                "backgroundColor": "#fff",
                "shadowBlur": 10,
                "shadowColor": "rgba(0, 0, 0, .2)",
                "textStyle": {
                    "color": "#000",
                    "fontSize": 15
                },
                "extraCssText": "white-space: normal;box-shadow: 1px 1px 5px #000;"
            },
            "color": [
                "#4E79A7",
                "#F28E2B",
                "#E15759",
                "#86BCB6",
                "#59A14F",
                "#9D7660",
                "#FFBE7D",
                "#EDC948",
                "#FABFD2",
                "#D37295"
            ],
            "textStyle": {
                "fontFamily": "Varela Round"
            }
        }


class MovieNumberChart(BaseChart):
    def __init__(self, **kwargs):
        self.data_frame = None
        super(MovieNumberChart, self).__init__(**kwargs)

    def get_series_data(self):
        series_data = []
        self.data_frame = get_movie_release_each_year_data(self.filters)
        for index, row in self.data_frame.iterrows():
            series_data.append({
                'name': str(row['release_year']),
                'value': float(row['num_unique_titles']) if row['num_unique_titles'] is not None else 0.0
            })
        series = [{
            'name': 'Number Of Movies',
            "emphasis": {
                "focus": "series"
            },
            "yAxisIndex": 0,
            "smooth": True,
            "itemStyle": {},
            "type": "line",
            "data": series_data
        }]

        self.chart['series'] = series

    def set_axes(self):
        self.chart['xAxis'][0]['data'] = list(self.data_frame['release_year'].astype(str).unique())
        self.chart['xAxis'][0]['name'] = 'Release Year'
        self.chart['yAxis'][0]['name'] = "No. Of  Movies"

    def generate(self):
        self.get_series_data()
        self.set_axes()
        return self.chart


class AvgRatingPerGenre(BaseChart):
    def __init__(self, **kwargs):
        self.data_frame = None
        super(AvgRatingPerGenre, self).__init__(**kwargs)

    def get_series_data(self):
        series = list()
        self.data_frame = get_avg_rating_data(self.filters)
        legend_data = list(self.data_frame['Genre'].astype(str).unique())
        group = self.data_frame.groupby('Genre')
        dimension_data = list(self.data_frame["Release Year"].astype(str).unique())
        for _data in legend_data:
            if _data and _data != 'None':
                _group = group.get_group(_data)
                _series = dict()
                _series["name"] = _data
                _series["name"] = _data
                _series["type"] = 'line'
                _series["yAxisIndex"] = 0
                _series["smooth"] = True
                _series["emphasis"] = {
                    "focus": "series"
                }
                series_data = list()
                data_mapping = {}
                for name, value in zip(
                        _group["Release Year"].astype(str),
                        _group["Avg Rating"]
                ):
                    data_mapping[name] = value
                for dimension in dimension_data:
                    value = None
                    if dimension in data_mapping:
                        value = data_mapping[dimension]
                    series_data.append({'name': dimension, 'value': value, 'name1': _data})
                _series["data"] = series_data
                series.append(_series)

        self.chart['series'] = series

    def set_axes(self):
        self.chart['xAxis'][0]['data'] = list(self.data_frame['Release Year'].astype(str).unique())
        self.chart['xAxis'][0]['name'] = 'Release Year'
        self.chart['yAxis'][0]['name'] = "Avg Rating"

    def generate(self):
        self.get_series_data()
        self.set_axes()
        return self.chart
