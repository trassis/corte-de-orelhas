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
def _generate_html(obj, idx, name):
    create_folder_if_not_exists(f'./animation{idx}')

    # Escreve cada svg
    for i, frame in enumerate(obj.frame_list):
        with open(f"./animation{idx}/frame{i}.svg", "w") as file:
            file.write(frame.generate_svg())

    # Escreve as descrições
    description = ('\n').join([ frame.get_description() for frame in obj.frame_list ])
    with open(f"./animation{idx}/text.txt", "w") as file:
        file.write(description)

    return _get(len(obj.frame_list), idx, name)

def generate_html(to_be_printed):
    if isinstance(to_be_printed, ear_clipping.Ear_clipping):
        return _generate_html(to_be_printed, 0, "Triangulação de polígonos");

    if isinstance(to_be_printed, coloring.Coloring):
        return _generate_html(to_be_printed, 1, "Colorindo uma triangulação")

    else:
        raise ValueError("Not implemented yet")

def _get(num_frames, index, animation_name):
    return f"""
<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<div>
    <div class="mycontainer">
        <div class="svg-column">
            <svg id="svgelem{index}" width="{FrameOptions.width}" height="{FrameOptions.height}" xmlns="http://www.w3.org/2000/svg"></svg>
        </div>

        <div class="controls-column">
            <h2>{animation_name}</h2>
            <br>
            <span id="spanelem{index}">No text yet</span>
            <br>
            <button class="button" onclick="previousPolygon{index}()"><span class="material-icons">fast_rewind</span></button>
            <button class="button" onclick="nextPolygon{index}()"><span class="material-icons">fast_forward</span></button>
            <button class="button" onclick="startAutoPlay{index}()"><span class="material-icons">play_arrow</span></button>
            <button class="button" onclick="stopAutoPlay{index}()"><span class="material-icons">pause</span></button>
            <button class="button" onclick="reset{index}()"><span class="material-icons">skip_previous</span></button>
            <button class="button" onclick="end{index}()"><span class="material-icons">skip_next</span></button>
            <br>
            <label for="speedRange{index}">Frequência do reprodutor: 
                <span id="speedValue{index}">500</span> ms
            </label>
            <input type="range" id="speedRange{index}" min="100" max="1000" value="500" step="100" oninput="changeSpeed{index}(this.value)" style="width: 300px;">
        </div>
    </div>
</div>
<style>
    .mycontainer {{
        display: flex; /* Use flexbox for side-by-side layout */
        align-items: center; /* Center items vertically */
        width: 100%;
        height: 100%;
    }}

    .svg-column {{
    }}

    .controls-column {{
        margin-left: 10px; /* Space between SVG and controls */
        overflow-wrap: break-word;
    }}

    .button {{
        color: black; /* Text color */
        background-color: white; /* Button background */
        border: 1px solid black; /* Button border */
        padding: 5px 5px; /* Button padding */
        margin: 5px; /* Space between buttons */
        cursor: pointer; /* Pointer cursor on hover */
        font-size: 24px; /* Font size */
        border-radius: 5px; /* Rounded corners */
        transition: background-color 0.3s; /* Smooth background transition */
    }}

    .button:hover {{
        background-color: #f0f0f0; /* Light gray on hover */
    }}

    #svgelem{index} {{
        border: 1px solid #ccc;
        background: lightyellow;
    }}

    .polygon {{
        fill: #c594f2;
        stroke: black;
        stroke-width: 2;
        stroke-opacity: 1;
        fill-opacity: 1;
        stroke-linecap: round;
        stroke-linejoin: round;
    }}

    .highlight_polygon {{
        fill: #a335de;
        fill-opacity: 1;
    }}

    .black_point {{
        fill: black;
        stroke: none;
        r: 4;
    }}

    .blue_point {{
        fill: #edec77;
        stroke: black;
        r: 4;
    }}

    .red_point {{
        fill: #eb445d;
        stroke: black;
        r: 4;
    }}

    .green_point {{
        fill: #65f077;
        stroke: black;
        r: 4;
    }}

    .line_style {{
        stroke-width: 2;
        stroke: red;
    }}

    .edge_style {{
        stroke-width: 1;
        stroke: black;
    }}
</style>
<script>
    var numberFrames{index} = {num_frames};
    var currentIndex{index} = 0;
    var intervalId{index};
    var speed{index} = 500;

    function fetchSVGContent{index}(file, callback) {{
        fetch(file)
            .then(response => response.text())
            .then(data => callback(data))
            .catch(error => console.error('Error fetching SVG:', error));
    }}

    function getLineFromFile{index}(fileUrl, lineNumber, callback) {{
    fetch(fileUrl)
        .then(response => {{
            if (!response.ok) {{
                throw new Error(`HTTP error! status: ${{response.status}}`);
            }}
            return response.text();
        }})
        .then(data => {{
            const lines = data.split('\\n');
            if (lineNumber < 0 || lineNumber >= lines.length) {{
                console.error('Line number out of range');
                return;
            }}
            callback(lines[lineNumber]); // Use callback to return the line
        }})
        .catch(error => console.error('Error fetching file:', error));
    }}

    function displayPolygon{index}() {{
        var filename = `./animation{index}/frame${{currentIndex{index}}}.svg`;

        fetchSVGContent{index}(filename, function(svgContent) {{
            var svg = document.getElementById('svgelem{index}');
            svg.innerHTML = svgContent;

        }});

        getLineFromFile{index}('./animation{index}/text.txt', currentIndex{index}, function(line) {{
            var spanElement = document.getElementById('spanelem{index}');
            spanElement.textContent = line; // Update span text
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
