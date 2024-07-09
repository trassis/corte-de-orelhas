from frame import Frame, Ear_Frame

const_html1 = """
<!DOCTYPE html>
<html>
<head>
    <title>Triangulação de polígonos</title>
    <style>
        /* CSS styles for the SVG container */
        #svgelem {
            border: 1px solid #ccc;
        }

        /* Additional CSS styles */
        .polygon {
            fill: #ada6db; /* Fill color */
            stroke: #2a2a2a; /* Stroke color */
            stroke-width: 2; /* Stroke width */
            stroke-opacity: 1; /* Stroke opacity */
            fill-opacity: 1; /* Fill opacity */
            stroke-linecap: round; /* Stroke linecap */
            stroke-linejoin: round; /* Stroke linejoin */
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
            fill: #658db6; /* Point color */
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
            stroke-widht: 2;
            stroke: red;
        }

    </style>
    <script>
        var svgContent = [
"""

const_html2 = """ 
        ];

        var currentIndex = 0;
        var intervalId;

        function displayPolygon(){
            var svg = document.getElementById('svgelem');
            svg.innerHTML = svgContent[currentIndex];
        }

        function nextPolygon() {
            currentIndex = (currentIndex + 1) % svgContent.length; // Move to the next polygon circularly
            displayPolygon(); // Display the new polygon
        }

        function previousPolygon() {
            currentIndex = (currentIndex - 1 + svgContent.length) % svgContent.length; // Move to the previous polygon circularly
            displayPolygon(); // Display the new polygon
        }

        function startAutoPlay() {
            if (!intervalId) { // Check if autoplay is not already running
                intervalId = setInterval(nextPolygon, 200); // Change frame every 1 second
            }
        }

        function stopAutoPlay() {
            if (intervalId) {
                clearInterval(intervalId); // Stop changing frames
                intervalId = null; // Reset intervalId
            }
        }
    </script>
</head>
<body>
    <h2>Triangulação de polígonos</h2>
    <svg id="svgelem" width="300" height="300" xmlns="http://www.w3.org/2000/svg">
    </svg>
    <br>
    <button onclick="previousPolygon()">Previous Polygon</button>
    <button onclick="nextPolygon()">Next Polygon</button>
    <button onclick="startAutoPlay()">Start AutoPlay</button>
    <button onclick="stopAutoPlay()">Stop AutoPlay</button>
    <br>
    <p>Current Polygon: <span id="currentPolygon"></span></p>

    <script>
        // Initial display of the first polygon
        displayPolygon();
    </script>
</body>
</html>
"""

# Retorna índice da primeira verdade em um lista de Bool
def search_true(x):
    for i in range(len(x)):
        if x[i] == True:
            return i
    raise ValueError("Nothing found on list")

class Ear_clipping:
    def __init__(self, initial_polygon):
        self.polygon_list = [initial_polygon]
        self.frame_list = []

    def triangulation(self):
        current_polygon = self.polygon_list[0]
        ear_list = [False] * current_polygon.get_size()

        # Para cada verificação, adiciona 2 frames
        for i in range(current_polygon.get_size()):
            verify_frame = Ear_Frame(current_polygon, ear_list, i)
            self.frame_list.append(verify_frame)

            response_frame = Ear_Frame(current_polygon, ear_list, i)

            if current_polygon.is_ear(i):
                ear_list[i] = True
                response_frame.set_vertex_type(i, "green")
            else:
                response_frame.set_vertex_type(i, "black")

            self.frame_list.append(response_frame)


        while current_polygon.get_size() > 3:
            to_be_removed = search_true(ear_list)

            # Marca que vértice será removido
            removed_frame = Frame(current_polygon, ear_list)
            removed_frame.set_vertex_type(to_be_removed, "red")
            self.frame_list.append(removed_frame)

            ear_list.pop(to_be_removed)
            new_polygon = current_polygon.removed_vertex(to_be_removed)

            # Vértice foi removido
            new_polygon_frame = Frame(new_polygon, ear_list)
            self.frame_list.append(new_polygon_frame)

            previous_index = to_be_removed-1 if to_be_removed > 0 else new_polygon.get_size()-1
            next_index = to_be_removed if to_be_removed < new_polygon.get_size()-1 else 0
            list_index = [ previous_index, next_index ]

            for idx in list_index:
                verify_frame = Ear_Frame(new_polygon, ear_list, idx)
                self.frame_list.append(verify_frame)

                ear_list[idx] = new_polygon.is_ear(idx)

                response_frame = Ear_Frame(new_polygon, ear_list, idx)
                if ear_list[idx]:
                    response_frame.set_vertex_type(idx, "red")
                else:
                    response_frame.set_vertex_type(idx, "black")
                self.frame_list.append(response_frame)


            current_polygon = new_polygon
            self.polygon_list.append(current_polygon)
    
    def get_polygons(self):
        return self.polygon_list

    def generate_html(self):
        html_string = const_html1

        for frame in self.frame_list:
            lines = frame.generate_svg()
            for i, line in enumerate(lines):
                html_string += '\t\t\t'
                if i == 0:
                    html_string += '`'
                html_string += line
                if i < len(lines)-1:
                    html_string += ' /\n';
            html_string += '`,\n'

        html_string += const_html2

        return html_string
