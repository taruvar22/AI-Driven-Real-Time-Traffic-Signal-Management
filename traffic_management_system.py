import time
from collections import deque

class TrafficManagementSystem:
    def __init__(self):
        self.lanes = {}
        self.signals = {}
        self.current_active_signal = None
        
    def setup_intersection(self):
        print("=== Traffic System Setup ===")
        num_lanes = int(input("Enter number of lanes: "))
        
        for i in range(1, num_lanes + 1):
            lane_id = f"Lane_{i}"
            initial_vehicles = int(input(f"Enter initial number of vehicles for {lane_id}: "))
            
            self.lanes[lane_id] = {
                'vehicle_count': initial_vehicles,
                'history': deque(maxlen=10),
                'wait_time': 0
            }
            self.signals[lane_id] = {
                'green_time': 30,
                'min_green': 15,
                'max_green': 60,
                'state': 'red'
            }
        
        # Activate first signal
        first_signal = list(self.signals.keys())[0]
        self.signals[first_signal]['state'] = 'green'
        self.current_active_signal = first_signal
        
    def calculate_green_time(self, lane_id):
        """Three different algorithms to calculate green time"""
        vehicles = self.lanes[lane_id]['vehicle_count']
        wait_time = self.lanes[lane_id]['wait_time']
        
        # Algorithm 1: Simple Linear Formula
        # green_time = 15 + (vehicles * 2) + (wait_time // 10)
        
        # Algorithm 2: Weighted Priority
        priority = (vehicles * 0.6) + (wait_time * 0.4)
        green_time = 15 + (priority * 1.5)
        
        # Algorithm 3: Adaptive Threshold (my recommended approach)
        if vehicles < 5:
            green_time = 20
        elif vehicles < 15:
            green_time = 30
        else:
            green_time = 45
        
        # Ensure within bounds
        min_g = self.signals[lane_id]['min_green']
        max_g = self.signals[lane_id]['max_green']
        return max(min_g, min(int(green_time), max_g))
    
    def update_traffic(self):
        """Allow manual updates or simulate automatic detection"""
        print("\n=== Traffic Update ===")
        for lane_id in self.lanes:
            vehicles = int(input(f"Enter current vehicles for {lane_id}: "))
            self.lanes[lane_id]['history'].append(vehicles)
            self.lanes[lane_id]['vehicle_count'] = vehicles
            
            # Update wait time (simplified)
            if len(self.lanes[lane_id]['history']) > 1:
                diff = vehicles - list(self.lanes[lane_id]['history'])[-2]
                self.lanes[lane_id]['wait_time'] += max(0, diff)
    
    def run_cycle(self):
        """Run one complete traffic light cycle"""
        print("\n=== Running Traffic Cycle ===")
        
        for lane_id in self.signals:
            if lane_id == self.current_active_signal:
                self.signals[lane_id]['state'] = 'green'
                green_time = self.calculate_green_time(lane_id)
                self.signals[lane_id]['green_time'] = green_time
                
                print(f"{lane_id}: GREEN for {green_time} sec (Vehicles: {self.lanes[lane_id]['vehicle_count']})")
                time.sleep(2)  # Simulate time passing
            else:
                self.signals[lane_id]['state'] = 'red'
                print(f"{lane_id}: RED")
        
        # Rotate to next signal
        signals = list(self.signals.keys())
        current_idx = signals.index(self.current_active_signal)
        self.current_active_signal = signals[(current_idx + 1) % len(signals)]
    
    def run_simulation(self):
        self.setup_intersection()
        
        while True:
            self.update_traffic()
            self.run_cycle()
            
            cont = input("\nContinue simulation? (y/n): ")
            if cont.lower() != 'y':
                break

if __name__ == "__main__":
    print("AI Traffic Management System")
    system = TrafficManagementSystem()
    system.run_simulation()