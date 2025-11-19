#!/usr/bin/env python3
"""
Life Cube Desktop Widget
A minimalist desktop widget that displays animated GIFs based on calendar state.
"""

import tkinter as tk
from PIL import Image, ImageTk
from icalendar import Calendar
from datetime import datetime
import os
import pytz


class LifeCubeWidget:
    """Main widget class for the Life Cube application."""
    
    def __init__(self, root):
        """Initialize the Life Cube widget."""
        self.root = root
        self.root.title("Academic Cube")
        self.root.geometry("200x200")
        self.root.resizable(False, False)
        
        # Canvas for displaying animations
        self.canvas = tk.Canvas(root, width=200, height=200, highlightthickness=0)
        self.canvas.pack()
        
        # State management
        self.current_state = None
        self.animation_frames = []
        self.current_frame_index = 0
        self.animation_id = None
        
        # Load animations
        self.idle_frames = self.load_gif("assets/idle.gif")
        self.stressed_frames = self.load_gif("assets/stressed.gif")
        
        # Start the main loop
        self.check_schedule()
        
    def load_gif(self, filepath):
        """Load an animated GIF and return all frames."""
        frames = []
        try:
            gif = Image.open(filepath)
            
            # Extract all frames from the GIF
            try:
                while True:
                    # Convert frame to PhotoImage and store
                    frame = gif.copy()
                    frame = frame.convert('RGBA')
                    photo = ImageTk.PhotoImage(frame)
                    frames.append(photo)
                    
                    # Move to next frame
                    gif.seek(gif.tell() + 1)
            except EOFError:
                pass  # End of frames
                
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
            # Create a simple placeholder frame
            placeholder = Image.new('RGB', (200, 200), (200, 200, 200))
            frames.append(ImageTk.PhotoImage(placeholder))
            
        return frames
    
    def check_schedule(self):
        """Check the schedule file and update state."""
        new_state = self.get_current_state()
        
        if new_state != self.current_state:
            self.current_state = new_state
            self.switch_animation()
            
        # Schedule next check in 30 seconds (30000 milliseconds)
        self.root.after(30000, self.check_schedule)
    
    def get_current_state(self):
        """
        Parse the ICS file and determine current state.
        Returns 'BUSY' if an event is happening now, otherwise 'IDLE'.
        """
        ics_file = "my_schedule.ics"
        
        # Default to IDLE if file doesn't exist
        if not os.path.exists(ics_file):
            return "IDLE"
        
        try:
            with open(ics_file, 'rb') as f:
                cal = Calendar.from_ical(f.read())
            
            # Get current time in UTC
            now = datetime.now(pytz.UTC)
            
            # Check all events
            for component in cal.walk():
                if component.name == "VEVENT":
                    start = component.get('dtstart')
                    end = component.get('dtend')
                    
                    if start and end:
                        # Convert to datetime if needed
                        start_dt = start.dt
                        end_dt = end.dt
                        
                        # Ensure we're working with timezone-aware datetimes
                        if isinstance(start_dt, datetime):
                            if start_dt.tzinfo is None:
                                start_dt = pytz.UTC.localize(start_dt)
                            else:
                                start_dt = start_dt.astimezone(pytz.UTC)
                        else:
                            # It's a date, not datetime - skip for now
                            continue
                            
                        if isinstance(end_dt, datetime):
                            if end_dt.tzinfo is None:
                                end_dt = pytz.UTC.localize(end_dt)
                            else:
                                end_dt = end_dt.astimezone(pytz.UTC)
                        else:
                            # It's a date, not datetime - skip for now
                            continue
                        
                        # Check if current time is within event time
                        if start_dt <= now <= end_dt:
                            return "BUSY"
            
            return "IDLE"
            
        except Exception as e:
            print(f"Error parsing schedule: {e}")
            return "IDLE"
    
    def switch_animation(self):
        """Switch to the appropriate animation based on current state."""
        # Stop current animation
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        
        # Select frames based on state
        if self.current_state == "BUSY":
            self.animation_frames = self.stressed_frames
        else:
            self.animation_frames = self.idle_frames
        
        # Reset to first frame
        self.current_frame_index = 0
        
        # Start animation
        self.animate()
    
    def animate(self):
        """Display the next frame of the current animation."""
        if not self.animation_frames:
            return
        
        # Get current frame
        frame = self.animation_frames[self.current_frame_index]
        
        # Display frame on canvas
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=frame, anchor=tk.NW)
        
        # Move to next frame
        self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)
        
        # Schedule next frame (adjust timing as needed - 50ms for smooth animation)
        self.animation_id = self.root.after(50, self.animate)


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = LifeCubeWidget(root)
    root.mainloop()


if __name__ == "__main__":
    main()
