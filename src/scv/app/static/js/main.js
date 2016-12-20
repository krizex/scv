/**
 * Created by dqian on 12/19/16.
 */

function drawCharts(xVals, series) {
    Highcharts.chart('container', {
        title: {
            text: 'Sales',
            x: -20 //center
        },
        subtitle: {
            text: 'Source: www.njhouse.com.cn',
            x: -20
        },
        xAxis: xVals,
        yAxis: {
            title: {
                text: 'Number'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: series
    });
}

