import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
try:
    from db_config import execute_query, execute_write, execute_returning
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False

C = {
    "bg":       "#0F172A",   # dark navy
    "surface":  "#1E293B",   # card surface
    "border":   "#334155",   # borders
    "accent":   "#38BDF8",   # sky blue
    "accent2":  "#F97316",   # orange
    "success":  "#22C55E",
    "danger":   "#EF4444",
    "text":     "#F1F5F9",
    "muted":    "#94A3B8",
    "white":    "#FFFFFF",
    "header":   "#0EA5E9",
}

FONT_H1   = ("Segoe UI", 22, "bold")
FONT_H2   = ("Segoe UI", 15, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 9)
FONT_BTN  = ("Segoe UI", 10, "bold")

MOCK = {
    "users": [
        {"user_id": 1, "username": "admin",    "full_name": "System Administrator", "group_name": "Admin",    "is_active": True},
        {"user_id": 2, "username": "john_emp", "full_name": "John Smith",           "group_name": "Employee", "is_active": True},
        {"user_id": 3, "username": "coach_ali","full_name": "Ali Yilmaz",           "group_name": "Coach",    "is_active": True},
    ],
    "tournaments": [
        {"tournament_id": 1, "tournament_name": "Turkey Super Cup 2025",  "sport_type": "Football",   "start_date": "2025-09-01", "end_date": "2025-12-15", "status": "Completed",  "prize_pool": 500000},
        {"tournament_id": 2, "tournament_name": "Ankara Basketball League","sport_type": "Basketball", "start_date": "2025-10-01", "end_date": "2026-02-28", "status": "Completed",  "prize_pool": 100000},
        {"tournament_id": 3, "tournament_name": "Spring Football League",  "sport_type": "Football",   "start_date": "2026-03-15", "end_date": "2026-06-30", "status": "Ongoing",    "prize_pool": 250000},
        {"tournament_id": 4, "tournament_name": "National Tennis Open",    "sport_type": "Tennis",     "start_date": "2026-05-01", "end_date": "2026-05-20", "status": "Ongoing",    "prize_pool":  75000},
    ],
    "teams": [
        {"team_id": 1, "team_name": "Galatasaray",    "city": "Istanbul", "coach_name": "Okan Buruk",    "tournament_name": "Turkey Super Cup 2025",   "wins": 10, "losses": 2, "draws": 4, "points": 34},
        {"team_id": 2, "team_name": "Fenerbahce",     "city": "Istanbul", "coach_name": "Jose Mourinho", "tournament_name": "Turkey Super Cup 2025",   "wins": 9,  "losses": 3, "draws": 4, "points": 31},
        {"team_id": 3, "team_name": "Besiktas",       "city": "Istanbul", "coach_name": "Giovanni",      "tournament_name": "Turkey Super Cup 2025",   "wins": 7,  "losses": 5, "draws": 4, "points": 25},
        {"team_id": 5, "team_name": "Ankara Hawks",   "city": "Ankara",   "coach_name": "Ali Yilmaz",    "tournament_name": "Ankara Basketball League","wins": 14, "losses": 2, "draws": 0, "points": 28},
        {"team_id": 7, "team_name": "Antalyaspor",    "city": "Antalya",  "coach_name": "Coach K",       "tournament_name": "Spring Football League",  "wins": 5,  "losses": 2, "draws": 3, "points": 18},
    ],
    "players": [
        {"player_id": 1, "full_name": "Mauro Icardi",  "nationality": "Argentine", "position": "Forward",    "jersey_number": 9,  "goals_scored": 18, "assists": 5,  "is_active": True},
        {"player_id": 2, "full_name": "Hakim Ziyech",  "nationality": "Moroccan",  "position": "Midfielder", "jersey_number": 22, "goals_scored": 8,  "assists": 12, "is_active": True},
        {"player_id": 3, "full_name": "Edin Dzeko",    "nationality": "Bosnian",   "position": "Forward",    "jersey_number": 10, "goals_scored": 14, "assists": 4,  "is_active": True},
        {"player_id": 9, "full_name": "Ahmad Hassan",  "nationality": "Egyptian",  "position": "Forward",    "jersey_number": 9,  "goals_scored": 22, "assists": 7,  "is_active": True},
        {"player_id": 4, "full_name": "Dusan Tadic",   "nationality": "Serbian",   "position": "Midfielder", "jersey_number": 11, "goals_scored": 6,  "assists": 15, "is_active": True},
    ],
    "matches": [
        {"match_id": 1, "tournament_name": "Turkey Super Cup 2025", "home_team": "Galatasaray", "away_team": "Fenerbahce", "match_date": "2025-09-15 20:00", "round_name": "Group Stage", "status": "Completed", "home_score": 3, "away_score": 1},
        {"match_id": 2, "tournament_name": "Turkey Super Cup 2025", "home_team": "Besiktas",    "away_team": "Trabzonspor","match_date": "2025-09-16 18:00", "round_name": "Group Stage", "status": "Completed", "home_score": 2, "away_score": 2},
        {"match_id": 5, "tournament_name": "Turkey Super Cup 2025", "home_team": "Galatasaray", "away_team": "Trabzonspor","match_date": "2025-11-15 20:00", "round_name": "Semi Final",  "status": "Completed", "home_score": 4, "away_score": 2},
        {"match_id": 8, "tournament_name": "Spring Football League", "home_team": "Antalyaspor","away_team": "Sivasspor", "match_date": "2026-04-20 18:00", "round_name": "Group Stage", "status": "Scheduled","home_score": None,"away_score": None},
    ],
}

def styled_button(parent, text, command, color=None, width=16):
    color = color or C["accent"]
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg=C["white"], font=FONT_BTN,
        relief="flat", cursor="hand2",
        activebackground=C["border"], activeforeground=C["white"],
        padx=10, pady=6, width=width
    )
    return btn

def section_label(parent, text):
    lbl = tk.Label(parent, text=text, font=FONT_H2,
                   bg=C["surface"], fg=C["accent"])
    return lbl

