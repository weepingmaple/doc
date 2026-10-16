from pynput.mouse import Controller
import time
import random
import math

def bezier_curve(t, p0, p1, p2):
    return (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2

def smooth_move(start, end, duration):
    start_time = time.time()
    distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
    
    # Generate a control point for the Bézier curve
    control_x = random.uniform(min(start[0], end[0]), max(start[0], end[0]))
    control_y = random.uniform(min(start[1], end[1]), max(start[1], end[1]))
    
    while time.time() - start_time < duration:
        t = (time.time() - start_time) / duration
        x = bezier_curve(t, start[0], control_x, end[0])
        y = bezier_curve(t, start[1], control_y, end[1])
        mouse.position = (int(x), int(y))
        time.sleep(0.01)  # Small delay for smoother movement

def smooth_move_with_waypoints(start, end, duration):
    # Create several waypoints for more natural movement
    num_waypoints = random.randint(2, 4)  # Random number of waypoints
    waypoints = [(start[0], start[1])]  # Start with initial position
    
    # Generate intermediate waypoints
    for i in range(num_waypoints):
        # Create waypoints that deviate slightly from direct path
        progress = (i + 1) / (num_waypoints + 1)
        base_x = start[0] + (end[0] - start[0]) * progress
        base_y = start[1] + (end[1] - start[1]) * progress
        
        # Add some random deviation
        deviation = 50  # pixels
        way_x = base_x + random.uniform(-deviation, deviation)
        way_y = base_y + random.uniform(-deviation, deviation)
        waypoints.append((way_x, way_y))
    
    waypoints.append(end)  # Add final destination
    
    # Move through each waypoint
    segment_duration = duration / (len(waypoints) - 1)
    for i in range(len(waypoints) - 1):
        start_pos = waypoints[i]
        end_pos = waypoints[i + 1]
        smooth_move(start_pos, end_pos, segment_duration)

def easeInOutQuad(t):
    """
    Quadratic easing function for smooth acceleration and deceleration
    t: Input between 0 and 1
    """
    if t < 0.5:
        return 2 * t * t
    return -1 + (4 - 2 * t) * t

def natural_scroll(direction, total_amount, duration=1.0):
    """
    Performs a natural scrolling motion with acceleration and deceleration
    """
    steps = 60  # Higher number of steps for smoother motion
    start_time = time.time()
    
    # Add slight random variation to total amount for more natural feel
    total_amount *= random.uniform(0.95, 1.05)
    
    # Micro-adjustments
    micro_movements = []
    accumulated = 0
    
    for i in range(steps):
        # Calculate progress with easing
        progress = i / (steps - 1)
        eased_progress = easeInOutQuad(progress)
        
        # Calculate ideal position at this time
        ideal_amount = total_amount * eased_progress
        
        # Add small random variations (tremor)
        tremor = random.uniform(-0.1, 0.1)
        
        # Calculate the difference from last position
        current_movement = ideal_amount - accumulated + tremor
        micro_movements.append(current_movement)
        accumulated += current_movement
    
    # Execute the scrolling movement
    step_duration = duration / steps
    for movement in micro_movements:
        if direction == 'up':
            mouse.scroll(0, movement)
        else:
            mouse.scroll(0, -movement)
        
        # Add slight random variation to timing
        time.sleep(step_duration * random.uniform(0.8, 1.2))

def realistic_scroll_sequence():
    """
    Performs a sequence of realistic scrolling movements
    """
    # Random initial scroll amount
    base_amount = random.uniform(1, 4)
    
    # Determine if this will be a "reading" scroll or "scanning" scroll
    scroll_type = random.choice(['read', 'scan'])
    
    if scroll_type == 'read':
        # Reading pattern: Smaller, more consistent scrolls with pauses
        num_scrolls = random.randint(2, 5)
        for _ in range(num_scrolls):
            amount = base_amount * random.uniform(0.8, 1.2)
            natural_scroll('down', amount, duration=random.uniform(0.3, 0.6))
            # Add reading pause
            time.sleep(random.uniform(0.8, 2.0))
    else:
        # Scanning pattern: Faster, longer scrolls
        amount = base_amount * random.uniform(2, 4)
        natural_scroll('down', amount, duration=random.uniform(0.2, 0.4))
        # Brief pause after scanning
        time.sleep(random.uniform(0.3, 0.7))

# Initialize the mouse controller
mouse = Controller()

print("Smooth mouse jiggler starting...")
print("Press Ctrl+C to stop the program.")

try:
    while True:
        # Random choice between moving or scrolling
        action = random.choice(['move', 'scroll'])
        
        if action == 'scroll':
            if random.random() < 0.8:  # 80% chance of scrolling down (more natural)
                realistic_scroll_sequence()
                print("Performed realistic scroll sequence")
            else:
                # Occasional upward scroll (like going back to previous content)
                amount = random.uniform(1, 3)
                natural_scroll('up', amount, duration=random.uniform(0.3, 0.6))
                print(f"Scrolled up by {amount}")
                # Longer pause after scrolling up
                time.sleep(random.uniform(1.0, 2.0))
        else:
            # Get screen size
            screen_size = (1920, 1080) # Adjust to your screen resolution

            # Get current mouse position
            start_pos = mouse.position
            
            # Generate random coordinates within screen boundaries
            end_x = random.randint(0, screen_size[0])
            end_y = random.randint(0, screen_size[1])
            end_pos = (end_x, end_y)
            
            # Move the mouse smoothly through multiple waypoints
            move_duration = random.uniform(2, 5)  # Slightly longer duration for multiple segments
            smooth_move_with_waypoints(start_pos, end_pos, move_duration)
            
            # Log the movement
            print(f"Moved mouse to ({end_x}, {end_y})")
            
            # Random pause between movements
            time.sleep(random.uniform(1, 5))

except KeyboardInterrupt:
    print("\nSmooth mouse jiggler stopped.")
