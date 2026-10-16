import heapq
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
from matplotlib.animation import FuncAnimation


# -----------------------------
# Node for Huffman Tree
# -----------------------------
class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


# -----------------------------
# Input text
# -----------------------------
text = "MISSISSIPPI"

frequency = Counter(text)

print("Input Text:", text)
print("\nCharacter Frequencies:")

for char, freq in frequency.items():
    print(char, ":", freq)


# -----------------------------
# Create Min Heap
# -----------------------------
heap = []

for char, freq in frequency.items():
    heapq.heappush(heap, Node(char, freq))


# Store each step for animation
steps = []

steps.append(list(heap))


# -----------------------------
# Build Huffman Tree
# -----------------------------
while len(heap) > 1:

    left = heapq.heappop(heap)
    right = heapq.heappop(heap)

    merged = Node(
        None,
        left.freq + right.freq,
        left,
        right
    )

    heapq.heappush(heap, merged)

    steps.append(list(heap))


root = heap[0]


# -----------------------------
# Generate Huffman Codes
# -----------------------------
codes = {}


def generate_codes(node, code=""):

    if node is None:
        return

    if node.char is not None:
        codes[node.char] = code
        return

    generate_codes(node.left, code + "0")
    generate_codes(node.right, code + "1")


generate_codes(root)


print("\nHuffman Codes:")

for char, code in codes.items():
    print(char, ":", code)


# -----------------------------
# Encode Text
# -----------------------------
encoded_text = ""

for char in text:
    encoded_text += codes[char]


print("\nEncoded Text:")
print(encoded_text)


# -----------------------------
# Calculate Compression
# -----------------------------
original_bits = len(text) * 8
compressed_bits = len(encoded_text)

saving = ((original_bits - compressed_bits) / original_bits) * 100

print("\nOriginal Size:", original_bits, "bits")
print("Compressed Size:", compressed_bits, "bits")
print("Space Saved:", round(saving, 2), "%")


# -----------------------------
# Function to draw tree
# -----------------------------
def draw_tree(root, title):

    G = nx.DiGraph()

    positions = {}

    counter = [0]

    def add_nodes(node, depth=0):

        if node is None:
            return

        add_nodes(node.left, depth + 1)

        x = counter[0]
        counter[0] += 1

        positions[id(node)] = (x, -depth)

        if node.char is None:
            label = str(node.freq)
        else:
            label = f"{node.char}\n{node.freq}"

        G.add_node(id(node), label=label)

        if node.left:
            G.add_edge(id(node), id(node.left), label="0")

        if node.right:
            G.add_edge(id(node), id(node.right), label="1")

        add_nodes(node.right, depth + 1)

    add_nodes(root)

    labels = nx.get_node_attributes(G, "label")
    edge_labels = nx.get_edge_attributes(G, "label")

    nx.draw(
        G,
        positions,
        labels=labels,
        with_labels=True,
        node_size=2500,
        font_size=10
    )

    nx.draw_networkx_edge_labels(
        G,
        positions,
        edge_labels=edge_labels
    )

    plt.title(title)


# -----------------------------
# Animation
# -----------------------------
fig = plt.figure(figsize=(10, 6))


def animate(frame):

    plt.clf()

    if frame == 0:

        plt.axis("off")

        plt.title(
            "Huffman Coding Animation",
            fontsize=18
        )

        plt.text(
            0.5,
            0.75,
            "Input Text",
            ha="center",
            fontsize=14
        )

        plt.text(
            0.5,
            0.65,
            text,
            ha="center",
            fontsize=20
        )

        freq_text = "Character Frequencies\n\n"

        for char, freq in frequency.items():
            freq_text += f"{char} : {freq}\n"

        plt.text(
            0.5,
            0.30,
            freq_text,
            ha="center",
            fontsize=13
        )

    elif frame <= len(steps):

        current_nodes = steps[frame - 1]

        plt.axis("off")

        plt.title(
            f"Step {frame}: Huffman Tree Construction",
            fontsize=16
        )

        display = ""

        for node in current_nodes:

            if node.char:
                display += f"{node.char} ({node.freq})     "
            else:
                display += f"Node ({node.freq})     "

        plt.text(
            0.5,
            0.5,
            display,
            ha="center",
            fontsize=14,
            wrap=True
        )

    else:

        plt.clf()

        draw_tree(
            root,
            "Final Huffman Tree"
        )


total_frames = len(steps) + 2

animation = FuncAnimation(
    fig,
    animate,
    frames=total_frames,
    interval=1800,
    repeat=True
)

plt.show()