def build_treeview(parent, columns, height=12):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Dark.Treeview",
                    background=C["surface"],
                    foreground=C["text"],
                    fieldbackground=C["surface"],
                    rowheight=26,
                    font=FONT_BODY)
    style.configure("Dark.Treeview.Heading",
                    background=C["bg"],
                    foreground=C["accent"],
                    font=("Segoe UI", 10, "bold"),
                    relief="flat")
    style.map("Dark.Treeview",
              background=[("selected", C["header"])],
              foreground=[("selected", C["white"])])

    frame = tk.Frame(parent, bg=C["surface"])
    tree = ttk.Treeview(frame, columns=columns, show="headings",
                        height=height, style="Dark.Treeview")

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
        tree.column(col, width=120, anchor="center")

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    return frame, tree

class LoginScreen(tk.Frame):
    def __init__(self, master, on_login):
        super().__init__(master, bg=C["bg"])
        self.on_login = on_login
        self._build()

    def _build(self):
        panel = tk.Frame(self, bg=C["surface"], padx=40, pady=40)
        panel.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(panel, text="🏆", font=("Segoe UI", 48), bg=C["surface"], fg=C["accent"]).pack()
        tk.Label(panel, text="Sports Tournament", font=("Segoe UI", 20, "bold"),
                 bg=C["surface"], fg=C["white"]).pack()
        tk.Label(panel, text="Database Management System", font=("Segoe UI", 11),
                 bg=C["surface"], fg=C["muted"]).pack(pady=(0, 24))

        tk.Label(panel, text="Username", font=FONT_BODY, bg=C["surface"], fg=C["muted"], anchor="w").pack(fill="x")
        self.username_var = tk.StringVar(value="admin")
        tk.Entry(panel, textvariable=self.username_var, font=FONT_BODY,
                 bg=C["bg"], fg=C["text"], insertbackground=C["text"],
                 relief="flat", bd=6, width=30).pack(fill="x", pady=(2, 12))

        tk.Label(panel, text="Password", font=FONT_BODY, bg=C["surface"], fg=C["muted"], anchor="w").pack(fill="x")
        self.password_var = tk.StringVar(value="admin123")
        tk.Entry(panel, textvariable=self.password_var, font=FONT_BODY,
                 bg=C["bg"], fg=C["text"], insertbackground=C["text"],
                 show="●", relief="flat", bd=6, width=30).pack(fill="x", pady=(2, 20))

        styled_button(panel, "  Login  →", self._login, width=30).pack(fill="x")

        self.status_lbl = tk.Label(panel, text="", font=FONT_BODY,
                                   bg=C["surface"], fg=C["danger"])
        self.status_lbl.pack(pady=(8, 0))

        tk.Label(panel, text="Demo: admin / admin123", font=("Segoe UI", 9),
                 bg=C["surface"], fg=C["muted"]).pack(pady=(12, 0))

    def _login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            self.status_lbl.config(text="Please enter username and password.")
            return

        if DB_AVAILABLE:
            rows = execute_query(
                "SELECT u.*, ug.group_name FROM users u "
                "JOIN user_groups ug ON u.group_id = ug.group_id "
                "WHERE u.username = %s AND u.is_active = TRUE",
                (username,)
            )
            if rows:
                self.on_login(rows[0])
            else:
                self.status_lbl.config(text="Invalid username or password.")
        else:
            DEMO_CREDS = {"admin": "admin123", "john_emp": "password123"}
            if username in DEMO_CREDS and DEMO_CREDS[username] == password:
                user = next(u for u in MOCK["users"] if u["username"] == username)
                self.on_login(user)
            else:
                self.status_lbl.config(text="Invalid credentials. Try admin / admin123")

class DashboardScreen(tk.Frame):
    def __init__(self, master, current_user, navigate):
        super().__init__(master, bg=C["bg"])
        self.current_user = current_user
        self.navigate = navigate
        self._build()

    def _build(self):
        hdr = tk.Frame(self, bg=C["surface"], pady=12, padx=20)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🏆 Sports Tournament DMS", font=FONT_H1,
                 bg=C["surface"], fg=C["accent"]).pack(side="left")
        tk.Label(hdr, text=f"Welcome, {self.current_user.get('full_name','User')}  |  Role: {self.current_user.get('group_name','—')}",
                 font=FONT_BODY, bg=C["surface"], fg=C["muted"]).pack(side="right", padx=10)

        stats_frame = tk.Frame(self, bg=C["bg"], pady=16)
        stats_frame.pack(fill="x", padx=20)

        stats = self._fetch_stats()
        stat_cards = [
            ("Tournaments", stats[0], C["accent"],  "🏆"),
            ("Teams",       stats[1], C["accent2"], "👥"),
            ("Players",     stats[2], C["success"],  "⚽"),
            ("Matches",     stats[3], C["header"],  "📅"),
        ]
        for label, value, color, icon in stat_cards:
            card = tk.Frame(stats_frame, bg=C["surface"], padx=24, pady=18, relief="flat")
            card.pack(side="left", expand=True, fill="both", padx=8)
            tk.Label(card, text=icon, font=("Segoe UI", 28), bg=C["surface"], fg=color).pack()
            tk.Label(card, text=str(value), font=("Segoe UI", 26, "bold"),
                     bg=C["surface"], fg=color).pack()
            tk.Label(card, text=label, font=FONT_BODY, bg=C["surface"], fg=C["muted"]).pack()

        nav_frame = tk.Frame(self, bg=C["bg"], pady=10)
        nav_frame.pack(fill="x", padx=20)
        nav_items = [
            ("🏆 Tournaments",  "tournaments",  C["accent"]),
            ("👥 Teams",        "teams",        C["accent2"]),
            ("⚽ Players",      "players",      C["success"]),
            ("📅 Matches",      "matches",      C["header"]),
            ("📊 Reports",      "reports",      "#A855F7"),
            ("👤 Users",        "users",        C["muted"]),
        ]
        for label, screen, color in nav_items:
            btn = tk.Button(
                nav_frame, text=label,
                command=lambda s=screen: self.navigate(s),
                bg=color, fg=C["white"], font=FONT_BTN,
                relief="flat", cursor="hand2", padx=14, pady=10, width=14
            )
            btn.pack(side="left", padx=6, pady=4)

        rec_frame = tk.Frame(self, bg=C["surface"], padx=20, pady=14)
        rec_frame.pack(fill="both", expand=True, padx=20, pady=10)
        section_label(rec_frame, "Recent & Upcoming Matches").pack(anchor="w", pady=(0, 8))

        cols = ("Match ID", "Tournament", "Home Team", "Score", "Away Team", "Date", "Status")
        tv_frame, self.tree = build_treeview(rec_frame, cols, height=8)
        tv_frame.pack(fill="both", expand=True)

        self._load_matches()

    def _fetch_stats(self):
        if DB_AVAILABLE:
            t = execute_query("SELECT COUNT(*) AS c FROM tournaments")[0]["c"]
            tm = execute_query("SELECT COUNT(*) AS c FROM teams")[0]["c"]
            p = execute_query("SELECT COUNT(*) AS c FROM players")[0]["c"]
            m = execute_query("SELECT COUNT(*) AS c FROM matches")[0]["c"]
            return t, tm, p, m
        return len(MOCK["tournaments"]), len(MOCK["teams"]), len(MOCK["players"]), len(MOCK["matches"])

    def _load_matches(self):
        self.tree.delete(*self.tree.get_children())
        if DB_AVAILABLE:
            rows = execute_query("""
                SELECT m.match_id, t.tournament_name,
                       h.team_name AS home_team,
                       COALESCE(mr.home_score::text,'—') || ' - ' || COALESCE(mr.away_score::text,'—') AS score,
                       a.team_name AS away_team,
                       TO_CHAR(m.match_date,'YYYY-MM-DD HH24:MI') AS match_date,
                       m.status
                FROM matches m
                JOIN tournaments t ON m.tournament_id = t.tournament_id
                JOIN teams h ON m.home_team_id = h.team_id
                JOIN teams a ON m.away_team_id = a.team_id
                LEFT JOIN match_results mr ON m.match_id = mr.match_id
                ORDER BY m.match_date DESC LIMIT 10
            """)
        else:
            rows = []
            for r in MOCK["matches"]:
                sc = f"{r['home_score']} - {r['away_score']}" if r["home_score"] is not None else "— - —"
                rows.append({"match_id": r["match_id"], "tournament_name": r["tournament_name"],
                              "home_team": r["home_team"], "score": sc,
                              "away_team": r["away_team"], "match_date": r["match_date"], "status": r["status"]})
        for row in rows:
            tag = "done" if row["status"] == "Completed" else ("live" if row["status"] == "Live" else "sched")
            self.tree.insert("", "end", values=list(row.values()), tags=(tag,))
        self.tree.tag_configure("done",  background="#1a2e1a")
        self.tree.tag_configure("live",  background="#2e1a1a")
        self.tree.tag_configure("sched", background=C["surface"])

