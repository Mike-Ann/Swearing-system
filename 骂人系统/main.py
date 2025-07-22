import customtkinter as ctk
import random
import time
import json
import os
import customtkinter as ctk


class CursingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- 窗口设置 ---
        self.title("KALI LINUX-骂人系统")
        self.geometry("800x600")
        self.resizable(False, False)

        # --- 主题和颜色 (Kali Linux风格) ---
        ctk.set_appearance_mode("Dark")
        self.kali_bg = "#1a1a1a"
        self.kali_green = "#00ff00"
        self.kali_red = "#ff0000"
        self.kali_white = "#ffffff"
        self.configure(fg_color=self.kali_bg)

        # --- 状态变量 ---        
        self.is_attacking = False

        # --- 预定义辱骂内容 ---
        self.insults = [
            "{target}，你的逻辑就像一团乱麻，理都理不清。",
            "{target}，你是不是把脑子落在家里了？",
            "{target}，听你说话就像在听天书，完全不知所云。",
            "{target}，你的智商真是令人堪忧啊。",
            "{target}，你这水平还敢出来丢人现眼？",
            "{target}，我从未见过如此厚颜无耻之人。",
            "{target}，你的理解能力是不是有问题？",
            "{target}，你这智商，是不是被门夹过啊？",
            "{target}，你说话的样子，像极了没吃饱的蚊子。",
            "{target}，你这脑子，大概是用来装饰的吧？",
            "{target}，你要是再笨点，我都得怀疑你是不是故意的。",
            "{target}，我要是你，早就找个地缝钻进去了。",
            "{target}，你这逻辑，我给满分，因为我实在找不到扣分的理由。",
            "{target}，你这水平，不去演小品真是可惜了。",
            "{target}，你这种人，活着就是浪费空气。",
            "{target}，你脑子进水了吧？还是被门挤了？",
            "{target}，我从未见过如此厚颜无耻之人，简直刷新了我的认知下限。",
            "{target}，你这智商，大概也就够用来呼吸了。",
            "{target}，你说话之前能不能先过过脑子？",
            "{target}，我要是你，早就找块豆腐撞死了。",
            "{target}，你这种人，真是让人倒胃口。",
            "{target}，阁下的逻辑，在下实在不敢苟同。",
            "{target}，兄台此言差矣，恕在下无法认同。",
            "{target}，你的见解，真是令在下大开眼界。",
            "{target}，阁下的智商，怕是与在下不在同一水平线上。",
            "{target}，在下奉劝阁下，还是先提升自身素养为好。",
            "{target}，兄台的言论，真是让在下刮目相看。",
            "{target}，阁下的理解能力，在下实在不敢恭维。"
        ]
        # 初始化历史记录
        self.history = []
        self.history_file = "history.json"
        self.load_history()

        # --- 用户界面组件 ---
        self.create_widgets()

    def create_widgets(self):
        # --- 主框架 ---
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # --- 标题标签 ---
        title_label = ctk.CTkLabel(main_frame, text="KALI LINUX 骂人系统", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.kali_green)
        title_label.pack(pady=(0, 20))

        # --- 目标输入 ---
        target_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        target_frame.pack(fill="x", pady=5)
        target_label = ctk.CTkLabel(target_frame, text="辱骂的对象:", font=ctk.CTkFont(size=14), text_color=self.kali_white)
        target_label.pack(side="left", padx=(0, 10))
        self.target_entry = ctk.CTkEntry(target_frame, placeholder_text="输入目标名称...", width=300, fg_color="#2b2b2b", border_color=self.kali_green)
        self.target_entry.pack(side="left", expand=True, fill="x")

        # --- 自定义辱骂内容输入 ---
        custom_insult_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        custom_insult_frame.pack(fill="x", pady=5)
        custom_insult_label = ctk.CTkLabel(custom_insult_frame, text="自定义内容:", font=ctk.CTkFont(size=14), text_color=self.kali_white)
        custom_insult_label.pack(side="left", padx=(0, 10))
        self.custom_insult_entry = ctk.CTkEntry(custom_insult_frame, placeholder_text="(可选) 输入自定义辱骂内容...", fg_color="#2b2b2b", border_color=self.kali_green)
        self.custom_insult_entry.pack(side="left", expand=True, fill="x")

        # --- 攻击次数设置 ---
        attack_count_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        attack_count_frame.pack(fill="x", pady=5)
        attack_count_label = ctk.CTkLabel(attack_count_frame, text="攻击次数:", font=ctk.CTkFont(size=14), text_color=self.kali_white)
        attack_count_label.pack(side="left", padx=(0, 10))
        self.attack_count_slider = ctk.CTkSlider(attack_count_frame, from_=5, to=20, number_of_steps=15, button_color=self.kali_green, button_hover_color=self.kali_green)
        self.attack_count_slider.set(10)
        self.attack_count_slider.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.attack_count_label = ctk.CTkLabel(attack_count_frame, text="10", font=ctk.CTkFont(size=14), text_color=self.kali_green, width=30)
        self.attack_count_label.pack(side="left")
        self.attack_count_slider.bind("<Motion>", lambda event: self.attack_count_label.configure(text=str(int(self.attack_count_slider.get()))))

        # --- 控制按钮区域 ---
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=10)

        # --- 攻击按钮 ---
        self.attack_button = ctk.CTkButton(button_frame, text="开始攻击", command=self.start_attack, font=ctk.CTkFont(size=16, weight="bold"), fg_color=self.kali_red, hover_color="#cc0000")
        self.attack_button.pack(side="left", padx=5, expand=True, fill="x")

        # --- 清除按钮 ---
        self.clear_button = ctk.CTkButton(button_frame, text="清除", command=self.clear_all, font=ctk.CTkFont(size=16, weight="bold"), fg_color="#333333", hover_color="#555555")
        self.clear_button.pack(side="left", padx=5, expand=True, fill="x")

        # --- 历史记录按钮 ---
        self.history_button = ctk.CTkButton(button_frame, text="历史记录", command=self.show_history, font=ctk.CTkFont(size=16, weight="bold"), fg_color="#333333", hover_color="#555555")
        self.history_button.pack(side="left", padx=5, expand=True, fill="x")

        # --- 输出终端 ---
        self.output_terminal = ctk.CTkTextbox(main_frame, font=ctk.CTkFont(family="Courier New", size=12), fg_color="#000000", text_color=self.kali_green, border_color=self.kali_green, border_width=2)
        self.output_terminal.pack(fill="both", expand=True)
        self.output_terminal.insert("end", "[+] 终端准备就绪...等待指令...\n")
        self.output_terminal.configure(state="disabled")

    def start_attack(self):
        target = self.target_entry.get()
        if not target:
            self.show_error("必须指定一个攻击目标！")
            return

        self.is_attacking = True
        self.attack_button.configure(state="disabled", text="攻击中...")
        self.clear_button.configure(state="disabled")
        self.output_terminal.configure(state="normal")
        self.output_terminal.delete("1.0", "end")
        self.output_terminal.insert("end", f"[*] 目标已锁定: {target}\n")
        self.output_terminal.insert("end", "[*] 初始化攻击序列...\n\n")
        self.output_terminal.configure(state="disabled")

        self.attack_step = 0
        self.attack_loop(target)

    def attack_loop(self, target):
        attack_count = int(self.attack_count_slider.get())
        if self.attack_step < attack_count:
            custom_insult = self.custom_insult_entry.get()
            if custom_insult:
                insult = custom_insult.format(target=target)
            else:
                # 随机选择辱骂内容
                insult = random.choice(self.insults).format(target=target)

            # 记录到历史
            self.history.append({
                "target": target,
                "insult": insult,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            })
            # 限制历史记录数量为50
            if len(self.history) > 50:
                self.history.pop(0)

            self.type_writer_effect(f"> {insult}\n", delay=30)
            self.attack_step += 1
            self.after(random.randint(800, 1200), lambda: self.attack_loop(target))
        else:
            self.after(1000, lambda: self.finish_attack())

    def type_writer_effect(self, text, delay=50):
        self.output_terminal.configure(state="normal")
        self._type_char(text, 0, delay)

    def _type_char(self, text, index, delay):
        if index < len(text):
            self.output_terminal.insert("end", text[index])
            self.output_terminal.see("end")
            self.after(delay, lambda: self._type_char(text, index+1, delay))
        else:
            self.output_terminal.configure(state="disabled")

    def finish_attack(self):
        self.output_terminal.configure(state="normal")
        self.output_terminal.insert("end", "\n[+] 攻击序列完成。目标精神已崩溃。\n")
        self.output_terminal.see("end")
        self.output_terminal.configure(state="disabled")
        # 保存历史记录
        self.save_history()
        self.is_attacking = False
        self.attack_button.configure(state="normal", text="开始攻击")
        self.clear_button.configure(state="normal")

    def clear_all(self):
        self.target_entry.delete(0, "end")
        self.custom_insult_entry.delete(0, "end")
        self.output_terminal.configure(state="normal")
        self.output_terminal.delete("1.0", "end")
        self.output_terminal.insert("end", "[+] 终端已重置...等待新指令...\n")
        self.output_terminal.configure(state="disabled")

    def show_error(self, message):
        self.output_terminal.configure(state="normal")
        self.output_terminal.insert("end", f"[!] 错误: {message}\n", "error")
        self.output_terminal.tag_config("error", foreground=self.kali_red)
        self.output_terminal.configure(state="disabled")

    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"加载历史记录失败: {e}")
            self.history = []

    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")

    def show_history(self):
        if not self.history:
            self.output_terminal.configure(state="normal")
            self.output_terminal.insert("end", "[*] 暂无历史记录\n")
            self.output_terminal.configure(state="disabled")
            return

        self.output_terminal.configure(state="normal")
        self.output_terminal.delete("1.0", "end")
        self.output_terminal.insert("end", "[*] 历史记录:\n\n")
        for i, item in enumerate(reversed(self.history), 1):
            self.output_terminal.insert("end", f"{i}. [{item['time']}] 目标: {item['target']} [类型: {item['type']}]\n")
            self.output_terminal.insert("end", f"   {item['insult']}\n\n")
        self.output_terminal.configure(state="disabled")


if __name__ == "__main__":
    app = CursingApp()
    app.mainloop()
