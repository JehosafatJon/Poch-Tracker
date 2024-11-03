from tkinter import *
from tkinter import ttk
import os
import inspect
from poch_tracker import Poch_Tracker as PT
import models

# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the tracker
pt = PT()

# Event Handlers

def add_site():
    # get list of pilots
    pilots = txt_fleet_pilots.get("1.0", END).split("\n")
    pilots = [p.strip("- ") for p in pilots]
    # get payout
    payout = int(cbx_payout_plus_minus.get())

    site = pt.add_site(pilots, payout)
    pt.calculate_site_payouts(site)

    lbl_pilot_payouts.configure(text=pt.get_all_main_payouts())
    print_payout()
    return

def update_payout_plus_minus():
    return

def update_weight():
    return

def print_payout():
    lbl_payout_total.configure(text=f"\nTotal Payout: {pt.payout_total}")
    return

def add_main():
    pt.add_main(ent_main.get())
    lbl_pilot_payouts.configure(text=pt.get_all_main_payouts())
    return

def add_alt():
    pt.add_alt(ent_main.get(), ent_alt.get())
    lbl_pilot_payouts.configure(text=pt.get_all_main_payouts())
    return

def on_close():
    pt.store.save_pilots_to_file()
    root.destroy()

# GUI Init
root = Tk()
root.title("Poch Site Tracker")
root.geometry("800x600")
root.rowconfigure(0, weight=8)
root.rowconfigure(1, weight=2)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.protocol("WM_DELETE_WINDOW", on_close)

# Set Icon
#app_id = 'APODViewer'
#root.iconbitmap(os.path.join(script_dir, "NASA Logo.ico"))

# Frames
frm_top_right = ttk.Frame(root)
frm_top_right.grid(row=0, column=1, padx=5, pady=5)

frm_top_left = ttk.Frame(root)
frm_top_left.grid(row=0, column=0, padx=5, pady=5)

frm_bot_left = ttk.Frame(root)
frm_bot_left.grid(row=1, column=0, padx=5, pady=5)

frm_bot_right = ttk.Frame(root)
frm_bot_right.grid(row=1, column=1, padx=5, pady=5)

# Widgets
txt_fleet_pilots = Text(frm_top_left, width=30, height=20)
txt_fleet_pilots.pack()

btn_add_site = ttk.Button(frm_bot_left, text="Add Site", command=add_site)
btn_add_site.pack(side=BOTTOM)

cbx_payout_plus_minus = ttk.Combobox(frm_bot_left, values=[*models.Site.PAYOUT_VALUES.keys()])
cbx_payout_plus_minus.pack(side=BOTTOM)
cbx_payout_plus_minus.set("0")

#lbl_pilots = ttk.Label(frm_top_right, text= "\n".join(pt.get_all_characters()))
#lbl_pilots.pack(side=LEFT)

lbl_pilot_payouts = ttk.Label(frm_top_right, text= pt.get_all_main_payouts())
lbl_pilot_payouts.pack( side=RIGHT)

lbl_payout_total = ttk.Label(frm_top_right, text=f"\nTotal Payout: {pt.payout_total}")
lbl_payout_total.pack(side=BOTTOM)

btn_add_main = ttk.Button(frm_bot_right, text="Add Main", command=add_main)
btn_add_main.pack(side=BOTTOM)

btn_add_alt = ttk.Button(frm_bot_right, text="Add Alt", command=add_alt)
btn_add_alt.pack(side=BOTTOM)

ent_main = ttk.Entry(frm_bot_right)
ent_main.pack(side=TOP)
ent_main.insert(0, "Main Name")

ent_alt = ttk.Entry(frm_bot_right)
ent_alt.pack(side=TOP)
ent_alt.insert(0, "Alt Name")

# GUI Loop
root.mainloop()