class TournamentsScreen(tk.Frame):
    def __init__(self, master, navigate):
        super().__init__(master, bg=C["bg"])
        self.navigate = navigate
        self._build()
        self._load()

    def _build(self):
        tb = tk.Frame(self, bg=C["surface"], pady=10, padx=16)
        tb.pack(fill="x")
        tk.Label(tb, text="🏆 Tournaments", font=FONT_H1, bg=C["surface"], fg=C["accent"]).pack(side="left")
        styled_button(tb, "← Back", lambda: self.navigate("dashboard"), C["muted"], 10).pack(side="right", padx=4)
        styled_button(tb, "+ Add Tournament", self._open_add_form, width=18).pack(side="right", padx=4)

        list_frame = tk.Frame(self, bg=C["surface"], padx=16, pady=10)
        list_frame.pack(fill="both", expand=True, padx=16, pady=10)
        cols = ("ID", "Name", "Sport", "Start Date", "End Date", "Status", "Prize Pool", "Max Teams")
        tv_frame, self.tree = build_treeview(list_frame, cols, height=14)
        tv_frame.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self, bg=C["bg"], pady=8)
        btn_frame.pack(fill="x", padx=16)
        styled_button(btn_frame, "✏️  Edit Selected",   self._edit_selected,   C["accent2"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🗑️  Delete Selected", self._delete_selected, C["danger"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🔄 Refresh",          self._load,            C["header"]).pack(side="left", padx=4)

    def _load(self):
        self.tree.delete(*self.tree.get_children())
        if DB_AVAILABLE:
            rows = execute_query("""
                SELECT tournament_id, tournament_name, sport_type,
                       start_date, end_date, status,
                       '$' || TO_CHAR(prize_pool,'FM999,999,999') AS prize_pool,
                       max_teams
                FROM tournaments ORDER BY tournament_id
            """)
        else:
            rows = [{"tournament_id": r["tournament_id"], "tournament_name": r["tournament_name"],
                     "sport_type": r["sport_type"], "start_date": r["start_date"],
                     "end_date": r["end_date"], "status": r["status"],
                     "prize_pool": f"${r['prize_pool']:,}", "max_teams": 16}
                    for r in MOCK["tournaments"]]
        for row in rows:
            self.tree.insert("", "end", values=list(row.values()))

    def _open_add_form(self):
        TournamentForm(self, title="Add Tournament", on_save=self._save_new)

    def _save_new(self, data):
        if DB_AVAILABLE:
            execute_write("""
                INSERT INTO tournaments (tournament_name, sport_type, start_date, end_date, prize_pool, max_teams, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (data["name"], data["sport"], data["start"], data["end"],
                  data["prize"], data["max_teams"], data["status"]))
        else:
            MOCK["tournaments"].append({"tournament_id": len(MOCK["tournaments"])+1,
                                        "tournament_name": data["name"], "sport_type": data["sport"],
                                        "start_date": data["start"], "end_date": data["end"],
                                        "status": data["status"], "prize_pool": float(data["prize"])})
        self._load()

    def _edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a tournament to edit.")
            return
        vals = self.tree.item(sel[0])["values"]
        TournamentForm(self, title="Edit Tournament", existing=vals, on_save=lambda d: self._save_edit(vals[0], d))

    def _save_edit(self, tid, data):
        if DB_AVAILABLE:
            execute_write("""
                UPDATE tournaments SET tournament_name=%s, sport_type=%s, start_date=%s,
                end_date=%s, prize_pool=%s, max_teams=%s, status=%s
                WHERE tournament_id=%s
            """, (data["name"], data["sport"], data["start"], data["end"],
                  data["prize"], data["max_teams"], data["status"], tid))
        self._load()

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a tournament to delete.")
            return
        vals = self.tree.item(sel[0])["values"]
        if messagebox.askyesno("Confirm Delete", f"Delete tournament '{vals[1]}'?"):
            if DB_AVAILABLE:
                execute_write("DELETE FROM tournaments WHERE tournament_id = %s", (vals[0],))
            else:
                MOCK["tournaments"] = [t for t in MOCK["tournaments"] if t["tournament_id"] != vals[0]]
            self._load()


class TournamentForm(tk.Toplevel):
    def __init__(self, parent, title, on_save, existing=None):
        super().__init__(parent)
        self.title(title)
        self.configure(bg=C["surface"])
        self.resizable(False, False)
        self.on_save = on_save
        self.existing = existing
        self._build()
        self.grab_set()

    def _build(self):
        tk.Label(self, text=self.title(), font=FONT_H2, bg=C["surface"], fg=C["accent"]).pack(pady=12)

        fields_frame = tk.Frame(self, bg=C["surface"], padx=24)
        fields_frame.pack(fill="x")

        labels = ["Tournament Name", "Sport Type", "Start Date (YYYY-MM-DD)",
                  "End Date (YYYY-MM-DD)", "Prize Pool ($)", "Max Teams", "Status"]
        self.entries = {}
        defaults = ["", "Football", "", "", "0", "16", "Upcoming"]
        if self.existing:
            defaults = [str(v) for v in self.existing[1:]]

        sport_opts  = ["Football", "Basketball", "Tennis", "Volleyball", "Swimming"]
        status_opts = ["Upcoming", "Ongoing", "Completed", "Cancelled"]

        for i, (label, default) in enumerate(zip(labels, defaults)):
            tk.Label(fields_frame, text=label, font=FONT_BODY,
                     bg=C["surface"], fg=C["muted"]).grid(row=i, column=0, sticky="w", pady=4, padx=4)

            if label == "Sport Type":
                var = tk.StringVar(value=default)
                widget = ttk.Combobox(fields_frame, textvariable=var, values=sport_opts,
                                      state="readonly", width=28)
                self.entries[label] = var
            elif label == "Status":
                var = tk.StringVar(value=default)
                widget = ttk.Combobox(fields_frame, textvariable=var, values=status_opts,
                                      state="readonly", width=28)
                self.entries[label] = var
            else:
                var = tk.StringVar(value=default)
                widget = tk.Entry(fields_frame, textvariable=var, font=FONT_BODY,
                                  bg=C["bg"], fg=C["text"], insertbackground=C["text"],
                                  relief="flat", bd=4, width=30)
                self.entries[label] = var
            widget.grid(row=i, column=1, sticky="ew", pady=4, padx=4)

        btn_frame = tk.Frame(self, bg=C["surface"], pady=16)
        btn_frame.pack()
        styled_button(btn_frame, "Save", self._save, C["success"], 12).pack(side="left", padx=8)
        styled_button(btn_frame, "Cancel", self.destroy, C["danger"], 10).pack(side="left", padx=8)

    def _save(self):
        e = self.entries
        data = {
            "name":     e["Tournament Name"].get().strip(),
            "sport":    e["Sport Type"].get(),
            "start":    e["Start Date (YYYY-MM-DD)"].get().strip(),
            "end":      e["End Date (YYYY-MM-DD)"].get().strip(),
            "prize":    e["Prize Pool ($)"].get().strip() or "0",
            "max_teams":e["Max Teams"].get().strip() or "16",
            "status":   e["Status"].get(),
        }
        if not data["name"] or not data["start"] or not data["end"]:
            messagebox.showerror("Validation Error", "Name, Start Date, and End Date are required.", parent=self)
            return
        self.on_save(data)
        self.destroy()

class TeamsScreen(tk.Frame):
    def __init__(self, master, navigate):
        super().__init__(master, bg=C["bg"])
        self.navigate = navigate
        self._build()
        self._load()

    def _build(self):
        tb = tk.Frame(self, bg=C["surface"], pady=10, padx=16)
        tb.pack(fill="x")
        tk.Label(tb, text="👥 Teams", font=FONT_H1, bg=C["surface"], fg=C["accent2"]).pack(side="left")
        styled_button(tb, "← Back", lambda: self.navigate("dashboard"), C["muted"], 10).pack(side="right", padx=4)
        styled_button(tb, "+ Add Team", self._open_add_form, C["accent2"], 14).pack(side="right", padx=4)

        list_frame = tk.Frame(self, bg=C["surface"], padx=16, pady=10)
        list_frame.pack(fill="both", expand=True, padx=16, pady=10)
        cols = ("ID", "Team Name", "City", "Coach", "Tournament", "W", "L", "D", "Points")
        tv_frame, self.tree = build_treeview(list_frame, cols, height=14)
        tv_frame.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self, bg=C["bg"], pady=8)
        btn_frame.pack(fill="x", padx=16)
        styled_button(btn_frame, "✏️  Edit",   self._edit_selected,   C["accent2"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🗑️  Delete", self._delete_selected, C["danger"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🔄 Refresh", self._load,            C["header"]).pack(side="left", padx=4)

    def _load(self):
        self.tree.delete(*self.tree.get_children())
        if DB_AVAILABLE:
            rows = execute_query("""
                SELECT tm.team_id, tm.team_name, tm.city, tm.coach_name,
                       t.tournament_name, tm.wins, tm.losses, tm.draws, tm.points
                FROM teams tm JOIN tournaments t ON tm.tournament_id = t.tournament_id
                ORDER BY t.tournament_name, tm.points DESC
            """)
        else:
            rows = [{"team_id": r["team_id"], "team_name": r["team_name"], "city": r["city"],
                     "coach_name": r["coach_name"], "tournament_name": r["tournament_name"],
                     "wins": r["wins"], "losses": r["losses"], "draws": r["draws"], "points": r["points"]}
                    for r in MOCK["teams"]]
        for row in rows:
            self.tree.insert("", "end", values=list(row.values()))

    def _open_add_form(self):
        if DB_AVAILABLE:
            t_rows = execute_query("SELECT tournament_id, tournament_name FROM tournaments ORDER BY tournament_name")
        else:
            t_rows = [{"tournament_id": t["tournament_id"], "tournament_name": t["tournament_name"]}
                      for t in MOCK["tournaments"]]
        TeamForm(self, title="Add Team", tournaments=t_rows, on_save=self._save_new)

    def _save_new(self, data):
        if DB_AVAILABLE:
            execute_write("INSERT INTO teams (team_name, city, coach_name, tournament_id) VALUES (%s,%s,%s,%s)",
                          (data["name"], data["city"], data["coach"], data["tournament_id"]))
        else:
            MOCK["teams"].append({"team_id": len(MOCK["teams"])+1, "team_name": data["name"],
                                  "city": data["city"], "coach_name": data["coach"],
                                  "tournament_name": "—", "wins": 0, "losses": 0, "draws": 0, "points": 0})
        self._load()

    def _edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No Selection", "Select a team first."); return
        vals = self.tree.item(sel[0])["values"]
        if DB_AVAILABLE:
            t_rows = execute_query("SELECT tournament_id, tournament_name FROM tournaments ORDER BY tournament_name")
        else:
            t_rows = [{"tournament_id": t["tournament_id"], "tournament_name": t["tournament_name"]}
                      for t in MOCK["tournaments"]]
        TeamForm(self, title="Edit Team", tournaments=t_rows, existing=vals,
                 on_save=lambda d: self._save_edit(vals[0], d))

    def _save_edit(self, tid, data):
        if DB_AVAILABLE:
            execute_write("UPDATE teams SET team_name=%s, city=%s, coach_name=%s WHERE team_id=%s",
                          (data["name"], data["city"], data["coach"], tid))
        self._load()

    def _delete_selected(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("No Selection", "Select a team first."); return
        vals = self.tree.item(sel[0])["values"]
        if messagebox.askyesno("Confirm", f"Delete team '{vals[1]}'?"):
            if DB_AVAILABLE:
                execute_write("DELETE FROM teams WHERE team_id = %s", (vals[0],))
            else:
                MOCK["teams"] = [t for t in MOCK["teams"] if t["team_id"] != vals[0]]
            self._load()

class TeamForm(tk.Toplevel):
    def __init__(self, parent, title, tournaments, on_save, existing=None):
        super().__init__(parent)
        self.title(title); self.configure(bg=C["surface"]); self.resizable(False, False)
        self.on_save = on_save; self.tournaments = tournaments; self.existing = existing
        self._build(); self.grab_set()

    def _build(self):
        tk.Label(self, text=self.title(), font=FONT_H2, bg=C["surface"], fg=C["accent2"]).pack(pady=12)
        f = tk.Frame(self, bg=C["surface"], padx=24); f.pack(fill="x")

        defaults = ["", "", ""]
        if self.existing:
            defaults = [str(self.existing[1]), str(self.existing[2]), str(self.existing[3])]

        for i, (lbl, key, dflt) in enumerate([("Team Name","name",defaults[0]),
                                               ("City","city",defaults[1]),
                                               ("Coach Name","coach",defaults[2])]):
            tk.Label(f, text=lbl, font=FONT_BODY, bg=C["surface"], fg=C["muted"]).grid(row=i, column=0, sticky="w", pady=4)
            var = tk.StringVar(value=dflt)
            tk.Entry(f, textvariable=var, font=FONT_BODY, bg=C["bg"], fg=C["text"],
                     insertbackground=C["text"], relief="flat", bd=4, width=30).grid(row=i, column=1, pady=4, padx=4)
            setattr(self, f"_{key}", var)

        tk.Label(f, text="Tournament", font=FONT_BODY, bg=C["surface"], fg=C["muted"]).grid(row=3, column=0, sticky="w", pady=4)
        t_names = [f"{t['tournament_id']}: {t['tournament_name']}" for t in self.tournaments]
        self._tour_var = tk.StringVar(value=t_names[0] if t_names else "")
        ttk.Combobox(f, textvariable=self._tour_var, values=t_names, state="readonly",
                     width=28).grid(row=3, column=1, pady=4, padx=4)

        btn_frame = tk.Frame(self, bg=C["surface"], pady=16); btn_frame.pack()
        styled_button(btn_frame, "Save", self._save, C["success"], 12).pack(side="left", padx=8)
        styled_button(btn_frame, "Cancel", self.destroy, C["danger"], 10).pack(side="left", padx=8)

    def _save(self):
        tid = int(self._tour_var.get().split(":")[0]) if self._tour_var.get() else None
        self.on_save({"name": self._name.get(), "city": self._city.get(),
                      "coach": self._coach.get(), "tournament_id": tid})
        self.destroy()

class PlayersScreen(tk.Frame):
    def __init__(self, master, navigate):
        super().__init__(master, bg=C["bg"])
        self.navigate = navigate
        self._build()
        self._load()

    def _build(self):
        tb = tk.Frame(self, bg=C["surface"], pady=10, padx=16); tb.pack(fill="x")
        tk.Label(tb, text="⚽ Players", font=FONT_H1, bg=C["surface"], fg=C["success"]).pack(side="left")
        styled_button(tb, "← Back", lambda: self.navigate("dashboard"), C["muted"], 10).pack(side="right", padx=4)
        styled_button(tb, "+ Add Player", self._open_add_form, C["success"], 14).pack(side="right", padx=4)

        list_frame = tk.Frame(self, bg=C["surface"], padx=16, pady=10)
        list_frame.pack(fill="both", expand=True, padx=16, pady=10)
        cols = ("ID", "Full Name", "Nationality", "Position", "Jersey #", "Goals", "Assists", "Active")
        tv_frame, self.tree = build_treeview(list_frame, cols, height=14)
        tv_frame.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self, bg=C["bg"], pady=8); btn_frame.pack(fill="x", padx=16)
        styled_button(btn_frame, "✏️  Edit",   self._edit,   C["accent2"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🗑️  Delete", self._delete, C["danger"]).pack(side="left", padx=4)
        styled_button(btn_frame, "🔄 Refresh", self._load,   C["header"]).pack(side="left", padx=4)

    def _load(self):
        self.tree.delete(*self.tree.get_children())
        if DB_AVAILABLE:
            rows = execute_query("SELECT player_id, full_name, nationality, position, jersey_number, goals_scored, assists, is_active FROM players ORDER BY goals_scored DESC")
        else:
            rows = [{"player_id": p["player_id"], "full_name": p["full_name"], "nationality": p["nationality"],
                     "position": p["position"], "jersey_number": p["jersey_number"],
                     "goals_scored": p["goals_scored"], "assists": p["assists"],
                     "is_active": p["is_active"]} for p in MOCK["players"]]
        for row in rows:
            self.tree.insert("", "end", values=list(row.values()))

    def _open_add_form(self):
        PlayerForm(self, title="Add Player", on_save=self._save_new)

    def _save_new(self, data):
        if DB_AVAILABLE:
            execute_write("""INSERT INTO players (full_name, date_of_birth, nationality, position, jersey_number)
                             VALUES (%s,%s,%s,%s,%s)""",
                          (data["name"], data["dob"], data["nationality"], data["position"], data["jersey"]))
        else:
            MOCK["players"].append({"player_id": len(MOCK["players"])+1, "full_name": data["name"],
                                    "nationality": data["nationality"], "position": data["position"],
                                    "jersey_number": data["jersey"], "goals_scored": 0, "assists": 0, "is_active": True})
        self._load()

    def _edit(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("No Selection","Select a player."); return
        vals = self.tree.item(sel[0])["values"]
        PlayerForm(self, title="Edit Player", existing=vals, on_save=lambda d: self._save_edit(vals[0], d))

    def _save_edit(self, pid, data):
        if DB_AVAILABLE:
            execute_write("UPDATE players SET full_name=%s, nationality=%s, position=%s, jersey_number=%s WHERE player_id=%s",
                          (data["name"], data["nationality"], data["position"], data["jersey"], pid))
        self._load()

    def _delete(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("No Selection","Select a player."); return
        vals = self.tree.item(sel[0])["values"]
        if messagebox.askyesno("Confirm", f"Delete player '{vals[1]}'?"):
            if DB_AVAILABLE:
                execute_write("DELETE FROM players WHERE player_id = %s", (vals[0],))
            else:
                MOCK["players"] = [p for p in MOCK["players"] if p["player_id"] != vals[0]]
            self._load()

class PlayerForm(tk.Toplevel):
    def __init__(self, parent, title, on_save, existing=None):
        super().__init__(parent)
        self.title(title); self.configure(bg=C["surface"]); self.resizable(False, False)
        self.on_save = on_save; self.existing = existing; self._build(); self.grab_set()

    def _build(self):
        tk.Label(self, text=self.title(), font=FONT_H2, bg=C["surface"], fg=C["success"]).pack(pady=12)
        f = tk.Frame(self, bg=C["surface"], padx=24); f.pack(fill="x")
        pos_opts = ["Forward", "Midfielder", "Defender", "Goalkeeper", "Other"]
        defs = ["", "", "", "Forward", "1"]
        if self.existing: defs = [str(self.existing[1]),"",str(self.existing[2]),str(self.existing[3]),str(self.existing[4])]
        fields = [("Full Name","name",defs[0]), ("Date of Birth (YYYY-MM-DD)","dob",defs[1]),
                  ("Nationality","nationality",defs[2]), ("Position","position",defs[3]),
                  ("Jersey Number","jersey",defs[4])]
        self._vars = {}
        for i, (lbl, key, dflt) in enumerate(fields):
            tk.Label(f, text=lbl, font=FONT_BODY, bg=C["surface"], fg=C["muted"]).grid(row=i, column=0, sticky="w", pady=4)
            var = tk.StringVar(value=dflt)
            if key == "position":
                w = ttk.Combobox(f, textvariable=var, values=pos_opts, state="readonly", width=28)
            else:
                w = tk.Entry(f, textvariable=var, font=FONT_BODY, bg=C["bg"], fg=C["text"],
                             insertbackground=C["text"], relief="flat", bd=4, width=30)
            w.grid(row=i, column=1, pady=4, padx=4)
            self._vars[key] = var
        bf = tk.Frame(self, bg=C["surface"], pady=16); bf.pack()
        styled_button(bf, "Save", self._save, C["success"], 12).pack(side="left", padx=8)
        styled_button(bf, "Cancel", self.destroy, C["danger"], 10).pack(side="left", padx=8)

    def _save(self):
        self.on_save({k: v.get() for k, v in self._vars.items()})
        self.destroy()

class MatchesScreen(tk.Frame):
    def __init__(self, master, navigate):
        super().__init__(master, bg=C["bg"])
        self.navigate = navigate
        self._build()
        self._load()

    def _build(self):
        tb = tk.Frame(self, bg=C["surface"], pady=10, padx=16); tb.pack(fill="x")
        tk.Label(tb, text="📅 Matches", font=FONT_H1, bg=C["surface"], fg=C["header"]).pack(side="left")
        styled_button(tb, "← Back", lambda: self.navigate("dashboard"), C["muted"], 10).pack(side="right", padx=4)

        list_frame = tk.Frame(self, bg=C["surface"], padx=16, pady=10)
        list_frame.pack(fill="both", expand=True, padx=16, pady=10)
        cols = ("ID", "Tournament", "Home Team", "Score", "Away Team", "Date", "Round", "Status")
        tv_frame, self.tree = build_treeview(list_frame, cols, height=12)
        tv_frame.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self, bg=C["bg"], pady=8); btn_frame.pack(fill="x", padx=16)
        styled_button(btn_frame, "🏁 Record Result", self._record_result, C["success"], 16).pack(side="left", padx=4)
        styled_button(btn_frame, "🔄 Refresh",       self._load,          C["header"],  12).pack(side="left", padx=4)

    def _load(self):
        self.tree.delete(*self.tree.get_children())
        if DB_AVAILABLE:
            rows = execute_query("""
                SELECT m.match_id, t.tournament_name,
                       h.team_name,
                       COALESCE(mr.home_score::text,'—')||' - '||COALESCE(mr.away_score::text,'—') AS score,
                       a.team_name,
                       TO_CHAR(m.match_date,'YYYY-MM-DD HH24:MI'),
                       m.round_name, m.status
                FROM matches m
                JOIN tournaments t ON m.tournament_id=t.tournament_id
                JOIN teams h ON m.home_team_id=h.team_id
                JOIN teams a ON m.away_team_id=a.team_id
                LEFT JOIN match_results mr ON m.match_id=mr.match_id
                ORDER BY m.match_date DESC
            """)
        else:
            rows = []
            for r in MOCK["matches"]:
                sc = f"{r['home_score']} - {r['away_score']}" if r["home_score"] is not None else "— - —"
                rows.append({"match_id": r["match_id"], "tournament_name": r["tournament_name"],
                              "home_team": r["home_team"], "score": sc, "away_team": r["away_team"],
                              "match_date": r["match_date"], "round_name": r["round_name"], "status": r["status"]})
        for row in rows:
            self.tree.insert("", "end", values=list(row.values()))

    def _record_result(self):
        sel = self.tree.selection()
        if not sel: messagebox.showwarning("No Selection", "Select a match to record result."); return
        vals = self.tree.item(sel[0])["values"]
        if vals[7] == "Completed":
            messagebox.showinfo("Already Done", "This match result is already recorded."); return
        ResultForm(self, match_id=vals[0], match_label=f"{vals[2]} vs {vals[4]}", on_save=self._save_result)

    def _save_result(self, match_id, home_score, away_score):
        if DB_AVAILABLE:
            execute_write("CALL record_match_result(%s, %s, %s, 90, NULL)",
                          (match_id, home_score, away_score))
        else:
            for r in MOCK["matches"]:
                if r["match_id"] == match_id:
                    r["home_score"] = home_score; r["away_score"] = away_score; r["status"] = "Completed"
        self._load()
        messagebox.showinfo("Success", f"Result recorded: {home_score} - {away_score}")

class ResultForm(tk.Toplevel):
    def __init__(self, parent, match_id, match_label, on_save):
        super().__init__(parent)
        self.title("Record Result"); self.configure(bg=C["surface"]); self.resizable(False, False)
        self.match_id = match_id; self.on_save = on_save; self._build(match_label); self.grab_set()

    def _build(self, label):
        tk.Label(self, text="🏁 Record Match Result", font=FONT_H2, bg=C["surface"], fg=C["success"]).pack(pady=12)
        tk.Label(self, text=label, font=FONT_BODY, bg=C["surface"], fg=C["muted"]).pack()
        f = tk.Frame(self, bg=C["surface"], padx=40, pady=10); f.pack(fill="x")
        tk.Label(f, text="Home Score:", font=FONT_BODY, bg=C["surface"], fg=C["muted"]).grid(row=0, column=0, sticky="w", pady=6)
        self.home_var = tk.IntVar(value=0)
        tk.Spinbox(f, from_=0, to=99, textvariable=self.home_var, width=6, font=FONT_H2,
                   bg=C["bg"], fg=C["text"], buttonbackground=C["border"]).grid(row=0, column=1, padx=10)
        tk.Label(f, text="Away Score:", font=FONT_BODY, bg=C["surface"], fg=C["muted"]).grid(row=1, column=0, sticky="w", pady=6)
        self.away_var = tk.IntVar(value=0)
        tk.Spinbox(f, from_=0, to=99, textvariable=self.away_var, width=6, font=FONT_H2,
                   bg=C["bg"], fg=C["text"], buttonbackground=C["border"]).grid(row=1, column=1, padx=10)
        bf = tk.Frame(self, bg=C["surface"], pady=16); bf.pack()
        styled_button(bf, "Save Result", self._save, C["success"], 14).pack(side="left", padx=8)
        styled_button(bf, "Cancel", self.destroy, C["danger"], 10).pack(side="left", padx=8)

    def _save(self):
        self.on_save(self.match_id, self.home_var.get(), self.away_var.get())
        self.destroy()

class ReportsScreen(tk.Frame):
    QUERIES = {
        "Top Goal Scorers": """
            SELECT p.full_name, p.nationality, p.position,
                   p.goals_scored, p.assists,
                   (p.goals_scored + p.assists) AS contributions
            FROM players p ORDER BY p.goals_scored DESC LIMIT 10
        """,
        "Tournament Standings": """
            SELECT t.tournament_name, tm.team_name,
                   tm.wins, tm.losses, tm.draws, tm.points
            FROM teams tm JOIN tournaments t ON tm.tournament_id=t.tournament_id
            ORDER BY t.tournament_name, tm.points DESC
        """,
        "Match Results Summary": """
            SELECT t.tournament_name,
                   COUNT(m.match_id) AS total_matches,
                   SUM(COALESCE(mr.home_score,0)+COALESCE(mr.away_score,0)) AS total_goals,
                   ROUND(AVG(COALESCE(mr.home_score,0)+COALESCE(mr.away_score,0)),2) AS avg_goals
            FROM tournaments t
            JOIN matches m ON t.tournament_id=m.tournament_id
            LEFT JOIN match_results mr ON m.match_id=mr.match_id
            GROUP BY t.tournament_id, t.tournament_name ORDER BY total_goals DESC
        """,
        "Venue Utilization": """
            SELECT v.venue_name, v.city, v.capacity,
                   COUNT(DISTINCT m.match_id) AS matches_hosted
            FROM venues v LEFT JOIN matches m ON v.venue_id=m.venue_id
            GROUP BY v.venue_id, v.venue_name, v.city, v.capacity
            ORDER BY matches_hosted DESC
        """,
        "User Roles Report": """
            SELECT ug.group_name, COUNT(u.user_id) AS total_users,
                   ug.can_manage_tournaments, ug.can_manage_teams
            FROM user_groups ug LEFT JOIN users u ON ug.group_id=u.group_id
            GROUP BY ug.group_id, ug.group_name, ug.can_manage_tournaments, ug.can_manage_teams
        """,
    }

    MOCK_RESULTS = {
        "Top Goal Scorers": [
            {"full_name": "Ahmad Hassan", "nationality": "Egyptian", "position": "Forward", "goals_scored": 22, "assists": 7, "contributions": 29},
            {"full_name": "Mauro Icardi",  "nationality": "Argentine","position": "Forward", "goals_scored": 18, "assists": 5, "contributions": 23},
            {"full_name": "Edin Dzeko",    "nationality": "Bosnian",  "position": "Forward", "goals_scored": 14, "assists": 4, "contributions": 18},
            {"full_name": "Hakim Ziyech",  "nationality": "Moroccan", "position": "Midfielder","goals_scored": 8, "assists": 12,"contributions": 20},
        ],
        "Tournament Standings": [
            {"tournament_name": "Turkey Super Cup 2025", "team_name": "Galatasaray", "wins": 10, "losses": 2, "draws": 4, "points": 34},
            {"tournament_name": "Turkey Super Cup 2025", "team_name": "Fenerbahce",  "wins": 9,  "losses": 3, "draws": 4, "points": 31},
            {"tournament_name": "Turkey Super Cup 2025", "team_name": "Besiktas",    "wins": 7,  "losses": 5, "draws": 4, "points": 25},
        ],
    }

    def __init__(self, master, navigate):
        super().__init__(master, bg=C["bg"])
        self.navigate = navigate
        self._build()

    def _build(self):
        tb = tk.Frame(self, bg=C["surface"], pady=10, padx=16); tb.pack(fill="x")
        tk.Label(tb, text="📊 Reports & Statistics", font=FONT_H1, bg=C["surface"], fg="#A855F7").pack(side="left")
        styled_button(tb, "← Back", lambda: self.navigate("dashboard"), C["muted"], 10).pack(side="right", padx=4)

        ctrl = tk.Frame(self, bg=C["bg"], pady=8, padx=16); ctrl.pack(fill="x")
        tk.Label(ctrl, text="Select Report:", font=FONT_BODY, bg=C["bg"], fg=C["muted"]).pack(side="left")
        self.report_var = tk.StringVar(value=list(self.QUERIES.keys())[0])
        cb = ttk.Combobox(ctrl, textvariable=self.report_var, values=list(self.QUERIES.keys()),
                          state="readonly", width=30, font=FONT_BODY)
        cb.pack(side="left", padx=8)
        styled_button(ctrl, "▶ Run Query", self._run_report, "#A855F7", 14).pack(side="left", padx=8)

        self.result_frame = tk.Frame(self, bg=C["surface"], padx=16, pady=10)
        self.result_frame.pack(fill="both", expand=True, padx=16, pady=8)

        self.sql_box = tk.Text(self, height=5, font=FONT_MONO, bg=C["bg"], fg=C["accent"],
                               insertbackground=C["text"], relief="flat", padx=8)
        self.sql_box.pack(fill="x", padx=16, pady=(0, 8))

    def _run_report(self):
        report = self.report_var.get()
        query = self.QUERIES[report]

        self.sql_box.delete("1.0", tk.END)
        self.sql_box.insert("1.0", query.strip())

        for w in self.result_frame.winfo_children():
            w.destroy()
        section_label(self.result_frame, f"Results: {report}").pack(anchor="w", pady=(0,8))

        if DB_AVAILABLE:
            try:
                rows = execute_query(query)
            except Exception as e:
                tk.Label(self.result_frame, text=f"Error: {e}", font=FONT_BODY,
                         bg=C["surface"], fg=C["danger"]).pack()
                return
        else:
            rows = self.MOCK_RESULTS.get(report, [{"info": "Demo mode — connect DB for real data"}])

        if not rows:
            tk.Label(self.result_frame, text="No results found.", font=FONT_BODY,
                     bg=C["surface"], fg=C["muted"]).pack()
            return

        cols = list(rows[0].keys())
        tv_frame, tree = build_treeview(self.result_frame, cols, height=10)
        tv_frame.pack(fill="both", expand=True)
        for row in rows:
            tree.insert("", "end", values=list(row.values()))

class UsersScreen(tk.Frame):
    def __init__(self, master, navigate):
        super().__init__(master, bg=C["bg"])
        self.navigate = navigate
        self._build()
        self._load()

    def _build(self):
        tb = tk.Frame(self, bg=C["surface"], pady=10, padx=16); tb.pack(fill="x")
        tk.Label(tb, text="👤 User Management", font=FONT_H1, bg=C["surface"], fg=C["muted"]).pack(side="left")
        styled_button(tb, "← Back", lambda: self.navigate("dashboard"), C["muted"], 10).pack(side="right", padx=4)

        list_frame = tk.Frame(self, bg=C["surface"], padx=16, pady=10)
        list_frame.pack(fill="both", expand=True, padx=16, pady=10)
        cols = ("ID", "Username", "Full Name", "Role", "Active")
        tv_frame, self.tree = build_treeview(list_frame, cols, height=14)
        tv_frame.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self, bg=C["bg"], pady=8); btn_frame.pack(fill="x", padx=16)
        styled_button(btn_frame, "🔄 Refresh", self._load, C["header"]).pack(side="left", padx=4)

    def _load(self):
        self.tree.delete(*self.tree.get_children())
        if DB_AVAILABLE:
            rows = execute_query("""
                SELECT u.user_id, u.username, u.full_name, ug.group_name, u.is_active
                FROM users u JOIN user_groups ug ON u.group_id=ug.group_id
                ORDER BY u.user_id
            """)
        else:
            rows = [{"user_id": u["user_id"], "username": u["username"], "full_name": u["full_name"],
                     "group_name": u["group_name"], "is_active": u["is_active"]}
                    for u in MOCK["users"]]
        for row in rows:
            self.tree.insert("", "end", values=list(row.values()))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sports Tournament Database Management System")
        self.geometry("1280x780")
        self.configure(bg=C["bg"])
        self.resizable(True, True)
        self.current_user = None
        self._show_login()

    def _show_login(self):
        self._clear()
        LoginScreen(self, on_login=self._on_login).pack(fill="both", expand=True)

    def _on_login(self, user):
        self.current_user = user
        self._navigate("dashboard")

    def _navigate(self, screen):
        self._clear()
        screens = {
            "dashboard":   lambda: DashboardScreen(self, self.current_user, self._navigate),
            "tournaments": lambda: TournamentsScreen(self, self._navigate),
            "teams":       lambda: TeamsScreen(self, self._navigate),
            "players":     lambda: PlayersScreen(self, self._navigate),
            "matches":     lambda: MatchesScreen(self, self._navigate),
            "reports":     lambda: ReportsScreen(self, self._navigate),
            "users":       lambda: UsersScreen(self, self._navigate),
        }
        if screen in screens:
            screens[screen]().pack(fill="both", expand=True)

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
