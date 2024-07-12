import ear_clipping
import tpolygon
import os
from frameOptions import FrameOptions

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
def _ear_clipping_html(obj):
    for i, frame in enumerate(obj.frame_list):
        with open(f"./frames/frame{i}.svg", "w") as file:
            file.write(frame.generate_svg())

    return _get(len(obj.frame_list), FrameOptions.width, FrameOptions.height)

# HTML para só um tpolygon
def _tpolygon_html(obj):
        frame = obj.get_frame()

        with open(f"./frames/frame0.svg", "w") as file:
            file.write(frame.generate_svg())

        print('oi')

        # MUDAR AQUI
        return _get(1, 400, 400)

def generate_html(to_be_printed):
    if isinstance(to_be_printed, ear_clipping.Ear_clipping):
        return _ear_clipping_html(to_be_printed);

    if isinstance(to_be_printed, tpolygon.TPolygon):
        return _tpolygon_html(to_be_printed);

    else:
        raise ValueError("Not implemented yet")

def _get(number_of_frames, height, width):
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Triangulação de polígonos</title>
    <style>
        #svgelem {
            border: 1px solid #ccc;
            background: white;
        }

        .polygon {
            fill: #ada6db; /* Fill color */
            stroke: #2a2a2a; /* Stroke color */
        stroke-width: 2; /* Stroke width */
        stroke-opacity: 1; /* Stroke opacity */
        fill-opacity: 1; /* Fill opacity */
        stroke-linecap: round; /* Stroke linecap */
        stroke-linejoin: round; /* Stroke linejoin */
    }

    .red_triangle {
        fill: #f03e65; /* Fill color */
        fill-opacity: 1; /* Fill opacity */
    }

    .permanent{
        fill: rgb(178, 178, 198); /* Fill color */
        stroke: #908f8f; /* Stroke color */
        stroke-width: 2; /* Stroke width */
        stroke-opacity: 0.7; /* Stroke opacity */
        fill-opacity: 0.4; /* Fill opacity */
        stroke-linecap: round; /* Stroke linecap */
        stroke-linejoin: round; /* Stroke linejoin */
    }


    .point {
        fill: #2a2a2a; /* Point color */
        stroke: none; /* No border */
    }

    .pointer {
        fill: #727374; /* Point color */
        stroke: none; /* No border */
    }

    .black_point {
        fill: black;
        stroke: none; 
        r: 5;
    }

    .blue_point {
        fill: blue;
        stroke: none; 
        r: 5;
    }

    .red_point {
        fill: red;
        stroke: none; 
        r: 5;
    }

    .green_point {
        fill : green;
        stroke: none;
        r: 5;
    }

    .line_style {
        stroke-width: 2;
        stroke: red;
    }

    .edge_style {
        stroke-width: 2;
        stroke: black;
    }
</style>
<script>
    var numberFrames = """ + str(number_of_frames) + """;
    var currentIndex = 0;
    var intervalId;
    var speed = 100;

    function fetchSVGContent(file, callback) {
        fetch(file)
            .then(response => response.text())
            .then(data => callback(data))
            .catch(error => console.error('Error fetching SVG:', error));
    }

    function displayPolygon(){
        var filename = `./frames/frame${currentIndex}.svg`;
        fetchSVGContent(filename, function(svgContent) {
            var svg = document.getElementById('svgelem');
            svg.innerHTML = svgContent;
            console.log(svg.innerHTML);
        });
    }

    function nextPolygon() {
        if(intervalId && currentIndex == numberFrames-1){
            stopAutoPlay();
        }
        else{
            currentIndex = (currentIndex + 1) % numberFrames; // Move to the next polygon circularly
            displayPolygon(); // Display the new polygon
        }
    }

    function previousPolygon() {
        currentIndex = (currentIndex - 1 + numberFrames) % numberFrames; // Move to the previous polygon circularly
        displayPolygon(); // Display the new polygon
    }

    function startAutoPlay() {
        if (!intervalId) { // Check if autoplay is not already running
            intervalId = setInterval(nextPolygon, speed); // Change frame every 1 second
        }
    }

    function stopAutoPlay() {
        if (intervalId) {
            clearInterval(intervalId); // Stop changing frames
            intervalId = null; // Reset intervalId
        }
    }

    function end() {
        stopAutoPlay();
        currentIndex = numberFrames - 1;
        displayPolygon();
    }

    function reset() {
        stopAutoPlay();
        currentIndex = 0;
        displayPolygon();
    }

    function changeSpeed(newSpeed) {
        if (intervalId) {
            stopAutoPlay();
            speed = newSpeed;
            startAutoPlay();
        }
        else{
            speed = newSpeed;
        }
        var speedCounter = document.getElementById("speedValue");
        speedCounter.innerText = speed;
    }
</script>
</head>
<body>
<h2>Triangulação de polígonos</h2>
<svg id="svgelem" width=""""" + str(width) + " height=" + str(height) + """ xmlns="http://www.w3.org/2000/svg">
</svg>
<br>
<button onclick="previousPolygon()">Previous Polygon</button>
<button onclick="nextPolygon()">Next Polygon</button>
<button onclick="reset()">Reset</button>
<button onclick="end()">End</button>
<button onclick="startAutoPlay()">Start AutoPlay</button>
<button onclick="stopAutoPlay()">Stop AutoPlay</button>
<br>
<label for="speedRange">Autoplay Frequency (ms): </label>
<input type="range" id="speedRange" min="50" max="1010" value="100" step="50" oninput="changeSpeed(this.value)">
<span id="speedValue">100</span> ms
<br>

<script>
    // Initial display of the first polygon
    displayPolygon();
</script>
</body>
</html>
"""
