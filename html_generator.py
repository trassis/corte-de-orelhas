import ear_clipping
import tpolygon

def _ear_clipping_html(obj):
    # Sem background por enquanto
    """
    frame.clear_frames()

    zero_list = [ 0 ]* self.polygon_list[0].get_size()
    background_frame = frame.Triangle_Frame(self.get_result(), zero_list, self.frame_options, 0.2)
    """

    for i, frame in enumerate(obj.frame_list):
        with open(f"./frames/frame{i}.svg", "w") as file:
            # file.write(frame.generate_svg(background_frame))
            file.write(frame.generate_svg(None))

    return _get(len(obj.frame_list), obj.frame_options.width, obj.frame_options.height)

def _tpolygon_html(obj):
    pass

def generate_html(to_be_printed):
    if isinstance(to_be_printed, ear_clipping.Ear_clipping):
        return _ear_clipping_html(to_be_printed);
    if isinstance(to_be_printed, tpolygon.TPolygon):
        return _ear_clipping_html(to_be_printed);
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
            fill: #2a2a2a; /* Point color */
            stroke: none; /* No border */
        }

        .blue_point {
            fill: #4b46f0
            stroke: none; /* No border */
        }

        .red_point {
            fill: #d04141; /* Point color */
            stroke: none; /* No border */
        }

        .green_point {
            fill : rgb(59, 142, 59);
            stroke: none
        }

        .line_style {
            stroke-width: 2;
            stroke: red;
        }

        .edge_style {
            stroke-width: 2;
            stroke: black;
        }

        .vertex_color0 {
            fill: #242e24;
            stroke-width: 2;
            stroke: black; 
        }
        .vertex_color1 {
            fill: #d5d4ff;
            stroke-width: 2;
            stroke: black; 
        }
        .vertex_color2 {
            fill: #68cc68;
            stroke-width: 2;
            stroke: black; 
        }
        .vertex_color3 {
            fill: #4b46f0;
            stroke-width: 2;
            stroke: black; 
        }

    </style>
    <script>
        var numberFrames = """ + str(number_of_frames) + """;
        var currentIndex = 0;
        var intervalId;
        var speed = 200;

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
            currentIndex = (currentIndex + 1) % numberFrames; // Move to the next polygon circularly
            displayPolygon(); // Display the new polygon
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
    <input type="range" id="speedRange" min="5" max="1005" value="200" step="50" oninput="changeSpeed(this.value)">
    <span id="speedValue">200</span> ms
    <br>

    <script>
        // Initial display of the first polygon
        displayPolygon();
    </script>
</body>
</html>
"""
