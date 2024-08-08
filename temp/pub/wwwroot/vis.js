export function testd3(id) {

    let container = document.getElementById(id);

    // Declare the chart dimensions and margins.
    const width = 640;
    const height = 400;
    const marginTop = 20;
    const marginRight = 20;
    const marginBottom = 30;
    const marginLeft = 40;

    // Declare the x (horizontal position) scale.
    const x = d3.scaleUtc()
        .domain([new Date("2023-01-01"), new Date("2024-01-01")])
        .range([marginLeft, width - marginRight]);

    // Declare the y (vertical position) scale.
    const y = d3.scaleLinear()
        .domain([0, 100])
        .range([height - marginBottom, marginTop]);

    // Create the SVG container.
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height);

    // Add the x-axis.
    svg.append("g")
        .attr("transform", `translate(0,${height - marginBottom})`)
        .call(d3.axisBottom(x));

    // Add the y-axis.
    svg.append("g")
        .attr("transform", `translate(${marginLeft},0)`)
        .call(d3.axisLeft(y));

    // Append the SVG element.
    container.append(svg.node());
}

export function sankeyD3(containerId, width, height, nodesJson, linksJson) {

    const container = document.getElementById(containerId);

    console.log(width);
    console.log(height);

    // Specify the dimensions of the chart.
    const format = d3.format(",.0f");

    // Create a SVG container.
    const svg = d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");
    // Constructs and configures a Sankey generator.
    const sankey = d3.sankey()
        .nodeId(d => d.name)
        .nodeAlign(d3.sankeyLeft) // d3.sankeyLeft, etc.
        .nodeWidth(15)
        .nodePadding(10)
        .extent([[1, 5], [width - 1, height - 5]]);


    const { nodes, links } = sankey({
        nodes: JSON.parse(nodesJson),
        links: JSON.parse(linksJson)
    });

    // Defines a color scale.
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    // Creates the rects that represent the nodes.
    const rect = svg.append("g")
        .attr("stroke", "#000")
        .selectAll()
        .data(nodes)
        .join("rect")
        .attr("x", d => d.x0)
        .attr("y", d => d.y0)
        .attr("height", d => d.y1 - d.y0)
        .attr("width", d => d.x1 - d.x0)
        .attr("fill", d => color(d.category));


    // Adds a title on the nodes.
    rect.append("title")
        .text(d => `${d.name}\n${format(d.value)}`);

    // Creates the paths that represent the links.
    const link = svg.append("g")
        .attr("fill", "none")
        .attr("stroke-opacity", 0.5)
        .selectAll()
        .data(links)
        .join("g")
        .style("mix-blend-mode", "multiply");

    link.append("path")
        .attr("d", d3.sankeyLinkHorizontal())
        .attr("stroke", "grey")
        .attr("stroke-width", d => Math.max(1, d.width));

    link.append("title")
        .text(d => `${d.source.name} → ${d.target.name}\n${format(d.value)}`);


    svg.append("g")
        .selectAll()
        .data(nodes)
        .join("text")
        .attr("x", d => d.x0 < width / 2 ? d.x1 + 6 : d.x0 - 6)
        .attr("y", d => (d.y1 + d.y0) / 2)
        .attr("dy", "0.35em")
        .attr("text-anchor", d => d.x0 < width / 2 ? "start" : "end")
        .text(d => d.name);


    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
    container.append(svg.node());
}

function getVirtualData(year) {
    const date = +echarts.time.parse(year + '-01-01');
    const end = +echarts.time.parse(+year + 1 + '-01-01');
    const dayTime = 3600 * 24 * 1000;
    const data = [];
    for (let time = date; time < end; time += dayTime) {
        data.push([
            echarts.time.format(time, '{yyyy}-{MM}-{dd}', false),
            Math.floor(Math.random() * 10000)
        ]);
    }
    return data;
}

export function testEchart(containerId) {
    const container = document.getElementById(containerId);
    const chart = echarts.init(container);

    const option = {
        title: {
            top: 30,
            left: 'center',
            text: 'Daily Step Count'
        },
        tooltip: {},
        visualMap: {
            min: 0,
            max: 10000,
            type: 'piecewise',
            orient: 'horizontal',
            left: 'center',
            top: 65
        },
        calendar: {
            top: 120,
            left: 30,
            right: 30,
            cellSize: ['auto', 13],
            range: '2016',
            itemStyle: {
                borderWidth: 0.5
            },
            yearLabel: { show: false }
        },
        series: {
            type: 'heatmap',
            coordinateSystem: 'calendar',
            data: getVirtualData('2016')
        }
    };

    console.log(option);

    chart.setOption(option);
}

// renders Apache ECharts to a div container. The div should have an id and width/height set.
export function renderEchart(containerId, option) {
    console.log(option);
    console.log(JSON.parse(option));
    const container = document.getElementById(containerId);
    const chart = echarts.init(container);
    chart.setOption(JSON.parse(option));
}