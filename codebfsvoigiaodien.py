import tkinter as tk
from tkinter import messagebox, scrolledtext
from collections import deque
import matplotlib.pyplot as plt
import time


# ====== THUẬT TOÁN GIẢI BÀI TOÁN ====== #
def is_goal_state(state):
    return target_amount in state

def get_neighbors(state, cap1, cap2):
    neighbors = []
    jug1, jug2 = state

    if jug1 < cap1:
        neighbors.append((cap1, jug2))
    if jug2 < cap2:
        neighbors.append((jug1, cap2))
    if jug1 > 0 and jug2 < cap2:
        transfer = min(jug1, cap2 - jug2)
        neighbors.append((jug1 - transfer, jug2 + transfer))
    if jug2 > 0 and jug1 < cap1:
        transfer = min(jug2, cap1 - jug1)
        neighbors.append((jug1 + transfer, jug2 - transfer))
    if jug1 > 0:
        neighbors.append((0, jug2))
    if jug2 > 0:
        neighbors.append((jug1, 0))

    return neighbors

def bfs(cap1, cap2):
    initial_state = (0, 0)
    queue = deque([(initial_state, [])])
    visited = set()

    while queue:
        current_state, path = queue.popleft()
        if is_goal_state(current_state):
            return path + [current_state]
        if current_state not in visited:
            visited.add(current_state)
            for neighbor in get_neighbors(current_state, cap1, cap2):
                if neighbor not in visited:
                    queue.append((neighbor, path + [current_state]))
    return None



# ====== GIAO DIỆN TKINTER ====== #
def solve_problem():
    global target_amount
    try:
        cap1 = int(entry1.get())
        cap2 = int(entry2.get())
        target_amount = int(entry3.get())

        start = time.time()
        solution = bfs(cap1, cap2)
        end = time.time()

        output_box.delete("1.0", tk.END)
        if solution:
            output_box.insert(tk.END, f"Số bước: {len(solution) - 1}\n\n")
            for step in solution:
                output_box.insert(tk.END, f"Bình 1: {step[0]} lít, Bình 2: {step[1]} lít\n")
        else:
            output_box.insert(tk.END, "Không tìm thấy giải pháp!")

        output_box.insert(tk.END, f"\nThời gian thực thi: {end - start:.4f} giây")

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ!")


def plot_multiple_targets():
    try:
        cap1 = int(entry1.get())
        cap2 = int(entry2.get())

        targets = []
        steps = []
        times = []

        for t in range(1, 11):
            global target_amount
            target_amount = t
            start = time.time()
            solution = bfs(cap1, cap2)
            end = time.time()

            targets.append(t)
            steps.append(len(solution) - 1 if solution else 0)
            times.append(end - start)

        plt.figure(figsize=(12, 5))
        plt.subplot(1, 2, 1)
        plt.plot(targets, steps, marker='o')
        plt.title("Số bước BFS theo target")
        plt.xlabel("Target (lít)")
        plt.ylabel("Số bước")

        plt.subplot(1, 2, 2)
        plt.plot(targets, times, marker='o', color='red')
        plt.title("Thời gian thực thi theo target")
        plt.xlabel("Target (lít)")
        plt.ylabel("Thời gian (giây)")

        plt.tight_layout()
        plt.show()

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ!")


# ====== TẠO CỬA SỔ ====== #
root = tk.Tk()
root.title("Đong Nước - BFS")
root.geometry("600x500")

tk.Label(root, text="Dung tích bình 1:").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Dung tích bình 2:").pack()
entry2 = tk.Entry(root)
entry2.pack()

tk.Label(root, text="Số lít cần đong:").pack()
entry3 = tk.Entry(root)
entry3.pack()

tk.Button(root, text="Tìm giải pháp", command=solve_problem, bg="lightblue").pack(pady=5)
tk.Button(root, text="Biểu đồ hiệu suất", command=plot_multiple_targets, bg="lightgreen").pack(pady=5)

output_box = scrolledtext.ScrolledText(root, width=70, height=20)
output_box.pack()

root.mainloop()
