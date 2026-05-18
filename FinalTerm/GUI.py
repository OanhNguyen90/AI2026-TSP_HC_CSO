import tkinter as tk
from tkinter import ttk, messagebox
import Visualization


class TSPGuiApp:
    def __init__(self, root, cmd_hc, cmd_cso, cmd_compare):
        self.root = root
        self.root.title("The Travelling Salesman Problem_HC_CSO")
        self.root.geometry("1100x700")

        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 11, "bold"), padding=5)

        self.cmd_hc = cmd_hc
        self.cmd_cso = cmd_cso
        self.cmd_compare = cmd_compare

        self.control_frame = ttk.Frame(self.root, width=350, padding=10)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.view_frame = ttk.Frame(self.root, padding=10)
        self.view_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._setup_control_panel()
        self.canvas, self.ax_route, self.ax_conv = Visualization.setup_canvas(self.view_frame)

    def _setup_control_panel(self):
        ttk.Label(self.control_frame, text="THIẾT LẬP THUẬT TOÁN", font=("Arial", 14, "bold")).grid(row=0, column=0,
                                                                                                    columnspan=2,
                                                                                                    pady=(0, 20))

        val_cmd = (self.root.register(self.validate_number), '%P')

        # 1. Ô nhập số thành phố
        ttk.Label(self.control_frame, text="Số lượng thành phố:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_cities = ttk.Entry(self.control_frame, font=("Arial", 12), validate="key", validatecommand=val_cmd)
        self.entry_cities.grid(row=1, column=1, pady=5, sticky=tk.EW)
        self.entry_cities.insert(0, "10")

        # 2. Ô nhập Random Seed
        ttk.Label(self.control_frame, text="Random seed:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_seed = ttk.Entry(self.control_frame, font=("Arial", 12), validate="key", validatecommand=val_cmd)
        self.entry_seed.grid(row=2, column=1, pady=5, sticky=tk.EW)
        self.entry_seed.insert(0, "42")

        # 3. MỚI: Ô nhập Số vòng lặp tối đa
        ttk.Label(self.control_frame, text="Số vòng lặp tối đa:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_iterations = ttk.Entry(self.control_frame, font=("Arial", 12), validate="key",
                                          validatecommand=val_cmd)
        self.entry_iterations.grid(row=3, column=1, pady=5, sticky=tk.EW)
        self.entry_iterations.insert(0, "100")  # Mặc định là 100 vòng lặp

        # Hệ thống nút bấm điều khiển (Đẩy dịch hàng xuống)
        self.btn_run_hc = ttk.Button(self.control_frame, text="CHẠY HC", command=self.cmd_hc)
        self.btn_run_hc.grid(row=4, column=0, columnspan=2, pady=(15, 5), sticky=tk.EW)

        self.btn_run_cso = ttk.Button(self.control_frame, text="CHẠY CSO", command=self.cmd_cso)
        self.btn_run_cso.grid(row=5, column=0, columnspan=2, pady=5, sticky=tk.EW)

        self.btn_compare = ttk.Button(self.control_frame, text="CHẠY SO SÁNH", command=self.cmd_compare)
        self.btn_compare.grid(row=6, column=0, columnspan=2, pady=(5, 15), sticky=tk.EW)

        # --- BOX 1: KẾT QUẢ TỔNG QUAN ---
        ttk.Label(self.control_frame, text="KẾT QUẢ CHÍNH:", font=("Arial", 12, "bold")).grid(row=7, column=0,
                                                                                              columnspan=2, pady=(5, 2),
                                                                                              sticky=tk.W)
        self.txt_main = tk.Text(self.control_frame, font=("Courier", 10), height=11, width=42, wrap=tk.WORD)
        self.txt_main.grid(row=8, column=0, columnspan=2, sticky="nsew")

        # --- BOX 2: LỊCH SỬ HỘI TỤ ---
        ttk.Label(self.control_frame, text="LỊCH SỬ TỪNG VÒNG LẶP:", font=("Arial", 12, "bold")).grid(row=9, column=0,
                                                                                                      columnspan=2,
                                                                                                      pady=(10, 2),
                                                                                                      sticky=tk.W)
        self.txt_history = tk.Text(self.control_frame, font=("Courier", 10), height=11, width=42, wrap=tk.WORD)
        self.txt_history.grid(row=10, column=0, columnspan=2, sticky="nsew")

        self.control_frame.grid_rowconfigure(8, weight=1)
        self.control_frame.grid_rowconfigure(10, weight=1)
        self.control_frame.grid_columnconfigure(0, weight=1)

    def validate_number(self, P):
        return P.isdigit() or P == ""

    def get_inputs(self):
        """Trả về thêm giá trị max_iter nhận từ ô nhập liệu mới"""
        cities_input = self.entry_cities.get().strip()
        if not cities_input.isdigit() or int(cities_input) < 3:
            self.show_error("Vui lòng nhập số nguyên >= 3 cho số thành phố!")
            return None, None, None

        seed_val = self.entry_seed.get().strip()
        seed = int(seed_val) if seed_val.isdigit() else None

        # Đọc dữ liệu vòng lặp
        iter_input = self.entry_iterations.get().strip()
        max_iter = int(iter_input) if (iter_input.isdigit() and int(iter_input) > 0) else 100

        return int(cities_input), seed, max_iter

    def update_result_text(self, main_text, history_text):
        self.txt_main.delete("1.0", tk.END)
        self.txt_main.insert(tk.END, main_text)

        self.txt_history.delete("1.0", tk.END)
        self.txt_history.insert(tk.END, history_text)

    def show_error(self, message):
        messagebox.showerror("Lỗi", message)