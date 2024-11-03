''' ~~~ Pochven site tracker. ~~~

~ Description ~
Personal Project to track Pochven sites and payouts.
Stores mains and alts, and calculates payouts based 
on site fleet list, variance of number of payouts
received, and altweight.

~ Author ~
iiwii'''

# Goals:
# - Copy and paste fleet list into app
# - App records mains and alts
# -- Way to add new mains/alts.
# - Variable weighting for alts
# - Tracks how much money a site made (+/- 0-10 people)
# - [Tracks who paid]
# - Tracks a whole session of running sites
# - Outputs the payout to each main.

from models import Pilot, Site
from store import Store

class Poch_Tracker:
    def __init__(self):
        self.store = Store()

        self.pilots = self.store.pilots
        self.sites = []

        self.alt_weight = .5

        self.payout_total = 0
        self.payouts = {p.name:0 for p in self.pilots}

    def get_all_main_payouts(self):
        text = ""

        for main in self.payouts:
            text += f"{main}: {self.payouts[main]}\n"


        return text

    def add_site(self, pilots, payout):
        new_site = Site(pilots, payout)
        self.sites.append(new_site)
        return new_site

    def calculate_site_payouts(self, site:Site):
        self.payout_total += site.site_payout

        total_weight = self.calculate_weights(site)

        self.calculate_main_payouts(site, total_weight)

    def calculate_main_payouts(self, site:Site, weight):
        unit_payout = site.site_payout / weight

        # calculate payouts per weight
        for char in site.fleet_pilots:
            if char in self.get_mains():
                if char in self.payouts:
                    self.payouts[char] += unit_payout
                else:
                    self.payouts[char] = unit_payout
            elif char in self.get_alts():
                if self.get_main_of_alt(char) in self.payouts:
                    self.payouts[self.get_main_of_alt(char)] += unit_payout * self.alt_weight
                else:
                    self.payouts[self.get_main_of_alt(char)] = unit_payout * self.alt_weight
            else:
                # add pilot to pilots, main or alt
                pass
        return

    def calculate_weights(self, site):
        # calculate total weight
        total_weight = 0
        for char in site.fleet_pilots:
            if char in self.get_mains():
                total_weight += 1
            elif char in self.get_alts():
                total_weight += self.alt_weight
            else:
                # add pilot to pilots, main or alt
                pass
        return total_weight
    
    def add_main(self, name):
        self.pilots.append(Pilot(name))

    def add_alt(self, main, alt):
        for pilot in self.pilots:
            if pilot.name == main:
                pilot.add_alt(alt)
                return True
        return False

    def get_all_characters(self):
        all = []

        for pilot in self.pilots:
            all.append(pilot.name)
            for alt in pilot.alts:
                all.append("- " + alt)
        
        return all

    def get_mains(self):
        return [p.name for p in self.pilots]
    
    def get_alts(self):
        alts = []
        for pilot in self.pilots:
            for alt in pilot.alts:
                alts.append(alt)
        return alts
    
    def get_main_of_alt(self, alt):
        for pilot in self.pilots:
            if alt in pilot.alts:
                return pilot.name
        return None        

def main():
    pt = Poch_Tracker()
    store = Store()
    pt.pilots = store.pilots

    while True:
        print("Poch Tracker TM\n")

        print("""1. Add main
2. Add alt
3. Add site
4. Calculate payouts
5. Exit
6. Print pilots
7. Print pilots to copy
              """)
        
        choice = input("Choice: ")

        match choice:
            case "1":
                name = input("Main name: ")
                pt.add_main(name)
            case "2":
                main = input("Main name: ")
                alt = input("Alt name: ")
                pt.add_alt(main, alt)
            case "3":
                fleet = input("Fleet list: ").split(",")
                payout = int(input("+/- pilots from 15: "))
                site = Site(fleet, payout)
                pt.calculate_site_payouts(site)
            case "4":
                print(pt.payouts)
                print(pt.payout_total)
            case "5":
                store.pilots = pt.pilots
                store.save_pilots_to_file()
                break
            case "6":
                print({p.name: p.alts for p in pt.pilots})
            case "7":
                for pilot in pt.pilots:
                    print(pilot.name + ",", end='')
                    if pilot.alts != []:
                        print(",".join(pilot.alts), end=',')
                print()
            case _:
                print("Invalid choice")
                continue

        input("Press enter to continue")

    return

# *** Debugging ***

def debug():
    pt = Poch_Tracker()
    print(pt.get_all_main_payouts())


if __name__ == "__main__":
    main()
    #debug()