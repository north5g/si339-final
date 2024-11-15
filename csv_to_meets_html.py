import csv
import os

def csv_to_html(csv_filename, output_folder):
    # Derive the HTML filename by replacing the CSV extension with '.html' in the meets folder
    html_filename = os.path.join(output_folder, os.path.splitext(os.path.basename(csv_filename))[0] + '.html')

    # try:
    with open(csv_filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

        # Ensure there are at least 5 rows for valid HTML generation
        if len(rows) < 5:
            print("CSV file must have at least 5 rows.")
            return

        # Extract values from the first five rows
        link_text = rows[0][0]
        h2_text = rows[1][0]
        link_url = rows[2][0]
        summary_text = rows[3][0]

        # Initialize HTML content
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{link_text}</title>
<link rel="stylesheet" href="../css/style.css">
</head>
   <body>
   <nav class="main-nav">
     <ul>
        <li><a href="../index.html">Home Page</a></li>
        <li><a href="#summary">Summary</a></li>
        <li><a href="#team-results">Team Results</a></li>
        <li><a href="#individual-results">Individual Results</a></li>
        <li><a href="#gallery">Gallery</a></li>
     </ul>
   </nav>
   <header class="meet-info">
      <!--Meet Info-->
       
        <h1><a href="{link_url}">{link_text}</a></h1>
        <h2>{h2_text}</h2>
</header>
   <main class="main" id = "main">


    <section class="summary" id = "summary">
      <h2>Race Summary</h2>
      {summary_text}
    </section>
"""


        # Start container for individual results
        html_content += """<section id="team-results">\n
        <h2>Team Results</h2>"""

        # Process the remaining rows (after the first five)
        html_content += """<table>\n"""
        table_start = True

        for row in rows[4:]:
            # For rows that are 3 columns wide, add to the team places list
            if len(row) == 3:
                if row[0] == "Place":
                    html_content += f"<tr><th>{row[0]}</th><th>{row[1]}</th><th>{row[2]}</th></tr>\n"

                else:
                    html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td> {row[2]}</td></tr>\n"

            # For rows that are 8 columns wide and contain 'Ann Arbor Skyline' in column 6
            elif len(row) == 8 and row[5].strip().lower() == 'ann arbor skyline':
                if table_start == True:
                    table_start = False
                    html_content += "</table>\n"
                    html_content += """</section>\n
                    <section id="individual-results">\n
                    <h2>Individual Results</h2>\n
                    <div class="athlete-container">"""

                place = row[0]
                grade = row[1]
                name = row[2]
                time = row[4]
                profile_pic = row[7]
                if os.path.isfile(f'images/profiles/{profile_pic}'):
                    image = f'''<img src="../images/profiles/{profile_pic}" width="200" alt="{name}">'''
                else:
                    image = f'''<img src="../images/profiles/default_image.jpg" width="200" alt="Runner not found">'''

                # Add the athlete div
                html_content += f"""
<div class="athlete-segment">
<figure> 
    {image} 
</figure>
<div class="athlete-info">
    <h3>{name}</h3>
    <dl>
        <dt>Place</dt><dd>{place[:-1]}</dd>
        <dt>Time</dt><dd>{time}</dd>
        <dt>Grade</dt><dd>{grade}</dd>
    </dl>
    </div>
</div>
"""

        html_content += """</div>\n</section>\n
        <section id = "gallery">
        <h2>Gallery</h2>
        <div class="carousel">
        <input type="radio" name="carousel" id="slide1" checked>
        <input type="radio" name="carousel" id="slide2">
        <input type="radio" name="carousel" id="slide3">
        <input type="radio" name="carousel" id="slide4">
        <input type="radio" name="carousel" id="slide5">
        <div class="carousel-navigation">
            <label for="slide1">Slide 1</label>
            <label for="slide2">Slide 2</label>
            <label for="slide3">Slide 3</label>
            <label for="slide4">Slide 4</label>
            <label for="slide5">Slide 5</label>
        </div>
        <div class="carousel-slides">
        """

        html_content += create_meet_image_gallery(url)
        # Close the HTML document
        html_content += """
   </section>
   </main>   
   <script>
    document.addEventListener("DOMContentLoaded", function () {
        const slides = document.querySelectorAll(".carousel input[type='radio']");
        const carouselSlides = document.querySelector(".carousel-slides");
        let interval;
        let currentIndex = 0;
        const intervalTime = 5000; // Change slide every 5 seconds

        // Check if 'prefers-reduced-motion' is enabled
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        function getTotalSlides() {
            return window.innerWidth >= 1024 ? 3 : 5;
        }

        function updateSlidePosition() {
            const totalSlides = getTotalSlides();
            carouselSlides.style.transform = `translateX(-${(currentIndex * 100) / totalSlides}%)`;
        }

        function showNextSlide() {
            slides[currentIndex].checked = false; // Uncheck current radio button
            currentIndex = (currentIndex + 1) % getTotalSlides(); // Move to next slide
            slides[currentIndex].checked = true; // Check the new radio button
            updateSlidePosition();
        }

        function startInterval() {
            // Only start the interval if reduced motion is not preferred
            if (!prefersReducedMotion) {
                interval = setInterval(showNextSlide, intervalTime);
            }
        }

        function resetInterval() {
            clearInterval(interval);
            startInterval();
        }

        // Initialize the interval for the first time
        startInterval();

        // Update currentIndex and reset interval when a radio button is clicked
        slides.forEach((slide, index) => {
            slide.addEventListener("click", function () {
                currentIndex = index;
                updateSlidePosition();
                resetInterval();
            });
        });

        // Adjust slide layout when resizing the window
        window.addEventListener("resize", function () {
            updateSlidePosition();
        });
    });
</script>
        </body>
</html>
"""
        import re
        html_content = re.sub(r'<time>', '<span class="time">', html_content)
        html_content = re.sub(r'</time>', '</span>', html_content)

        # Save HTML content to a file in the meets folder
        with open(html_filename, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(html_content)

        print(f"HTML file '{html_filename}' created successfully.")
        return(link_text, f"meets/{link_text.replace(' ','_')}_24.html")

    # except Exception as e:
    #     print(f"Error processing file: {e}")

def process_meet_files():
    # Set the meets folder path
    meets_folder = os.path.join(os.getcwd(), "meets")
    
    # Search for all CSV files in the meets folder
    csv_files = [f for f in os.listdir(meets_folder) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in folder: {meets_folder}")
        return

    meets = []
    # Process each CSV file in the meets folder
    for csv_file in csv_files:
        csv_file_path = os.path.join(meets_folder, csv_file)
        meets.append(csv_to_html(csv_file_path, meets_folder))
    html_content = '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Meets Index</title>
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
        <header class="meet-info">
            <h1>Upcoming Meets</h1>
            <p>Select a meet to view more details</p>
        </header>
        <main>
            <section class="meets-list">
            <!-- Dynamically generated list of meets -->
            <ul>
            '''
    for name, link in meets:
        html_content += f'''<li><a href="{link}">{name}</a></li>\n'''
    html_content += '''</ul>
                </section>
            </main>
        </body>
    </html>'''
    with open("index.html", 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(html_content)
    print(f"HTML file 'index.html' created successfully.")



import re
import os
import random

# Step 1: Extract the meet ID from the URL
def extract_meet_id(url):
    # Regex to extract the meet ID, which is the number right after '/meet/'
    match = re.search(r"/meet/(\d+)", url)
    print(f"The meet id is {match}")
    if match:
        print(f"REturning {match.group(1)}")
        return match.group(1)
    else:
        raise ValueError("Meet ID not found in URL.")

# Step 2: Select 12 random photos from the folder
def select_random_photos(folder_path, num_photos=15):
    # List all files in the folder
    print(f"Checking {folder_path}")
    all_files = os.listdir(folder_path)
    # Filter out non-image files if necessary (assuming .jpg, .png, etc.)
    image_files = [f for f in all_files if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    # Ensure we have enough images to select
    if len(image_files) < num_photos:
        return ""
        raise ValueError(f"Not enough images in the folder. Found {len(image_files)} images.")
    
    # Select 12 random images
    return random.sample(image_files, num_photos)

# Step 3: Generate HTML image tags
def generate_image_tags(image_files, folder_path):
    carousel = ''''''
    for i, img in enumerate(image_files):
        if i % 3 == 0:
            carousel += '''<div class="carousel-slide">\n'''
        img_path = os.path.join(folder_path, img)
        # print(f"The image_path is {img_path}")
        carousel += f'<img src=../{img_path} width = "200" alt="">\n'
        if i % 3 == 2:
            carousel += '''</div>\n'''
    return carousel

# Putting it all together
def create_meet_image_gallery(url):
    meet_id = extract_meet_id(url)
    # Define the folder path for images based on the meet ID
    folder_path = f'images/meets/{meet_id}/'

    # print(f"The folder path is {folder_path}")
    
    if not os.path.exists(folder_path):
        return ""
        raise FileNotFoundError(f"The folder {folder_path} does not exist.")
    
    # Select 12 random photos
    selected_photos = select_random_photos(folder_path)
    
    # Generate image tags
    html_image_tags = generate_image_tags(selected_photos, folder_path)
    
    return html_image_tags

# Example usage
url = "https://www.athletic.net/CrossCountry/meet/235827/results/943367"
html_gallery = create_meet_image_gallery(url)
print(html_gallery)


if __name__ == "__main__":
    # Check if meets folder exists
    meets_folder = os.path.join(os.getcwd(), "meets")
    if not os.path.exists(meets_folder):
        print(f"Folder '{meets_folder}' does not exist.")
    else:
        process_meet_files()
