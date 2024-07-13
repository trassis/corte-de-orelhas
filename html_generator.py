import ear_clipping
import coloring
import os
from frameOptions import FrameOptions

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path) 

def clear_frames():
    pasta = './frames'
    for arquivo in os.listdir(pasta):
        caminho_arquivo = os.path.join(pasta, arquivo)
        try:
            if os.path.isfile(caminho_arquivo):
                os.unlink(caminho_arquivo)

        except Exception as e:
            raise MemoryError(f"Erro ao deletar {caminho_arquivo}: {e}")

# HTML para a animação
def _generate_html(obj, idx):
    create_folder_if_not_exists(f'./animation{idx}')
    for i, frame in enumerate(obj.frame_list):
        with open(f"./animation{idx}/frame{i}.svg", "w") as file:
            file.write(frame.generate_svg())

    return _get(len(obj.frame_list), idx)

def generate_html(to_be_printed):
    if isinstance(to_be_printed, ear_clipping.Ear_clipping):
        return _generate_html(to_be_printed, 0);

    if isinstance(to_be_printed, coloring.Coloring):
        return _generate_html(to_be_printed, 1)

    else:
        raise ValueError("Not implemented yet")

def _get(num_frames, index):
    return f"""
<div>
    <h2>Triangulação de polígonos - Animation {index}</h2>
    <svg id="svgelem{index}" width="{FrameOptions.width}" height="{FrameOptions.height}" xmlns="http://www.w3.org/2000/svg"></svg>
    <br>
    <button onclick="previousPolygon{index}()">Previous Polygon</button>
    <button onclick="nextPolygon{index}()">Next Polygon</button>
    <button onclick="reset{index}()">Reset</button>
    <button onclick="end{index}()">End</button>
    <button onclick="startAutoPlay{index}()">Start AutoPlay</button>
    <button onclick="stopAutoPlay{index}()">Stop AutoPlay</button>
    <br>
    <label for="speedRange{index}">Autoplay Frequency (ms): </label>
    <input type="range" id="speedRange{index}" min="50" max="1010" value="100" step="50" oninput="changeSpeed{index}(this.value)">
    <span id="speedValue{index}">100</span> ms
</div>
<style>
    #svgelem {{
        border: 1px solid #ccc;
        background: white;
    }}

    .polygon {{
        fill: #ada6db;
        stroke: #2a2a2a;
        stroke-width: 2;
        stroke-opacity: 1;
        fill-opacity: 1;
        stroke-linecap: round;
        stroke-linejoin: round;
    }}

    .red_triangle {{
        fill: #f03e65;
        fill-opacity: 1;
    }}

    .permanent {{
        fill: rgb(178, 178, 198);
        stroke: #908f8f;
        stroke-width: 2;
        stroke-opacity: 0.7;
        fill-opacity: 0.4;
        stroke-linecap: round;
        stroke-linejoin: round;
    }}

    .point {{
        fill: #2a2a2a;
        stroke: none;
    }}

    .pointer {{
        fill: #727374;
        stroke: none;
    }}

    .black_point {{
        fill: black;
        stroke: none;
        r: 5;
    }}

    .blue_point {{
        fill: blue;
        stroke: none;
        r: 5;
    }}

    .red_point {{
        fill: red;
        stroke: none;
        r: 5;
    }}

    .green_point {{
        fill: green;
        stroke: none;
        r: 5;
    }}

    .line_style {{
        stroke-width: 2;
        stroke: red;
    }}

    .edge_style {{
        stroke-width: 2;
        stroke: black;
    }}
</style>
<script>
    var numberFrames{index} = {num_frames};
    var currentIndex{index} = 0;
    var intervalId{index};
    var speed{index} = 100;

    function fetchSVGContent{index}(file, callback) {{
        fetch(file)
            .then(response => response.text())
            .then(data => callback(data))
            .catch(error => console.error('Error fetching SVG:', error));
    }}

    function displayPolygon{index}() {{
        var filename = `./animation{index}/frame${{currentIndex{index}}}.svg`;
        fetchSVGContent{index}(filename, function(svgContent) {{
            var svg = document.getElementById('svgelem{index}');
            svg.innerHTML = svgContent;
            console.log(svg.innerHTML);
        }});
    }}

    function nextPolygon{index}() {{
        if(intervalId{index} && currentIndex{index} == numberFrames{index}-1) {{
            stopAutoPlay{index}();
        }}
        else{{
            currentIndex{index} = (currentIndex{index} + 1) % numberFrames{index};
            displayPolygon{index}();
        }}
    }}

    function previousPolygon{index}() {{
        currentIndex{index} = (currentIndex{index} - 1 + numberFrames{index}) % numberFrames{index};
        displayPolygon{index}();
    }}

    function startAutoPlay{index}() {{
        if (!intervalId{index}) {{
            intervalId{index} = setInterval(nextPolygon{index}, speed{index});
        }}
    }}

    function stopAutoPlay{index}() {{
        if (intervalId{index}) {{
            clearInterval(intervalId{index});
            intervalId{index} = null;
        }}
    }}

    function end{index}() {{
        stopAutoPlay{index}();
        currentIndex{index} = numberFrames{index} - 1;
        displayPolygon{index}();
    }}

    function reset{index}() {{
        stopAutoPlay{index}();
        currentIndex{index} = 0;
        displayPolygon{index}();
    }}

    function changeSpeed{index}(newSpeed) {{
        if (intervalId{index}) {{
            stopAutoPlay{index}();
            speed{index} = newSpeed;
            startAutoPlay{index}();
        }}
        else{{
            speed{index} = newSpeed;
        }}
        var speedCounter{index} = document.getElementById("speedValue{index}");
        speedCounter{index}.innerText = speed{index};
    }}

    displayPolygon{index}();
</script>
"""
