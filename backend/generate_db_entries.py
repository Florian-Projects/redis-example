import sqlite3
import random
import string
import uuid
from itertools import product
from PIL import Image, ImageDraw
import base64
from io import BytesIO


# Generate a book title
def generate_book_titles(n=20000):
    adjectives = [
        "Lost",
        "Dark",
        "Golden",
        "Eternal",
        "Final",
        "Mysterious",
        "Hidden",
        "Ancient",
        "Red",
        "Silent",
    ]
    nouns = [
        "Secret",
        "Promise",
        "Time",
        "Light",
        "Shadow",
        "Dream",
        "Tree",
        "Moon",
        "Star",
        "Wind",
    ]

    # Create all possible combinations of adjectives and nouns
    combinations = list(product(adjectives, nouns))
    random.shuffle(combinations)  # Shuffle the combinations to get them in random order

    # Return the first n combinations as titles
    return [f"{adj} {noun}" for adj, noun in combinations[:n]]


# Generate an author name
def generate_author_name():
    # Extended list of first names
    first_names = [
        "John",
        "Jane",
        "Alex",
        "Emily",
        "Chris",
        "Kate",
        "Michael",
        "Sarah",
        "David",
        "Laura",
        "Robert",
        "Michelle",
        "Brian",
        "Lisa",
        "Richard",
        "Linda",
        "Daniel",
        "Susan",
        "Paul",
        "Karen",
        "Mark",
        "Nancy",
        "Jason",
        "Deborah",
        "Jeffrey",
        "Jessica",
        "Ryan",
        "Sharon",
        "Eric",
        "Cynthia",
        "Stephen",
        "Angela",
        "Andrew",
        "Rebecca",
        "Joshua",
        "Ruth",
        "Kevin",
        "Melissa",
        "Timothy",
        "Brenda",
        "Joseph",
        "Amy",
        "Larry",
        "Barbara",
        "Frank",
        "Nicole",
        "Scott",
        "Kathy",
        "Brandon",
        "Denise",
        "Samuel",
        "Diane",
        "Benjamin",
        "Pamela",
        "Gregory",
        "Martha",
        "Raymond",
        "Teresa",
        "Dennis",
        "Carol",
        "Jerry",
        "Cheryl",
        "Ronald",
        "Megan",
        "Anthony",
        "Andrea",
        "Joel",
        "Olivia",
        "Jack",
        "Katherine",
        "Henry",
        "Samantha",
        "Graham",
        "Vanessa",
        "Kenneth",
        "Sandra",
        "Roger",
        "Donna",
        "Keith",
        "Paula",
    ]

    # Extended list of last names
    last_names = [
        "Smith",
        "Johnson",
        "Williams",
        "Jones",
        "Brown",
        "Davis",
        "Miller",
        "Wilson",
        "Moore",
        "Taylor",
        "Anderson",
        "Thomas",
        "Jackson",
        "White",
        "Harris",
        "Martin",
        "Thompson",
        "Garcia",
        "Martinez",
        "Robinson",
        "Clark",
        "Rodriguez",
        "Lewis",
        "Lee",
        "Walker",
        "Hall",
        "Allen",
        "Young",
        "Hernandez",
        "King",
        "Wright",
        "Lopez",
        "Hill",
        "Scott",
        "Green",
        "Adams",
        "Baker",
        "Gonzalez",
        "Nelson",
        "Carter",
        "Mitchell",
        "Perez",
        "Roberts",
        "Turner",
        "Phillips",
        "Campbell",
        "Parker",
        "Evans",
        "Edwards",
        "Collins",
        "Stewart",
        "Sanchez",
        "Morris",
        "Rogers",
        "Reed",
        "Cook",
        "Morgan",
        "Bell",
        "Murphy",
        "Bailey",
        "Rivera",
        "Cooper",
        "Richardson",
        "Cox",
        "Howard",
        "Ward",
        "Torres",
        "Peterson",
        "Gray",
        "Ramirez",
        "James",
        "Watson",
        "Brooks",
        "Kelly",
        "Sanders",
        "Price",
        "Bennett",
        "Wood",
        "Barnes",
        "Ross",
        "Henderson",
        "Coleman",
        "Jenkins",
        "Perry",
        "Powell",
        "Long",
        "Patterson",
        "Hughes",
        "Flores",
        "Washington",
    ]
    return random.choice(first_names) + " " + random.choice(last_names)


# Generate a random image and return its base64 encoded string
def generate_cover_picture():
    width, height = 100, 100
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    for _ in range(1000):  # Draw 1000 random points
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.point((x, y), fill=color)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# Generate an ISBN number (a simple random one, not a valid format)
def generate_isbn():
    return "".join(random.choices(string.digits, k=13))


# Insert the generated entries into an SQLite database
def insert_into_database(titles):
    conn = sqlite3.connect("bookdatabase.sqlite")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    # cursor.execute('''
    # CREATE TABLE IF NOT EXISTS books (
    #     id INTEGER PRIMARY KEY,
    #     title TEXT NOT NULL,
    #     author TEXT NOT NULL,
    #     cover_picture TEXT NOT NULL,
    #     isbn TEXT NOT NULL UNIQUE
    # )
    # ''')

    for title in titles:
        author = generate_author_name()
        cover = generate_cover_picture()
        isbn = generate_isbn()
        cursor.execute(
            "INSERT INTO books (title, author, cover_picture, isbn) VALUES (?, ?, ?, ?)",
            (title, author, cover, isbn),
        )

    conn.commit()
    conn.close()


def read_file_line_by_line(filename):
    with open(filename, "r") as file:
        for line in file:
            yield line.strip()


if __name__ == "__main__":
    titles = read_file_line_by_line("uniq_title.txt")
    insert_into_database(titles)
    print(f"Inserted 20,000 unique titles into the database!")
